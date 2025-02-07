---
layout: default
title: "Database"
---

# Database Schema Documentation

The TeachGPT system uses SQLAlchemy to define its data models. The following tables are used to store users, courses, documents, and chat histories.

## User
- **Table Name:** users
- **Description:** Stores details of registered users.
- **Key Fields:**
  - `id` (String, Primary Key): Unique identifier.
  - `name` (String): User's full name.
  - `email` (String, Unique): User's login email.
  - `hashed_password` (String): Hashed password for authentication.
  - `department` (String)
  - `year` (String)
  - _Additional fields as needed (e.g., gender)._

## Course
- **Table Name:** courses
- **Description:** Contains course information.
- **Key Fields:**
  - `id` (String, Primary Key): Course code.
  - `subject_name` (String): Name of the course.

## Document
- **Table Name:** documents
- **Description:** Holds metadata about documents uploaded for embedding.
- **Key Fields:**
  - `id` (String, Primary Key): Unique document identifier.
  - `added_at` (DateTime): Timestamp when the document was added.
  - `user_id` (String, ForeignKey): ID of the uploader.
  - `course_code` (String, ForeignKey): Associated course.
  - `document_name` (String): Name of the file.

## Chat & ChatMessage
- **Tables:** chats, chat_messages
- **Chat:**
  - `id` (String, Primary Key)
  - `time` (DateTime): Timestamp of the chat session.
  - `description` (String): Description of the chat.
  - `user_id` (String, ForeignKey)
- **ChatMessage:**
  - `id` (String, Primary Key)
  - `created_at` (DateTime): When the message was sent.
  - `chat_id` (String, ForeignKey): Associated chat session.
  - `message` (Text): Chat content.
  - `from_user` (Boolean): Marks if the message came from the user.
  - `is_opener` (Boolean): Flags initial or system messages. 