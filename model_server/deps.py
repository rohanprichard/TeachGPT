
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
import logging

from model_server.database.database import get_db
from model_server.database.database_models import User

from .util import (
    ALGORITHM,
    JWT_SECRET_KEY
)
from .database.models import UserResponse
from .config import logging_level

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/client/login",
)

HTTPBearerAuthorization = HTTPBearer(auto_error=False, scheme_name="JWT")

logger = logging.getLogger(f"{__name__}")
logging.basicConfig()
logger.setLevel(logging_level)


async def get_current_user(
        token: str = Depends(reuseable_oauth),
        db: Session = Depends(get_db)
) -> UserResponse:
    try:

        logger.debug("Recieving jwt token")

        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )

        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            logger.debug("Expired token detected")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except Exception:
        logger.debug("Invalid token detected")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == payload["sub"]).first()  # type: ignore

    if user is None:
        logger.debug("Unknown user")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    logger.debug("Token Validated")

    return UserResponse(
        name=user.name,
        id=user.id,
        email=user.email,
        department=user.department,
        year=user.year,
        gender=user.gender
    )
