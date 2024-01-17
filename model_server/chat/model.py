from pydantic import BaseModel
from typing import List, Dict


class ChatMessageParams(BaseModel):
    message: str


class InitiateChatParams(BaseModel):
    name: str
    gender: str
    subject: str
    year: str
    course: str
    course_code: str


class HTTPErrorResponse(BaseModel):
    detail: str


class InitiateChatResult(BaseModel):
    messages: List[Dict[str, str]]


class ChatMessageResult(BaseModel):
    message: str
