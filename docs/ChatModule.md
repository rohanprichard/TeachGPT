---
layout: default
title: "Chat Module"
---

# Chat Module Documentation

The chat module handles conversations between users and the AI, forming the core interactive functionality of TeachGPT.

## Key Components

### chat/base.py
- **BaseChatBot Class:**  
  - **Purpose:**  
    - Exposes a FastAPI router with endpoints for processing chat messages.
  - **Main Endpoints:**
    - `get_prediction_with_ctx` (POST `/chat/`): Receives a user message (with relevant course subject) and returns an AI-generated reply.
    - `initiate_chat` (POST `/chat/initiate`): Starts a new chat session, potentially sending an opener message.
    - `delete_chat_history` (POST `/chat/delete`): Clears the chat history.
  - **Model Integration:**  
    - Chooses between using an OpenAI endpoint or a local "Fireworks" model based on configuration.
    - Loads the system prompt from a file (e.g., `model_server/prompts/chat.txt`) to establish conversation context.

### chat/util.py
- **get_system_prompt:**  
  - Reads the system prompt file and returns its content for use in the chat session.
  
### Chat History
- The module saves both user and bot messages in the database (using SQLAlchemy models), ensuring that context is maintained throughout a conversation. 