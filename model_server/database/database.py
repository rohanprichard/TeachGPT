from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

from model_server.config import cfg, logging_level


logger = logging.getLogger(f"{__name__}")
logging.basicConfig()
logger.setLevel(logging_level)

SQLALCHEMY_DATABASE_URL = (cfg["DB_URL"])

logger.info("Starting SQL DB engine")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

logger.info("DB Initialized and connected")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
