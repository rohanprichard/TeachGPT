---
layout: default
title: "Deployment"
---

# Deployment Guide

This guide explains how to deploy the TeachGPT project to a production environment.

## Backend Deployment

### Containerization (Optional)
- Create a Dockerfile to containerize the FastAPI server.
- Use a multi-stage build to optimize image size.

### Server Deployment
- Deploy on a cloud provider (AWS, DigitalOcean, etc.) using a process manager like Gunicorn with Uvicorn workers:  ```bash
  gunicorn model_server.server:app -k uvicorn.workers.UvicornWorker  ```
- Configure your environment variables on the server:
  - `JWT_SECRET_KEY`
  - `USE_OPENAI_ENDPOINT`
  - `DB_URL`

### Database Considerations
- Ensure the chosen database is set up and accessible.
- Update the `DB_URL` in your environment accordingly.

## Frontend Deployment

### Client Interface
1. Navigate to `frontend/client`
2. Build the production version:   ```bash
   npm run build   ```
3. Serve the static files using a customizable server (e.g., Nginx, or integrate with FastAPI StaticFiles).

### Admin Interface
1. Navigate to `frontend/admin`
2. Build the production version:   ```bash
   npm run build   ```
3. Serve the admin build folder using a static file server.

## Additional Security and Performance Considerations
- **CORS:** Ensure that the CORS middleware in FastAPI is configured properly for production.
- **HTTPS:** Serve all endpoints over HTTPS to secure the data.
- **Reverse Proxy:** Consider using Nginx or Apache as a reverse proxy to improve performance and security.
- **Logging & Monitoring:** Set up proper logging and error monitoring using your preferred tools. 