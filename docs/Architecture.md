---
layout: default
title: "Architecture"
---

# Architecture

TeachGPT is organized into several interconnected components, each responsible for part of the overall functionality.

## Components

### Backend
- **FastAPI Server:** Exposes REST API endpoints for chat, document embedding, and user–client operations.
- **Embedding Module:** Processes uploaded PDF/PPTX files, extracts text, splits it into manageable chunks, and saves text embeddings into a persistent vector store (using Chroma).
- **Chat Module:** Manages conversations with AI using context history and system prompts. It selects between an OpenAI-based API or a local model (Fireworks) based on configuration.
- **Client Module:** Handles user registration, authentication, and profile retrieval.

### Database
- **SQLAlchemy ORM:** Used for persistence. The main models include User, Course, Document, Chat, and ChatMessage.

### Frontend
- **Client Interface:** A React app (in `frontend/client`) that provides a chat interface for students.
- **Admin Interface:** A React app (in `frontend/admin`) that allows administrators to manage courses and documents.

## Data Flow
1. **User Interaction:** Students or administrators use the appropriate React interface.
2. **API Communication:** The frontends communicate with the FastAPI back end via REST endpoints.
3. **Processing:** The backend modules handle document embedding, chat message processing, and user management.
4. **Persistence:** Data is stored in a SQL database, while embeddings are stored in Chroma.

This modular architecture supports scalability and easier maintenance. 