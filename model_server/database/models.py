from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    id: str
    email: str
    hashed_password: str
    department: str
    year: str


class UserResponse(BaseModel):
    name: str
    id: str
    email: str
    department: str
    year: str


class UserSearch(BaseModel):
    id: str


class HTTPErrorResponse(BaseModel):
    detail: str
