---
layout: default
title: "Frontend"
---

# Frontend Documentation

TeachGPT features two dedicated React applications—for clients (students) and for administrators.

## Client Interface
- **Location:** `frontend/client`
- **Purpose:**  
  - Provides an interactive chat interface for students.
  - Displays a conversation with the bot, rendered with support for Markdown (via ReactMarkdown).
- **Key Files:**
  - `ChatInterface.js`:  
    - Manages fetching initial messages, sending new messages, and updating the chat view.
    - Makes POST requests to the `/chat/` endpoint.
  - `ChatMessage.js`:  
    - Renders individual chat messages and includes an optional button for downloading related document files.
  - `apiConfig.js`:  
    - Sets the API URL based on the environment (development/production).

## Admin Interface
- **Location:** `frontend/admin`
- **Purpose:**  
  - Offers an interface for managing courses and documents.
  - Allows administrators to add new courses, upload documents, and view or delete existing documents.
- **Key Files:**
  - `AdminInterface.js`:  
    - Contains forms and interactions for adding courses and documents.
  - `DocumentCard.js`:  
    - Displays individual document details with options to download or delete.
  
## Styling and Build
- Both frontends are bootstrapped with Create React App. Standard CRA scripts (such as `npm start`, `npm run build`, and `npm test`) are available.
- CSS styling is provided (for example, in `frontend/admin/src/index.css`) to maintain a consistent look and feel. 