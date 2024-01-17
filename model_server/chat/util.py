from uuid import uuid4
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from langchain.schema import HumanMessage, AIMessage
from model_server.database.database_models import Chat, ChatMessage


def get_system_prompt():
    prompt = ""
    with open("model_server/prompts/chat.txt", "r") as f:
        prompt = f.read()
    return prompt


def generate_context(name, subject, year, course):
    pass


def create_or_get_chat_in_db(uid: str, db: Session):
    try:
        chat = db.query(Chat).filter(Chat.user_id == uid).first()  # type: ignore

        if chat is not None:
            if (datetime.now() - chat.time) < timedelta(hours=1):
                return chat.id
    except Exception:
        pass

    new_chat = Chat(
                id=str(uuid4()),
                time=datetime.now(),
                user_id=uid,
            )  # type: ignore

    db.add(new_chat)
    db.commit()
    return new_chat.id


def get_all_chat_messages(chat_id: str, db: Session):

    messages = (
        db.query(ChatMessage)  # type: ignore
        .filter(ChatMessage.chat_id == chat_id)
        .limit(50).all()
    )

    chat_history = []

    for message in messages:
        if message.from_user:
            chat_history.append(HumanMessage(content=message.message))
        else:
            chat_history.append(AIMessage(content=message.message))

    return chat_history
