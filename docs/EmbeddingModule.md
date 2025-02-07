---
layout: default
title: "Embedding Module"
---

# Embedding Module Documentation

The embedding module is responsible for processing educational documents and creating text embeddings to enable context‐aware search and retrieval.

## Key Components

### embed.py
- **Embedder Class:**  
  - **Purpose:**  
    - Provides a FastAPI router with endpoints to embed uploaded files and manage associated documents.
  - **Initialization:**  
    - Sets up logging and instantiates a persistent Chroma client.
  - **Core Methods:**
    - `embed_file`: 
      - Reads uploaded files; uses different extraction algorithms for PDFs and PPTXs.
      - Splits extracted text into chunks (using the `RecursiveCharacterTextSplitter`).
      - Adds the text chunks to the vector store and records metadata in the database.
    - `list_documents`: Retrieves documents based on course details.
    - `delete_document`: Deletes a document (removing both file and vector store entries).
    - `search_documents`: Serves the document for download based on its type.
  
### util.py
- **pdf_extraction_alg:**  
  - Reads the PDF file, saves it locally, and extracts text from each page.
- **pptx_extraction_alg:**  
  - Processes PPTX files by iterating through slides and shapes to extract text.
  
### Chroma Vector Store Integration
- Uses the persistent client from `chromadb` to store and query document embeddings, facilitating semantic search within educational documents. 