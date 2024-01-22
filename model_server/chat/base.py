import time
from uuid import uuid4
from langchain.chat_models.openai import ChatOpenAI
from langchain.chat_models.fireworks import ChatFireworks
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    BaseMessage
)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import logging
from datetime import datetime

from model_server.chat.model import (
    InitiateChatParams,
    InitiateChatResult,
    HTTPErrorResponse,
    ChatMessageResult,
    ChatMessageParams,
)
from model_server.chat.util import create_or_get_chat_in_db, get_all_chat_messages
from model_server.config import cfg, logging_level
from model_server.database.database import get_db
from model_server.database.database_models import ChatMessage, User
from model_server.deps import get_current_user
from model_server.embedding.model import GetCourseParams
from model_server.prompts.util import get_system_prompt
from model_server.embedding.embed import embedder


class BaseChatBot:
    router: APIRouter

    def _init_api_routes(self) -> None:

        self.router.add_api_route(
            "/",
            endpoint=self.get_prediction_with_ctx,
            methods=["POST"],
            responses={
                200: {"model": ChatMessageResult},
                400: {"model": HTTPErrorResponse},
                401: {"model": HTTPErrorResponse},
                403: {"model": HTTPErrorResponse},
            },
        )

        self.router.add_api_route(
            "/initiate",
            endpoint=self.initiate_chat,
            methods=["POST"],
            responses={
                200: {"model": InitiateChatResult},
                401: {"model": HTTPErrorResponse},
                403: {"model": HTTPErrorResponse},
            },
        )

        self.router.add_api_route(
            "/delete",
            endpoint=self.delete_chat_history,
            methods=["POST"],
            responses={
                200: {"model": InitiateChatResult},
                400: {"model": HTTPErrorResponse},
                401: {"model": HTTPErrorResponse},
                403: {"model": HTTPErrorResponse},
            },
        )

    def __init__(self):

        self.logger = logging.getLogger(f"{__name__}")
        logging.basicConfig()
        self.logger.setLevel(logging_level)

        self.logger.info("Initiated local chat model")

        if cfg["USE_OPENAI_ENDPOINT"] == 1:

            self.logger.info("Using OpenAI")
            self._model = ChatOpenAI(
                openai_api_key="NONE",  # type: ignore
                openai_api_base="http://127.0.0.1:1234/v1",  # type: ignore
                max_tokens=800,
                temperature=0.3,
                streaming=False,
            )

        else:
            self.logger.info("Using Fireworks")
            self._model = ChatFireworks(
                model="accounts/fireworks/models/yi-34b-200k-capybara",
                model_kwargs={
                    "temperature": 0.4,
                    "max_tokens": 1000,
                },
            )

        self._system_prompt = get_system_prompt("chat.txt")
        self.router = APIRouter(
            tags=["Chat"]
        )
        self._init_api_routes()

    def get_opener_message(self, chat_history):

        self.logger.debug("getting history for opener message.")
        messages: List[HumanMessage | AIMessage | SystemMessage] = [
            SystemMessage(content=self._system_prompt.format(
                user_context=self.ctx,
                search_context="",
                source="",
                ))
        ] + chat_history + [HumanMessage(
            content="This message is invisible to the user. Do not acknowlege it. Generate an opener message based on all the conversation above to greet the user."
        )]  # type: ignore

        self.logger.debug("Generating opener message.")

        result = self._model.predict_messages(
            messages=messages,  # type: ignore
            stop=["</s>"],
            )

        return result

    def get_prediction_with_ctx(
        self,
        chat_message: ChatMessageParams,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> ChatMessageResult:

        self.course_code = embedder.get_course_code(GetCourseParams(subject_name=chat_message.subject), db)
        self.logger.info(f"Got course code: {self.course_code}")
        chat_id = create_or_get_chat_in_db(user.id, self.course_code, db)

        self.chat_history: List[HumanMessage | AIMessage] = get_all_chat_messages(str(chat_id), db)

        self.chat_history = self.chat_history[-20:]
        if len(self.chat_history) > 0:
            if isinstance(self.chat_history[0], AIMessage):
                self.chat_history: List[HumanMessage | AIMessage] = [HumanMessage(content="")] + self.chat_history

        self.chat_history.append(HumanMessage(content=chat_message.message))

        self.logger.info(f"user chat: {chat_message.message}")
        self.logger.info(
            f"using {len(self.chat_history) - 1} messages as history"
            )

        search_ctx, source = embedder.query(
            chat_message.message,
            self.course_code
        )

        self.logger.debug(f"\nSearch ctx: {search_ctx}\n\nSource: {source}")
        self.messages = []
        self.messages: List[BaseMessage] = [
            SystemMessage(content=self._system_prompt.format(
                user_context=self.ctx,
                search_context=search_ctx,
                source=source
                ))
        ] + self.chat_history  # type: ignore

        t = datetime.now()
        self.logger.debug("Starting prediction")

        result = self._model.predict_messages(
            messages=self.messages,  # type: ignore
            stop=["</s>"],
            )

        self.chat_history.append(AIMessage(content=result.content))
        self.logger.info(
            f"ai response: {result.content}\n \
            Prediction took: {datetime.now()-t}"
            )
        self.logger.debug("Adding message to database")

        user_message = ChatMessage(
            id=str(uuid4()),
            created_at=datetime.now(),
            chat_id=chat_id,
            message=chat_message.message,
            from_user=True,
            is_opener=False
        )  # type: ignore

        time.sleep(0.1)

        bot_message = ChatMessage(
            id=str(uuid4()),
            created_at=datetime.now(),
            chat_id=chat_id,
            message=result.content,
            from_user=False,
            is_opener=False
        )  # type: ignore

        db.add(user_message)
        db.add(bot_message)

        db.commit()

        return ChatMessageResult(message=str(result.content))

    def initiate_chat(
        self,
        params: InitiateChatParams,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        self.course_code = embedder.get_course_code(GetCourseParams(subject_name=params.subject), db)
        self.logger.info(f"Got course code: {self.course_code}")
        self.logger.debug(f"Starting to initiate chat for user {user.id}")
        chat_id = create_or_get_chat_in_db(user.id, self.course_code, db)
        self.logger.debug("Got chat")
        self.chat_history = get_all_chat_messages(str(chat_id), db)
        self.logger.debug("Got messages")
        self.ctx = get_system_prompt("user_ctx.txt").format(
            user_name=user.name,
            user_gender=user.gender,
            user_year=user.year,
            user_course=user.department,
            subject_request=params.subject,
        )
        self.chat_history = self.chat_history + [self.get_opener_message(self.chat_history)]
        self.logger.info(
            f"Initiated with {len(self.chat_history)} existing messages"
        )
        return InitiateChatResult(
            messages=[
                {
                    "role": "user" if isinstance(chat, HumanMessage)
                    else "bot",
                    "message": chat.content,
                }
                for chat in self.chat_history
            ]  # type: ignore
        )

    def delete_chat_history(self):
        self.logger.info("Deleting chat history")
        self.chat_history = []
        self.messages = []

        return InitiateChatResult(messages=[])
