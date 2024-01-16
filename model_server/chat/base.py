from langchain.chat_models.openai import ChatOpenAI
from langchain.chat_models.fireworks import ChatFireworks
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    BaseMessage
)
from fastapi import APIRouter
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
from model_server.config import cfg
from model_server.prompts.util import get_system_prompt
from model_server.embedding.embed import embedder


class BaseChatBot:
    router: APIRouter

    def _init_api_routes(self) -> None:
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
        self.logger.setLevel(logging.DEBUG)

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
                    "temperature": 0.3,
                    "max_tokens": 500,
                },
            )

        self._system_prompt = get_system_prompt("chat.txt")
        self.router = APIRouter(
            tags=["Chat"]
        )
        self._init_api_routes()

    def get_prediction_with_ctx(
        self, chat_message: ChatMessageParams
    ) -> ChatMessageResult:
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

        messages: List[BaseMessage] = [
            SystemMessage(content=self._system_prompt.format(
                user_context=self.ctx,
                search_context=search_ctx,
                source=source
                ))
        ] + self.chat_history  # type: ignore
        t = datetime.now()
        self.logger.debug("Starting prediction")
        result = self._model.predict_messages(messages=messages)

        self.chat_history.append(AIMessage(content=result.content))
        self.logger.info(
            f"ai response: {result.content}\n \
            Prediction took: {datetime.now()-t}"
            )

        return ChatMessageResult(message=str(result.content))

    def initiate_chat(self, params: InitiateChatParams):
        self.chat_history = []
        self.messages = []
        self.course_code = params.course_code
        self.ctx = get_system_prompt("user_ctx.txt").format(
            user_name=params.name,
            user_gender=params.gender,
            user_year=params.year,
            user_course=params.course,
            subject_request=params.subject,
        )

        self.logger.info(
            f"Initiated with {len(self.messages)} existing messages"
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
