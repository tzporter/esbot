# ESBot - Project Task Breakdown

**Version:** 0.1.0
**Date:** 2026-03-28

This document breaks down the implementation plan into actionable tasks assigned to specific team members.

---

### **Task Area: Database & Containerization**

- **Assignee:** Truman
- **Objective:** Establish the foundational data layer for the application.

| Task ID | Description                                                                                                                                                                     | Priority | Status      |
| :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------- | :---------- |
| `DB-01` | Create a `docker-compose.yml` file to define the PostgreSQL service. Ensure it includes a persistent volume for data storage.                                                   | High     | Not Started |
| `DB-02` | Define the database schema for `ChatHistory`. The table should include columns for `id` (primary key), `session_id`, `timestamp`, `actor` (e.g., 'user', 'bot'), and `message`. | High     | Not Started |
| `DB-03` | Write a script or document the process for initializing the database schema upon the first run.                                                                                 | Medium   | Not Started |
| `DB-04` | Provide the necessary connection URI and credentials (via environment variables) to the backend team (Zeynep and Sena).                                                         | High     | Not Started |

---

### **Task Area: Backend Development**

- **Assignees:** Zeynep and Sena
- **Objective:** Develop the core application logic and API endpoints.

| Task ID | Description                                                                                                                                                  | Priority | Status      |
| :------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :---------- |
| `BE-01` | Initialize the FastAPI project structure. Set up virtual environment and initial dependencies (`fastapi`, `uvicorn`, `pydantic`).                            | High     | Not Started |
| `BE-02` | Implement a database module to connect to Truman's PostgreSQL container. This should handle database sessions and connections.                               | High     | Not Started |
| `BE-03` | Create the Pydantic models for API request and response bodies (e.g., `ChatMessage`, `ChatRequest`).                                                         | High     | Not Started |
| `BE-04` | Develop the `/chat` endpoint. This endpoint will receive POST requests from the frontend, containing the user's message.                                     | High     | Not Started |
| `BE-05` | Implement the logic within the `/chat` endpoint to read from and write to the `ChatHistory` table in the PostgreSQL database.                                | High     | Not Started |
| `BE-06` | Create a service module to integrate with the external Groq API. This module should handle API key management securely (via environment variables).          | High     | Not Started |
| `BE-07` | Integrate the Groq API service into the `/chat` endpoint. Construct the prompt using user input and chat history, send it to Groq, and process the response. | High     | Not Started |
| `BE-08` | Develop a `/history/{session_id}` endpoint that allows the frontend to retrieve all messages for a given session.                                            | Medium   | Not Started |

---

### **Task Area: Frontend Development**

- **Assignee:** Melek
- **Objective:** Create the user-facing chat interface.

| Task ID | Description                                                                                                                                             | Priority | Status      |
| :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------ | :------- | :---------- |
| `FE-01` | Set up the initial Streamlit application file and basic project structure.                                                                              | High     | Not Started |
| `FE-02` | Build the main chat interface using Streamlit's `st.chat_input` for user entry and `st.chat_message` to display the conversation history.               | High     | Not Started |
| `FE-03` | Implement Streamlit's session state to manage the chat history on the client side for the duration of the session.                                      | High     | Not Started |
| `FE-04` | Write a client-side function to send the user's message to the backend's `/chat` endpoint (POST request).                                               | High     | Not Started |
| `FE-05` | Implement the logic to handle the response from the backend and display the bot's message in the chat interface.                                        | High     | Not Started |
| `FE-06` | Implement a function to call the `/history/{session_id}` endpoint when the app loads to populate the chat with previous messages, ensuring persistence. | Medium   | Not Started |
| `FE-07` | Add basic error handling to inform the user if the backend is unavailable or an error occurs.                                                           | Medium   | Not Started |
