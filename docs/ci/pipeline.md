# CI Pipeline Design

This document explains the configuration choices made for our basic Continuous Integration pipeline (`.github/workflows/ci.yml`).

## 1. Triggers
The workflow triggers on `push` and `pull_request` to ensure that every contribution and code change is automatically verified before it can be merged into the default branch. This is the foundation of a healthy CI pipeline. Additionally, `workflow_dispatch` was included to allow developers to trigger the pipeline manually if needed.

## 2. Runner
We are using `ubuntu-latest`. It is the industry standard. it is lightweight, fast, and familiar. It is also similar to our docker container's ubuntu image.

## 3. Environment
Our application uses Python 3.11 (as defined in our `backend/Dockerfile`). The pipeline utilizes `actions/setup-python@v5` configured with `python-version: '3.11'` to match our exact runtime environment. We chose this over our docker container image to reduce overhead and speed up the pipeline execution time.

## 4. Jobs and Steps
We have one unified job `test-and-lint` which performs the following:
*   **Checkout code:** Grabs the repository context.
*   **Install dependencies:** Installs the core packages as well as development tools directly via `pip install -r backend/requirements.txt`.
*   **Run Linters:** uses  `ruff` to catch style issues and unused imports, and `bandit` for security scanning. We exclude the `features/` directory from `bandit` to prevent false positive warnings on our `assert` statements.
*   **Run Unit Tests:** Runs `pytest` in the `backend/` directory.
*   **Run BDD Tests:** Runs `behave` in the `backend/` directory.

**What is out of scope for CI:** 
We intentionally mock the AI provider to prevent making live, non-deterministic requests to external LLM APIs. We are also using our in-memory SQLite database for testing instead of a full PostgreSQL database container, optimizing for speed while testing our ORM logic.

## 5. Parity with Local
Locally, we use `docker compose run --rm backend <command>` (as documented in `local-verification.md`) to verify our changes within our Docker container.

In CI, we use native `actions/setup-python` directly on the runner to save the overhead of building a Docker image on every single pull request, reducing our feedback loop time. Because both our Dockerfile and the CI runner use Python 3.11, and both install dependencies from `requirements.txt`, we ensure environmental parity. If CI fails natively but passes locally (or vice-versa), we should look closely at dependency drift.


# this document was edited with AI. All edits were thoroughly checked by humans.