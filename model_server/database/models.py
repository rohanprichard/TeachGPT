from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    department: str
    year: str


class UserResponse(BaseModel):
    name: str
    id: str
    email: str
    department: str
    year: str


class UserSearch(BaseModel):
    email: str


class UserLogin(BaseModel):
    email: str
    password: str


class AuthTokenResponse(BaseModel):
    access_token: str


class HTTPErrorResponse(BaseModel):
    detail: str
