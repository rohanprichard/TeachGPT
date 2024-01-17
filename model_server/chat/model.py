from pydantic import BaseModel
from typing import List, Dict


class ChatMessageParams(BaseModel):
    message: str


class InitiateChatParams(BaseModel):
    subject: str
    course_code: str


class HTTPErrorResponse(BaseModel):
    detail: str


class InitiateChatResult(BaseModel):
    messages: List[Dict[str, str]]


class ChatMessageResult(BaseModel):
    message: str
