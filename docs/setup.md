# ESBot Setup and Configuration

## Backend Configuration

### Environment Setup
Make sure you have Docker and Docker Compose installed. (https://www.docker.com/get-started/)

### Installation and running
You can install and run the application via `Docker`. Run the following command in the `.devcontainer` directory:
```bash
docker compose up -d --build
```

If there are any errors, ensure docker is running and that you have enough permissions to run docker commands. You can check if docker is running by running the following command:
```bash
docker ps
```

## Unit Testing & Smoke Tests

The backend uses `pytest` and `fastapi.testclient.TestClient` for testing functionality. To run the tests, use the following command:
```bash
docker compose exec backend pytest tests/
```

### Isolated Test Profile
Unit and integration tests are configured with an isolated "test profile". They bypass the production database variables and utilize an in-memory SQLite database (`sqlite://`) to ensure zero-dependency, fast, reproducible test execution.