# Exercise 8 – Mock Testing

## Goal

The goal of this exercise is to practice unit and mock testing techniques within the context of the **ESBot** application. Based on the available code, you will analyze the implementation, derive test scenarios, and implement the missing parts to successfully run the tests.

---

## Background

ESBot follows the structure of a **three-tier architecture** — a widely adopted pattern that separates an application into three distinct layers: the presentation layer, the business logic layer, and the data access layer. This separation of concerns allows for better maintainability, testability, and scalability of the application.

- The **presentation layer** is responsible for handling user interactions, rendering the chat interface, and displaying AI-generated learning content.
- The **business logic layer** (service layer) contains the core functionality of ESBot: managing learning sessions, orchestrating AI inference requests, generating quizzes, and evaluating user answers.
- The **data access layer** (repository layer) manages the interaction with the persistent storage, providing a clean abstraction over the database for domain objects such as sessions and messages.

A key characteristic of ESBot is its integration with an **external AI inference engine** (e.g., Ollama, vLLM, LM Studio). This external dependency introduces non-deterministic behavior and must be isolated during testing using mocking techniques. The service layer therefore acts as an intermediary between the presentation layer, the repository layer, and the AI inference engine.

Testing services and repositories requires different approaches due to their distinct responsibilities and dependencies. The testing strategy should focus on:

- **Unit testing services in isolation** (focus of this exercise)
- **Integration testing repositories with the database** (focus of this exercise)
- End-to-end testing of the complete flow (NOT the focus of this exercise)

---

## Exercise 8.1 (10 Points): Unit Testing of Models

Please review carefully the unit test implementations of your ESBot code repository using your gained knowledge about test design techniques from the lecture (e.g., equivalence class partitioning, boundary value analysis, decision table, etc.).

Focus your review on the domain models relevant to ESBot, including but not limited to:

- `Session` – represents a user's learning session, including timestamps and associated messages
- `Message` – represents a single interaction turn (user input or ESBot response)
- `Quiz` / `Question` – represents a generated practice question with possible answers
- `Answer` – represents a user's submitted answer to a quiz question

For each model, ask yourself:

- Are all valid attribute combinations covered?
- Are boundary values (e.g., empty content, maximum message length, invalid session state) tested?
- Are invalid inputs and edge cases explicitly handled in the tests?

Please describe your approach to how you analyzed your current test implementations and document it in your repository (e.g., as a short written section in this file or a dedicated analysis document).

---

## Exercise 8.2 (10 Points): Service Testing with Mocks

ESBot's service layer is responsible for coordinating the core learning workflow. It interacts with two types of dependencies:

1. The **repository/database/ORM layer** (e.g., `SessionRepository`, `MessageRepository`) for persistent data access
2. The **AI inference service** (e.g., `LLMService` or `AIInferenceClient`) for generating responses, quizzes, and feedback

Implement a `ChatService` (or `LearningSessionService`) that realizes the following functions:

- **Start a new learning session** – creates and persists a new session for a user
- **Send a message and receive a response** – forwards the user's message to the LLM service and stores both the user message and the AI-generated response
- **Generate a quiz** – requests a set of practice questions on a given topic from the LLM service and stores them in the session
- **Evaluate a user answer** – sends the answer along with the original question to the LLM service and returns feedback
- **Handle LLM service failures gracefully** – returns a meaningful fallback response when the AI inference engine is unavailable or returns an error

Next, create a **test suite for the `ChatService`** that verifies the behavior of the described scenarios. For each scenario, you should:

- Set up the necessary mock objects (e.g., mock `SessionRepository`, mock `LLMService`)
- Configure the mock behavior (e.g., stubbing return values, simulating errors)
- Execute the service method under test
- Verify the expected outcomes (e.g., returned response, session state)
- Verify the interactions with the mocked dependencies (e.g., assert that `SessionRepository.save()` was called with the correct arguments)

**Hints:**

- You can use one of the following frameworks to implement mocks (e.g., Python `unittest.mock`, Java Mockito, Jest mocks for TypeScript)
- Pay special attention to the non-deterministic nature of AI responses — your tests should not rely on specific LLM output content, but on the _behavior_ of the service when given a mocked response
- Examples are available at [https://github.com/dgrewe-hse/xyzTesting](https://github.com/dgrewe-hse/xyzTesting)

---

## Exercise 8.3 (10 Points): Repository / Database Testing

The next exercise focuses on testing the repository / database layer that realizes the interaction between the business logic layer and the actual database (e.g., PostgreSQL, SQLite). Implement a `SessionRepository` realizing the following functionality:

- **Creating a new session** – persists a new learning session to the database
- **Finding a session by ID** – retrieves a session by its unique identifier
- **Finding sessions by user** – retrieves all sessions belonging to a specific user
- **Appending a message to a session** – stores a new message (user or bot) linked to an existing session
- **Retrieving the full message history of a session** – returns all messages for a given session in chronological order
- **Updating session metadata** – updates attributes such as the session title or last-activity timestamp
- **Deleting a session** – removes a session and all associated messages from the database

Next, create a **test suite for the `SessionRepository`** that verifies the behavior of the described scenarios. You should:

- Set up an in-memory database or a dedicated test database (e.g., SQLite in-memory, H2, or a test-scoped PostgreSQL container)
- Initialize the test data required for each scenario
- Execute the repository method under test
- Verify the resulting database state (e.g., check that a record was persisted correctly or removed)
- Clean up the test data after each test to ensure test isolation

---

## Exercise 8.4 (10 Points): REST API Controller

The fourth exercise focuses on implementing REST API endpoints as part of ESBot's backend, which serves as the entry point for HTTP requests from the frontend. This exercise serves as the basis for the upcoming week, when we focus on API testing using different tools and techniques. **It is not necessary to implement test cases in this exercise** — but the endpoints will be needed in the following week.

Please implement REST endpoints supporting at least _five_ of the following scenarios:

- **Session creation endpoint** – allows a user to start a new learning session (`POST /sessions`)
- **Message submission endpoint** – allows a user to send a message within a session and receive an AI-generated response (`POST /sessions/{sessionId}/messages`)
- **Session history retrieval endpoint** – returns the full message history of a given session (`GET /sessions/{sessionId}/messages`)
- **Quiz generation endpoint** – triggers the generation of practice questions for a given topic within a session (`POST /sessions/{sessionId}/quiz`)
- **Answer evaluation endpoint** – submits a user's answer to a quiz question and returns feedback (`POST /sessions/{sessionId}/quiz/{questionId}/answer`)
- **Session listing endpoint** – retrieves all sessions for the current user (`GET /sessions`)
- **Session deletion endpoint** – removes a session and its associated data (`DELETE /sessions/{sessionId}`)
- **Error handling and appropriate HTTP response codes** – e.g., `404 Not Found` for unknown sessions, `422 Unprocessable Entity` for invalid input, `503 Service Unavailable` when the LLM inference engine is unreachable
- **Input validation** – reject empty or malformed messages, enforce maximum input lengths, and sanitize user input to mitigate injection risks
