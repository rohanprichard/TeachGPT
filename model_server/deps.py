
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
import logging
import traceback

from model_server.database.database import get_db
from model_server.database.database_models import User

from .util import (
    ALGORITHM,
    JWT_SECRET_KEY
)
from .database.models import UserResponse

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="login",
)

HTTPBearerAuthorization = HTTPBearer(auto_error=False, scheme_name="JWT")


async def get_current_user(
        token: str = Depends(reuseable_oauth),
        db: Session = Depends(get_db)
) -> UserResponse:
    try:

        logger = logging.getLogger(f"{__name__}")
        logging.basicConfig()
        logger.setLevel(logging.DEBUG)

        logger.debug("logger init")

        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        logger.debug(f"{payload}")
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except Exception:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == payload["sub"]).first()  # type: ignore

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return UserResponse(
        name=user.name,
        id=user.id,
        email=user.email,
        department=user.department,
        year=user.year,
        gender=user.gender
    )
