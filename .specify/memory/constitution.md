# ESBot Project Constitution

## 1. Core Principles & Rules

- **Language**: All code and documentation must be in English.
- **Architecture**: The project will follow a 3-layered architecture:
  - **Presentation Layer (Frontend)**
  - **Application Layer (Backend)**
  - **Data Layer (Database)**
- **Modularity**: Components should be designed to be modular and reusable.
- **Clarity**: Code must be clear, well-documented, and maintainable.
- **Testing**: Test-Driven Development (TDD) is encouraged to ensure software quality.

## 2. Technology Stack

| Layer/Component  | Technology                       | Description                                                                                 |
| ---------------- | -------------------------------- | ------------------------------------------------------------------------------------------- |
| **Language**     | **Python**                       | The primary programming language for both backend and frontend development.                 |
| **Frontend**     | **Streamlit**                    | The framework for building the user interface (Presentation Layer).                         |
| **Backend**      | **FastAPI**                      | The web framework for building the API and business logic (Application Layer).              |
| **Database**     | **PostgreSQL** (with **Docker**) | The relational database for data storage (Data Layer), containerized for consistency.       |
| **AI Inference** | **Groq API**                     | The service for performing AI model inference, providing the core intelligence for the bot. |

## 3. Architectural Guidelines

- **Layered Architecture**: Strictly adhere to the 3-layered architecture. The Presentation Layer (Streamlit) communicates with the Application Layer (FastAPI) via a RESTful API. The Application Layer handles business logic and interacts with the Data Layer (PostgreSQL).
- **API-First Design**: The FastAPI backend will expose a well-defined RESTful API. This API is the single source of truth for all client interactions.
- **Containerization**: All services, especially the PostgreSQL database, must be containerized using Docker to ensure a consistent and reproducible environment.
- **Configuration Management**: Application configuration (e.g., database URIs, API keys) must be managed through environment variables, not hard-coded in the source.

## 4. Governance

- This constitution is the guiding document for all technical decisions within the ESBot project.
- Amendments to this constitution must be proposed via a pull request and receive approval from the project maintainers.
