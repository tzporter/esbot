# ESBot - Project Task Breakdown

**Version:** 0.2.0
**Date:** 2026-04-01

This document breaks down the ESBot implementation into team-specific tasks with a focus on user learnability, backend validation, and consistent containerized environments.

---

### **Task Area: Database & Containerization**

- **Assignee:** Truman
- **Objective:** Build the persistent data foundation and ensure identical development/test environments.

| Task ID | Description                                                                                                                        | Priority | Status      |
| :------ | :--------------------------------------------------------------------------------------------------------------------------------- | :------- | :---------- |
| `DB-01` | Define PostgreSQL schemas for session tracking, chat history, course content, quiz items, and evaluation records.                  | High     | Not Started |
| `DB-02` | Create a `docker-compose.yml` configuration for PostgreSQL and any needed supporting services.                                     | High     | Not Started |
| `DB-03` | Configure Docker Compose to support both development and test environments with the same service definitions and network settings. | High     | Not Started |
| `DB-04` | Implement secure environment variable handling for database credentials, connection URIs, and service ports.                       | High     | Not Started |
| `DB-05` | Document database initialization, migration, and cleanup procedures for the team.                                                  | Medium   | Not Started |

---

### **Task Area: Backend Development**

- **Assignees:** Zeynep and Sena
- **Objective:** Build the FastAPI backend, Groq integration, and validation/test infrastructure.

| Task ID | Description                                                                                                                                      | Priority | Status      |
| :------ | :----------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :---------- |
| `BE-01` | Initialize the FastAPI service with dependency injection support for the AI client, database session, and configuration.                         | High     | Not Started |
| `BE-02` | Build RESTful endpoints including `/chat`, `/quiz`, `/history/{session_id}`, and `/evaluate`.                                                    | High     | Not Started |
| `BE-03` | Implement Groq API integration behind an injectable service interface and manage API keys securely via environment variables.                    | High     | Not Started |
| `BE-04` | Add prompt construction logic that combines user input, stored course context, and session history for grounded AI responses.                    | High     | Not Started |
| `BE-05` | Implement AI output validation rules to detect inconsistencies, unsafe content, and prompt injection before returning responses to the frontend. | High     | Not Started |
| `BE-06` | Persist all interactions and AI outputs to PostgreSQL, ensuring data isolation by session and user identifier.                                   | High     | Not Started |
| `BE-07` | Create JUnit-style test suites with mocked AI responses to verify prompt construction, response handling, validation, and persistence behavior.  | High     | Not Started |
| `BE-08` | Develop test fixtures to simulate the Groq API and PostgreSQL dependencies for isolated backend testing.                                         | Medium   | Not Started |

---

### **Task Area: Frontend Development**

- **Assignee:** Melek
- **Objective:** Deliver the Streamlit interface and supporting end-to-end tests aligned to the learnability quality goal.

| Task ID | Description                                                                                                                                                     | Priority | Status      |
| :------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :---------- |
| `FE-01` | Build the Streamlit web UI with plain text input/output, chat history rendering, and controls for asking questions, generating quizzes, and submitting answers. | High     | Not Started |
| `FE-02` | Implement chronological chat history display that updates in real time and supports session restoration when a user returns.                                    | High     | Not Started |
| `FE-03` | Ensure the UI supports the < 60 second learnability goal through clear layout, minimal required actions, and contextual prompts.                                | High     | Not Started |
| `FE-04` | Connect Streamlit actions to the FastAPI REST endpoints and handle success/error flows cleanly.                                                                 | High     | Not Started |
| `FE-05` | Create end-to-end tests using Selenium or Cypress that simulate student interactions from login through chat, quiz generation, and response display.            | High     | Not Started |
| `FE-06` | Validate that the frontend presents meaningful feedback for backend errors, invalid AI responses, or connectivity problems.                                     | Medium   | Not Started |
| `FE-07` | Document the frontend usage pattern and the onboarding path for new students to support rapid adoption.                                                         | Medium   | Not Started |

---

### **Task Area: Cross-Team Quality & Delivery**

- **Assignees:** All team members
- **Objective:** Ensure the system is testable, reliable, and maintainable across development and deployment.

| Task ID | Description                                                                                                                                                             | Priority | Status      |
| :------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :---------- |
| `QT-01` | Define shared API contracts and data schemas for chat messages, quizzes, and evaluation results.                                                                        | High     | Not Started |
| `QT-02` | Establish a shared Docker Compose workflow for local development and CI that uses the same PostgreSQL service definitions and environment variables.                    | High     | Not Started |
| `QT-03` | Agree on a testing approach: unit tests for backend logic, JUnit-style structure for test organization, and E2E tests for UI workflows.                                 | High     | Not Started |
| `QT-04` | Implement structured logging and monitoring points in the backend so validation failures, AI integrations, and persistence errors are diagnosable via logs and metrics. | Medium   | Not Started |
| `QT-05` | Plan a sprint review to validate the first end-to-end flow: Streamlit → FastAPI → PostgreSQL → Groq API → Streamlit.                                                    | Medium   | Not Started |
