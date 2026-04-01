# ESBot - Implementation and Architectural Plan

**Version:** 0.2.0
**Date:** 2026-04-01

## 1. Introduction

This document defines the ESBot architectural plan and implementation strategy. The goal is to deliver a structured educational chat system with a clear separation of responsibilities, secure persistence, grounded AI inference, and robust testing and observability.

## 2. Architectural Overview

ESBot is built as a 3-tier application with an external AI inference layer. Each layer has a specific role and communicates through well-defined interfaces.

### 2.1. Presentation Layer (Streamlit)

- Captures user input through plain text fields.
- Displays chronological chat history in a conversational format.
- Provides controls for actions like asking questions, generating quizzes, and submitting answers.
- Calls the FastAPI RESTful backend for every interaction.

### 2.2. Application Layer (FastAPI)

- Exposes RESTful endpoints for chat interactions, quiz generation, and history retrieval.
- Handles business logic, session management, and validation of AI outputs.
- Reads and writes session history to PostgreSQL.
- Validates Groq API responses against source material and application rules before returning them to the frontend.
- Ensures functional sustainability by rejecting or sanitizing unsafe or inconsistent AI responses.

### 2.3. Data Layer (PostgreSQL)

- Persistently stores all user interactions, chat records, quiz attempts, and source content.
- Enforces secure data isolation by session and user identifier.
- Supports retrieval of contextual information for grounded responses and explanations.
- Runs in Docker to guarantee consistent development and deployment environments.

### 2.4. AI Inference Layer (Groq API)

- Generates contextual explanations, examples, quizzes, and answer evaluation feedback.
- Receives prompts constructed by FastAPI with grounded course material and session history.
- Returns structured responses that the backend can validate and persist.

### 2.5. Testing & Observability Architecture

- **Automated Unit Testing:** Write unit tests for business logic, prompt construction, validation, and persistence layers. Use Python test frameworks and JUnit-style structure where applicable for shared conventions.
- **End-to-End Testing:** Use Cypress or Selenium to validate user flows from Streamlit through FastAPI to the database and back.
- **Logging:** Implement structured request/response logging in FastAPI, including AI call metadata, validation decisions, and persistence events.
- **Monitoring:** Capture key metrics such as response time, error rates, session throughput, and AI validation failures.
- **Error Diagnostics:** Ensure logs contain enough context to trace failed messages, invalid AI outputs, and database issues quickly.

## 3. Data Flow

1. Student enters a question or quiz request in the Streamlit UI.
2. Streamlit sends a POST request to the FastAPI backend.
3. FastAPI loads session history and relevant course content from PostgreSQL.
4. FastAPI constructs a grounded prompt and sends it to the Groq API.
5. Groq API returns a generated response.
6. FastAPI validates the response, persists the interaction, and returns the validated result to Streamlit.
7. Streamlit displays the response and updates the chronological chat history.

## 4. Implementation Phases

### Phase 1: Presentation Layer

- Build the Streamlit app to capture plain text input and render sequential chat history.
- Implement session-specific state and UI controls for quizzes and answer submission.
- Connect UI actions to FastAPI endpoints.

### Phase 2: Application Layer

- Implement RESTful API endpoints for `/chat`, `/quiz`, `/history`, and `/evaluate`.
- Add session management and request validation.
- Integrate prompt construction, Groq API client, and AI response validation.
- Ensure AI outputs are checked before being returned to the frontend.

### Phase 3: Data Layer

- Dockerize PostgreSQL and define schema for sessions, chat_history, course_content, quiz_items, and evaluations.
- Implement data isolation per user/session.
- Create persistence logic in FastAPI for all interactions.

### Phase 4: Testing & Observability

- Add automated unit tests for backend services, AI prompt builders, and validation layers.
- Define end-to-end tests covering the full Streamlit → FastAPI → PostgreSQL → Streamlit path.
- Implement structured logging and monitoring metrics for response latency, error conditions, and validation events.

## 5. Governance and Sustainability

- Maintain the architectural plan as the source of truth for integration decisions.
- Use Docker Compose for reproducible local and CI environments.
- Enforce validation of AI output to preserve instructional accuracy and avoid unsafe responses.
- Monitor system health continuously and use alerts to catch regressions or service degradation early.
