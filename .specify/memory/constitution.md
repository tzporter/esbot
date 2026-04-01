# ESBot Project Constitution

This constitution defines the foundational principles, architecture, technology stack, and development rules for the ESBot project.

## 1. Core Principles

- **Language:** Python is the only supported implementation language for application code and documentation.
- **Architecture:** Follow a strict 3-tier architecture with an external AI inference layer:
  - **Presentation Tier:** Streamlit frontend for user interaction.
  - **Application Tier:** FastAPI backend for request handling and business logic.
  - **Data Tier:** PostgreSQL database containerized via Docker for persistence.
  - **AI Inference Layer:** External Groq API for all model-based response generation.
- **Separation of Concerns:** Each tier must implement a clear responsibility boundary and communicate via well-defined interfaces.
- **Specification-Driven Development:** The specification is the primary source of truth. Requirements must be captured in formal documentation before implementation begins.
- **Testability as a First-Class Concern:** Design for dependency injection, mockable AI components, and automated verification from the start.

## 2. Technology Stack

| Layer / Responsibility | Technology                               | Purpose                                                                                           |
| ---------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Language               | Python                                   | Primary language for frontend, backend, and scripting.                                          |
| Presentation Tier      | Streamlit                                | Frontend UI and user interaction layer.                                                           |
| Application Tier       | FastAPI                                  | Backend API, routing, business logic, and integration coordinator.                               |
| Data Tier              | PostgreSQL (Dockerized)                  | Persistent storage for session history, course context, and chat records.                       |
| AI Inference           | Groq API                                 | External AI service for generating answers, explanations, and quiz content.                      |
| Containerization       | Docker / Docker Compose                  | Consistent local and deployment environments for database and service dependencies.               |
| Static Analysis        | SonarQube                                | Continuous static code analysis to enforce code quality, security, and maintainability.           |

## 3. Architectural Guidelines

- **3-Tier Architecture:** The Streamlit frontend must only consume backend APIs. The FastAPI backend must mediate between the frontend, database, and Groq API. The PostgreSQL database must be the single source of persistent state.
- **External AI Layer:** All AI inference must occur through the Groq API. FastAPI constructs prompts, sends them to Groq, receives responses, and persists them as needed.
- **Dependency Injection:** Design backend services so AI clients, database sessions, and external integrations are injected and replaceable for testing.
- **Docker Compose:** Use Docker Compose to define the database and dependent infrastructure, ensuring environments are reproducible across development and CI.
- **Configuration as Code:** Environment-specific settings (DB URIs, API keys, service endpoints) must be managed through environment variables and `.env` files, not embedded in source code.

## 4. Testability Requirements

- **Mockable AI Components:** The Groq integration layer must be abstracted behind an interface so the AI service can be mocked in unit and integration tests.
- **Automated Test Coverage:** Core business flows (chat routing, prompt construction, history persistence, and quiz generation) must be covered by automated tests.
- **Static Code Analysis:** SonarQube must run against Python code to detect bugs, code smells, and security issues before merging changes.
- **Environment Consistency:** Docker Compose must be used in test and development environments to reduce configuration drift.

## 5. Governance

- **Specification First:** Changes to requirements must be captured in the project specification before implementation begins.
- **Review and Approval:** Architecture or process changes to this constitution must be proposed via pull request and approved by project maintainers.
- **Documentation:** All design decisions, environment requirements, and test policies must be documented in English.

**Version:** 1.0.0 | **Ratified:** 2026-04-01
