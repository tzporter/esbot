<!-- This file was created with AI assistance. AI was used to draft the
documentation of the combined test-suite command and to check consistency
with the actual backend project structure. -->

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

## Running the Test Suite

ESBot has two layers of automated tests:

1. **Unit tests** (`pytest`) — test individual domain entities and API
   behaviour in isolation, using an in-memory SQLite database.
2. **BDD / acceptance tests** (`behave`) — test end-to-end user flows
   described in Gherkin `.feature` files. The AI provider is mocked in the
   step definitions, so these tests are deterministic and run offline.

### Run everything (recommended)

From the `backend/` directory, run both test layers with a single command:

```bash
pytest tests/ && behave features/
```

The `&&` ensures that `behave` only runs if `pytest` passes, so failures in
either layer stop the build.

Inside the Docker environment, the equivalent command is:

```bash
docker compose exec backend bash -c "pytest tests/ && behave features/"
```

### Run only unit tests

```bash
pytest tests/
```

### Run only BDD/acceptance tests

```bash
behave features/
```

You can also run a single feature file, for example:

```bash
behave features/ask_question.feature
```

### Isolated Test Profile

Unit and integration tests are configured with an isolated "test profile".
They bypass the production database variables and utilise an in-memory SQLite
database (`sqlite://`) to ensure zero-dependency, fast, reproducible test
execution.

For BDD tests, the AI inference service is replaced with a mock in each step
definition (see `backend/features/steps/`). This keeps acceptance tests
deterministic and means no API key or network access is required to run them.

## Test Strategy

For a discussion of *when* unit tests and BDD tests should run in the CI
pipeline, see [`docs/spec/test-strategy.md`](spec/test-strategy.md).
