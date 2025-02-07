---
layout: default
title: "Backend API"
---

# Backend API Documentation

This document outlines the REST API endpoints provided by the FastAPI server within TeachGPT.

## API Routers

### Embedding Router (`/embed`)
This router provides endpoints for processing documents and managing the vector store.

#### Endpoints

- **POST /**  
  - **Description:** Receives a list of files (PDFs/PPTXs), extracts their content, creates text chunks, and adds them as embeddings to the vector store.
  - **Input:**  
    - `files` (List[UploadFile]): Files to process.
  - **Security:** Requires a valid authentication token.
  - **Responses:**  
    - `200`: Returns a message with the number of files added.
    - `401`, `403`, `404`: Error responses.

- **POST /documents**  
  - **Description:** Lists documents associated with a given course.  
  - **Input:**  
    - JSON body with `subject`.
  - **Response:** Returns a list of document metadata and the course code.

- **GET /courses**  
  - **Description:** Retrieves a list of all available course subjects.
  - **Response:** JSON with course names.
  
- **POST /courses/add**  
  - **Description:** Adds a new course to the system.
  - **Input:**  
    - `course_code` (str)
    - `subject_name` (str)
  - **Response:** Success message upon course creation.

- **GET /documents/{course_code}/{filename}**  
  - **Description:** Serves a file download based on course code and filename.
  - **Response:** Returns a FileResponse with appropriate content type.

- **GET /documents/delete/{course_code}/{filename}**  
  - **Description:** Deletes the specified document from both the database and vector store.
  - **Response:** A success/failure message.

---

### Chat Router (`/chat`)
This router handles all chat-related requests.

#### Endpoints

- **POST /** (`get_prediction_with_ctx`)  
  - **Description:** Accepts a user's chat message along with a subject and returns an AI-generated response.  
  - **Input:**  
    - JSON body containing `message` and `subject`.
  - **Response Model:**  
    - `message` (str): The AI response.
    - `document_name` (Optional[str]): Link to a related document if applicable.

- **POST /initiate**  
  - **Description:** Initiates a new chat session and returns any preloaded or greeting messages.
  
- **POST /delete**  
  - **Description:** Deletes the current chat history.

---

### Client Router (`/client`)
This router manages user-related functionality.

#### Endpoints

- **POST /**  
  - **Description:** Retrieves user profile details by email.
  - **Input:**  
    - JSON body with an `email` field.
  - **Response:** User details.

- **POST /register**  
  - **Description:** Registers a new user.
  - **Input:**  
    - User details (name, email, password, department, year, etc.).
  - **Response:** Success message upon registration.

- **POST /login**  
  - **Description:** Authenticates the user credentials.
  - **Input:**  
    - Form data with username (email) and password.
  - **Response:**  
    - `access_token` (str): The authentication token.
    - `token_type` (str).

- **GET /me**  
  - **Description:** Returns the profile details of the currently authenticated user. 