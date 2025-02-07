---
layout: default
title: "Setup and Installation"
---

# Setup and Installation

This guide explains how to set up and run TeachGPT on your local machine.

## Prerequisites
- Python 3.8 or higher
- Node.js (with npm)
- A supported database engine (SQLite is used by default, but you may configure PostgreSQL or another choice)
- Environment variables:
  - `JWT_SECRET_KEY`: Key used for authenticating JSON Web Tokens.
  - `USE_OPENAI_ENDPOINT`: Set to "1" to use the OpenAI model endpoint or "0" to use the local model.
  - `DB_URL`: Database connection URL.

## Backend Setup
1. **Create a virtual environment**     ```bash
   python -m venv venv   ```
2. **Activate the virtual environment**  
   - On Unix/macOS:       ```bash
     source venv/bin/activate     ```  
   - On Windows:       ```bash
     venv\Scripts\activate     ```
3. **Install backend dependencies**     ```bash
   pip install -r requirements.txt   ```
4. **Set environment variables:**  
   You can create a `.env` file with settings such as:     ```env
   JWT_SECRET_KEY=your_secret_key
   USE_OPENAI_ENDPOINT=1
   DB_URL=sqlite:///./sql_app.db   ```
5. **Run the backend server:**     ```bash
   uvicorn model_server.server:app --reload   ```
   The backend API will be available (by default) at [http://localhost:8000](http://localhost:8000).

## Frontend Setup

### Client Interface
1. **Navigate to the client folder:**     ```bash
   cd frontend/client   ```
2. **Install dependencies:**     ```bash
   npm install   ```
3. **Configure the API URL:**  
   Create a `.env` file (if not already present) with lines like:     ```env
   REACT_APP_API_URL_DEV=http://localhost:8000
   REACT_APP_API_URL_PROD=https://your_production_api_url   ```
4. **Run the client interface:**     ```bash
   npm start   ```

### Admin Interface
1. **Navigate to the admin folder:**     ```bash
   cd frontend/admin   ```
2. **Install dependencies:**     ```bash
   npm install   ```
3. **Run the admin interface:**     ```bash
   npm start   ```

## Testing
- A Jupyter Notebook (`testing.ipynb`) is available for experimental testing of document parsing and other modules.
- You can add unit tests as needed.

## Deployment
- For production, build the React apps by running:    ```bash
  npm run build  ```
- Deploy the build folders using any static file server or integrate them into the FastAPI backend (using StaticFiles middleware). 