# ESBot API Reference

This document outlines the REST API endpoints for the ESBot application.
All endpoints consume and produce `application/json`.

**Base URL:** `http://localhost:8000/api/v1`

---

## Setup Instructions

To run the ESBot API locally for testing, follow these steps:

1.  **Navigate to the backend directory:**

        cd backend

2.  **Install dependencies:**

        pip install -r requirements.txt

3.  **Configure Environment Variables:**
    For API testing, run the LLM in mock mode to ensure deterministic responses and avoid external API costs.

         export LLM_PROVIDER=mock
         export GROQ_API_KEY=mock_key

    _(On Windows PowerShell, use `$env:LLM_PROVIDER="mock"`)_

4.  **Start the backend server:**

        uvicorn main:app --reload --port 8000

5.  **Verify health:**
    Navigate to `http://localhost:8000/api/v1/health` in your browser or use curl to confirm the server is running.

---

## Standard Error Responses

As per standard REST conventions, the API returns specific JSON structures for errors. Here are the expected response bodies for common error codes:

- **`404 Not Found`** (e.g., Session or Quiz item does not exist)

        {
          "detail": "Resource not found."
        }

- **`422 Unprocessable Entity`** (e.g., Missing required fields or validation failure)

        {
          "detail": [
            {
              "loc": ["body", "content"],
              "msg": "field required",
              "type": "value_error.missing"
            }
          ]
        }

- **`500 Internal Server Error`** (e.g., Database connection failure or unhandled exception)

        {
          "detail": "Internal Server Error."
        }

---

## 1. System Health

### `GET /health`

Liveness check to verify if the API is up and running.

- **Request Body:** None
- **Success Response:**
  - **Code:** `200 OK`
  - **Content:**

        {
          "status": "ok",
          "service": "esbot-backend"
        }

---

## 2. Session Management

### `POST /sessions`

Creates a new learning session for the user.

- **Request Body:** None
- **Success Response:**
  - **Code:** `201 Created`
  - **Content:**

        {
          "session_id": 123,
          "created_at": "2026-05-15T10:00:00Z"
        }

### `GET /sessions`

Retrieves a list of all active sessions for the current user.

- **Parameters:** `user_id` (Query parameter)
- **Success Response:**
  - **Code:** `200 OK`
  - **Content:**

        [
          {
            "session_id": 123,
            "created_at": "2026-05-15T10:00:00Z"
          }
        ]

### `DELETE /sessions/{sessionId}`

Removes a specific session and all its associated data (messages, quizzes).

- **Path Parameter:** `sessionId` (integer)
- **Success Response:**
  - **Code:** `204 No Content`

---

## 3. Messaging

### `POST /sessions/{sessionId}/messages`

Allows a user to send a message within a session and triggers an AI-generated response.

- **Path Parameter:** `sessionId` (integer)
- **Request Body:**

        {
          "content": "Can you explain polymorphism in Python?"
        }

- **Success Response:**
  - **Code:** `201 Created`
  - **Content:**

        {
          "role": "assistant",
          "content": "Polymorphism allows objects of different types to be treated uniformly..."
        }

### `GET /sessions/{sessionId}/messages`

Returns the full message history of a given session.

- **Path Parameter:** `sessionId` (integer)
- **Success Response:**
  - **Code:** `200 OK`
  - **Content:**

        [
          {"role": "user", "content": "Hello", "timestamp": "2026-05-15T10:01:00Z"},
          {"role": "assistant", "content": "Hi there! How can I help?", "timestamp": "2026-05-15T10:01:05Z"}
        ]

---

## 4. Quiz Management

### `POST /sessions/{sessionId}/quiz`

Triggers the generation of practice questions for a given topic within a session.

- **Path Parameter:** `sessionId` (integer)
- **Request Body:**

        {
          "topic": "Software Testing"
        }

- **Success Response:**
  - **Code:** `201 Created`
  - **Content:**

        {
          "quiz_id": 456,
          "topic": "Software Testing",
          "questions": [
            {"id": 1, "question": "What is unit testing?"},
            {"id": 2, "question": "Explain integration testing."}
          ]
        }

### `POST /sessions/{sessionId}/quiz/{questionId}/answer`

Submits a user's answer to a specific quiz question and returns AI evaluation/feedback.

- **Path Parameters:** `sessionId` (integer), `questionId` (integer)
- **Request Body:**

        {
          "answer": "Testing individual components in isolation."
        }

- **Success Response:**
  - **Code:** `200 OK`
  - **Content:**

        {
          "is_correct": true,
          "feedback": "Great job! That is exactly what unit testing is."
        }

Google Gemini was used to help writing this part of the exercise and all content was thoroughly checked.
