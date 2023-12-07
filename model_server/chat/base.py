from langchain.chat_models import ChatOpenAI
from fastapi import APIRouter
import openai
import traceback
from langchain.chains import ConversationChain
from langchain.prompts import (
    ChatPromptTemplate,
)
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from logging import Logger
from model_server.chat.model import ChatMessageParams, InitiateChatParams
from model_server.chat.util import get_system_prompt, generate_context


class BaseChatModel:
    def __init__(self):
        openai.base_url = "http://localhost:1234/v1"  # type: ignore
        self._model = ChatOpenAI(
            openai_api_key="",  # type: ignore
            base_url="http://localhost:1234/v1",  # type: ignore
            max_tokens=256
        )
        self._chat = []
        self.context = ""
        self.router = APIRouter()
        self._logger = Logger("Chat Logger")

        @self.router.get("/test")
        def test():
            return {"chat": "ok"}

        @self.router.post("/")
        def chat(input: ChatMessageParams):

            self._chat.append(HumanMessage(content=input.message))
            self._logger.info(("History before prediction:", self._chat))
            try:
                response = self._model.invoke(self._chat)
                print(response)

            except Exception:
                print(traceback.format_exc())
                return "Something went wrong......"

            self._chat.append(response)
            self._logger.info("AI response:" + str(response.content))

            self._logger.info(("History after prediction:", self._chat))
            return response.content

        @self.router.post("/initiate")
        def initiate(initiate_params: InitiateChatParams):
            self._chat = []

            self.context = generate_context(
                initiate_params.name,
                initiate_params.subject,
                initiate_params.name,
                initiate_params.course
                )

            self._chat.append(SystemMessage(content=get_system_prompt()))
