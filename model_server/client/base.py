from uuid import uuid4
import traceback
from fastapi import HTTPException, APIRouter, Depends
from model_server.database.models import (
    AuthTokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
    UserSearch,
    HTTPErrorResponse
    )
from sqlalchemy.orm import Session
from model_server.database.database_models import User
from model_server.database.database import get_db
from model_server.deps import get_current_user
from model_server.util import (
    create_access_token,
    get_hashed_password,
    verify_password
)


class Client:
    def __init__(self):
        self.router = APIRouter(tags=["Client"])
        self._init_api_routes()

    def _init_api_routes(self) -> None:

        self.router.add_api_route(
            "/",
            endpoint=self.get_user_by_email,
            methods=["POST"],
            responses={
                200: {"model": UserSearch},
                400: {"model": HTTPErrorResponse},
                401: {"model": HTTPErrorResponse},
                403: {"model": HTTPErrorResponse},
            },
        )

        self.router.add_api_route(
            "/register",
            endpoint=self.register_user,
            methods=["POST"],
            responses={
                200: {"model": UserResponse},
                400: {"model": HTTPErrorResponse},
                401: {"model": HTTPErrorResponse},
                403: {"model": HTTPErrorResponse},
            },
        )

        self.router.add_api_route(
            "/login",
            endpoint=self.login,
            methods=["POST"],
            responses={
                200: {"model": AuthTokenResponse},
                400: {"model": HTTPErrorResponse},
                401: {"model": HTTPErrorResponse},
                403: {"model": HTTPErrorResponse},
            },
        )

        self.router.add_api_route(
            "/me",
            endpoint=self.get_me,
            methods=["GET"],
            responses={
                200: {"model": UserResponse},
                400: {"model": HTTPErrorResponse},
                401: {"model": HTTPErrorResponse},
                403: {"model": HTTPErrorResponse},
            },
        )

    def register_user(
        self,
        user_data: UserCreate,
        db: Session = Depends(get_db)
    ):

        try:
            user = db.query(User) \
                .filter(User.email == user_data.email).first()  # type: ignore

            if user is not None:
                raise HTTPException(status_code=401, detail='User Exists')

            new_user = User(
                id=str(uuid4()),
                name=user_data.name,
                email=user_data.email,
                hashed_password=get_hashed_password(user_data.password),
                department=user_data.department,
                year=user_data.year,
            )  # type: ignore

            db.add(new_user)
            db.commit()

            return {'message': 'User registered successfully'}

        except Exception:

            traceback.print_exc()
            db.rollback()
            raise HTTPException(status_code=500, detail='Server Error')

    def get_user_by_email(
        self,
        user_search: UserSearch,
        db: Session = Depends(get_db)
    ):
        # Query the user by ID
        user = db.query(User)\
            .filter(User.email == user_search.email).first()  # type: ignore

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Return user details
        return UserResponse(
            name=user.name,
            id=user.id,
            email=user.email,
            department=user.department,
            year=user.year,
        )

    def login(
        self,
        user_login: UserLogin,
        db: Session = Depends(get_db)
    ):

        user = db.query(User) \
            .filter(User.email == user_login.email).first()  # type: ignore

        if user is None:
            return HTTPErrorResponse(detail='User does not exist')

        if not verify_password(
            password=user_login.password,
            hashed_pass=user.hashed_password
        ):
            return HTTPErrorResponse(detail='User does not exist')

        return AuthTokenResponse(
            access_token=create_access_token(user.id)
        )

    def get_me(self, user: User = Depends(get_current_user)):
        return user


client = Client()
