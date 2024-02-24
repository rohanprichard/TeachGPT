from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import sys

from model_server.config import cfg, logging_level


logger = logging.getLogger(f"{__name__}")
logging.basicConfig()
logger.setLevel(logging_level)

SQLALCHEMY_DATABASE_URL = (cfg["DB_URL"])

if cfg["DEV"]:
    __import__('pysqlite3')
    logger.info("Swapping sqlite for ChromaDB fix")
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

logger.info(f"Starting SQL DB engine {cfg['DB_URL']}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={'check_same_thread': False}

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
