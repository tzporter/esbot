# ESBot Quality Management Plan
This document defines the quality attributes for ESBot based on the ISO/IEC 25010 standard and outlines the technical measures taken during development to ensure high software quality and testability.

## 1. Selected Quality Models
Following the 3-steps approach, we have identified the following models:

### Model 1: Usability (*NFR-7.1*)
| Level | Description |
| :--- | :--- |
| **Abstract** | **Usability**: Degree to which a product can be used by specified users. |
| **Specific** | **Learnability**: Ease of learning for first-time students. |
| **Measurable** | **Target**: First successful interaction within < 60 seconds. |

### Model 2: Performance Efficiency (*NFR-8.1, NFR-8.2*)
| Level | Description |
| :--- | :--- |
| **Abstract** | **Performance Efficiency**: Performance relative to the amount of resources used under stated conditions. |
| **Specific** | **Time Behaviour**: The degree to which the response and processing times of ESBot meet requirements when performing its functions. |
| **Measurable** | **Target**: 95% of queries must be responded to within a 2–5 second timeframe under a load of up to 50 concurrent users. |

### Model 3: Security *(NFR-10.1, NFR-10.2, NFR-10.3)*
| Level | Description |
| :--- | :--- |
| **Abstract** | **Security**: The degree to which the system protects data so that the users have access appropriate to their authorization levels. |
| **Specific** | **Integrity & Authenticity**: Ensuring students can only access their own session history and preventing system manipulation via malicious "prompt injection". |
| **Measurable** | **Target**: 100% of unauthorized data access attempts must be blocked; 99% of known prompt injection techniques must be successfully mitigated in penetration tests. |

### Model 4: Functional Suitability (*FR-2.2, FR-2.4, NFR-13.1*)
| Level | Description |
| :--- | :--- |
| **Abstract** | **Functional Suitability**: Degree to which a product or system provides functions that meet stated and implied needs when used under specified conditions. |
| **Specific** | **Functional Correctness (AI Accuracy)**: The system's ability to provide accurate answers based solely on provided course materials, preventing AI hallucinations. |
| **Measurable** | **Target**: A minimum of 98% consistency between the AI's generated response and the source document; unverifiable responses must be filtered before presentation. |

## Testability Measures for ESBot
These measures directly address the Maintainability and Testability 
requirements (NFR-11.1–11.3) as defined in the requirements specification.

To ensure ESBot meets Testability standards, the following measures are proposed:

### 1. Architectural Measures (Structural Testability)

- **Modular Three-Tier Separation:** By strictly separating the Presentation, Application, and Data layers, we ensure that each component can be tested in isolation (Unit Testing) without side effects from other layers.
- **Dependency Injection for AI Inference:** The system is designed to support the mocking of AI inference components. This allows developers to simulate various LLM responses, including edge cases and errors, without incurring API costs or latency during automated testing.
- **RESTful API Design:** The backend follows the REST architectural style, providing clear, versioned endpoints that can be easily validated using automated tools like JMeter or Postman.

### 2. Technical and Tooling Strategy

- **Containerization with Docker:** Using Docker Compose ensures that the development, testing, and production environments are identical. This eliminates "environment-specific" bugs and guarantees that tests are reproducible across all team members' machines.
- **Automated Testing Frameworks:**
  - **Unit Testing:** Implementation of JUnit for backend logic verification to ensure individual functions perform as expected.
  - **End-to-End (E2E) Testing:** Utilization of Cypress or Selenium to automate the user chat flow, ensuring the frontend correctly displays messages and maintains session continuity.
- **Static Code Analysis:** Integration of SonarQube to monitor code complexity and maintainability. High-quality, clean code is inherently easier to test and debug.

### 3. Process-Driven Measures (SDD Approach)

- **Spec-First Development:** Precise, versioned specifications act as the primary "Source of Truth". By defining behavior and acceptance criteria before coding, test cases become a natural by-product of the requirements.
- **Requirements Traceability:** Every functional requirement (e.g., 
Requirement 1.1: Plain text input) would be mapped back to specific 
test cases, aiming for full coverage and preventing "feature drift."
- **AI Output Validation:** Since AI is non-deterministic, the system implements response validation to manage outputs. This allows the test suite to verify if the AI's output meets pedagogical and safety constraints before it is presented to the student.

### 4. Observability and Diagnostics

- **Logging and Monitoring:** The system provides comprehensive logging capabilities to trace system behavior. In the event of a test failure, these logs allow for rapid Analyzability to identify the root cause of the defect.
- **State Persistence Testing:** Specific tests are designed to verify that the Data Layer correctly stores and fetches interactions in chronological order, ensuring the "Persistence of Learning Context" requirement is met.
