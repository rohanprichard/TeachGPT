from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model_server.chat.chat import chat
from model_server.embedding.embed import embed
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(chat.router, prefix="/chat")
app.include_router(embed.router, prefix="/embed")
