from fastapi import HTTPException, APIRouter
from model_server.database.database import SessionLocal
from model_server.database.models import (
    UserCreate,
    UserResponse,
    UserSearch,
    HTTPErrorResponse
    )
from model_server.database.database_models import User


class Client:
    def __init__(self):
        self.router = APIRouter(tags=["Client"])
        self._init_api_routes()

    def _init_api_routes(self) -> None:
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
            "/",
            endpoint=self.get_user_by_id,
            methods=["POST"],
            responses={
                200: {"model": UserSearch},
                400: {"model": HTTPErrorResponse},
                401: {"model": HTTPErrorResponse},
                403: {"model": HTTPErrorResponse},
            },
        )

    # Registration route
    def register_user(self, user_data: UserCreate):
        db = SessionLocal()

        try:
            # Create a new user instance
            new_user = User(**user_data.dict())

            # Add the user to the database
            db.add(new_user)
            db.commit()

            return {'message': 'User registered successfully'}
        except Exception:
            import traceback
            traceback.print_exc()
            db.rollback()
            raise HTTPException(status_code=500, detail='Server Error')
        finally:
            db.close()

    # Search user by ID route
    def get_user_by_id(self, user_search: UserSearch):
        db = SessionLocal()

        try:
            # Query the user by ID
            user = db.query(User)\
                .filter(User.id == user_search.id).first()  # type: ignore

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
        finally:
            db.close()


client = Client()
