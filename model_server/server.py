from fastapi import FastAPI
from model_server.chat.chat import chat

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(chat.router, prefix="/chat")
