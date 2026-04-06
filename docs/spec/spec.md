# ESBot - Software Requirements Specification

**Version:** 0.2.0
**Date:** 2026-04-01

## 1. Problem Space

General-purpose chatbots are typically unstructured, not grounded in course material, and do not provide immediate pedagogical feedback. ESBot is designed to solve these gaps by delivering course-grounded explanations, example generation, dynamic practice, and answer evaluation in an educational chat interface.

## 2. System Overview

ESBot is an educational conversational system with a 3-tier architecture and an external AI inference layer.

- **Presentation Tier:** Streamlit frontend for student interaction through plain text input and output.
- **Application Tier:** FastAPI backend for request routing, business logic, prompt construction, and orchestration.
- **Data Tier:** Dockerized PostgreSQL for persistent session history, source content, and evaluation records.
- **AI Inference Layer:** Groq API for generating grounded explanations, examples, quizzes, and feedback.

## 3. Functional Requirements

### FR-1: Conversational Learning Interface

- The system must provide a chat-style interface with plain text input and plain text output.
- Session history must be persisted in PostgreSQL and retrievable across user visits.
- Users must be able to continue a previous conversation and view prior exchanges.

### FR-2: Explanation and Example Generation

- The system must generate explanations grounded in course material stored in PostgreSQL.
- When a student asks a question, the backend must retrieve relevant content, construct a grounded prompt, and send it to the Groq API.
- The returned response must include both explanation and at least one contextual example when appropriate.

### FR-3: Dynamic Quiz Generation

- The system must generate short practice quizzes on demand using course content as the basis.
- Each quiz must contain dynamically generated questions and answer options, with clear instructions for the student.
- The backend must use the Groq API to produce quiz content derived from the stored course material.

### FR-4: Answer Evaluation and Pedagogical Feedback

- The system must evaluate student answers to generated quiz questions.
- The backend must compare student responses to correct answers and provide pedagogical feedback through the Groq API.
- Feedback should indicate correctness, explain mistakes, and suggest areas for review.

## 4. Quality Model (ISO 25010)

### 4.1. Usability

- **ID:** QM-001
- **Characteristic:** Learnability
- **Requirement:** The first successful interaction must occur within 60 seconds for a new student using the Streamlit interface.
- **Rationale:** Students should be able to start learning immediately without onboarding friction.

### 4.2. Performance Efficiency

- **ID:** QM-002
- **Characteristic:** Time Behavior
- **Requirement:** 95% of queries must receive a response within 2-5 seconds under a load of 50 concurrent users.
- **Rationale:** Fast responses keep learners engaged and support real-time study sessions.

### 4.3. Security

- **ID:** QM-003
- **Characteristic:** Integrity & Authenticity
- **Requirement:** The system must block 100% of unauthorized data access and mitigate at least 99% of prompt injection attempts.
- **Rationale:** Student data and course content must remain secure, and AI prompts must not be manipulated to return untrusted or unrelated outputs.

### 4.4. Functional Suitability

- **ID:** QM-004
- **Characteristic:** Functional Suitability
- **Requirement:** At least 98% of AI responses must be consistent with source documents stored in PostgreSQL.
- **Rationale:** Grounded answers are essential to maintain instructional accuracy and trust.

## 5. Additional Constraints

- All user-facing text and documentation must be in English.
- The backend must use dependency injection for the AI integration layer to support testing and mocking.
- The system must be deployed with Docker Compose to ensure consistent environments.
- Static code analysis should be integrated as part of the development process to maintain quality.
