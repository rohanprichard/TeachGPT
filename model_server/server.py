from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from model_server.chat.chat import chat
from model_server.database.database import get_db, engine, Base
from model_server.embedding.embed import embedder
from model_server.client.base import client
from model_server.config import logging_level
import logging


logger = logging.getLogger(f"{__name__}")
logging.basicConfig()
logger.setLevel(logging_level)

logger.info("Initializing fastapi app")

app = FastAPI()

origins = ["*"]


@app.get("/ok")
async def root(
    db: Session = Depends(get_db)
):
    return {"db": "ok"}

@app.get("/admin")
async def subapp1():
    return FileResponse("frontend/admin/build/index.html")

app.include_router(chat.router, prefix="/chat")
app.include_router(embedder.router, prefix="/embed")
app.include_router(client.router, prefix="/client")

app.mount("/", StaticFiles(directory="frontend/client/build", html=True), name="client")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

Base.metadata.create_all(bind=engine)  # type: ignore
