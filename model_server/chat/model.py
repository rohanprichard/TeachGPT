from pydantic import BaseModel


class ChatMessageParams(BaseModel):
    message: str


class InitiateChatParams(BaseModel):
    name: str
    subject: str
    year: str
    course: str
