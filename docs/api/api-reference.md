# ESBot API Reference

This document outlines the REST API endpoints for the ESBot application.
All endpoints consume and produce `application/json`.

**Base URL:** `http://localhost:8000/api/v1`

## 1. System Health

### `GET /health`

Liveness check to verify if the API is up and running.

- **Request Body:** None
- **Success Response:**
  - **Code:** `200 OK`
  - **Content:** `{"status": "ok", "service": "esbot-backend"}`
- **Error Response:** None expected unless the server is down (`502/503`).

## 2. Session Management

### `POST /sessions`

Creates a new learning session for the user.

- **Request Body:** None (or user ID if authentication is implemented)
- **Success Response:**
  - **Code:** `201 Created`
  - **Content:** `{"session_id": 123, "created_at": "2026-05-15T10:00:00Z"}`

### `GET /sessions`

Retrieves a list of all active sessions for the current user.

- **Parameters:** `user_id` (Query parameter, optional depending on auth)
- **Success Response:**
  - **Code:** `200 OK`
  - **Content:** `[ {"session_id": 123, "created_at": "2026-05-15T10:00:00Z"}, ... ]`

### `DELETE /sessions/{sessionId}`

Removes a specific session and all its associated data (messages, quizzes).

- **Path Parameter:** `sessionId` (integer)
- **Success Response:**
  - **Code:** `204 No Content`
- **Error Responses:**
  - **Code:** `404 Not Found` (If session does not exist)

## 3. Messaging

### `POST /sessions/{sessionId}/messages`

Allows a user to send a message within a session and triggers an AI-generated response.

- **Path Parameter:** `sessionId` (integer)
- **Request Body:** ```json
  {
  "content": "Can you explain polymorphism in Python?"
  }
