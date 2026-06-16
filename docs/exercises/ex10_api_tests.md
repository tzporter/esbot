# Exercise 10 – API Testing

## Goal

The goal of this exercise is to systematically test the **ESBot** REST API using a combination of manual tooling, automated test frameworks, and performance/load testing tools. You will validate correct behavior, error handling, and the scalability characteristics of the API you implemented in Exercise 8.4.

---

## Background

ESBot exposes a REST API that acts as the gateway between the frontend and the backend services. Clients interact with the system exclusively through this interface — creating learning sessions, exchanging messages with the AI tutor, generating quizzes, and submitting answers.

API testing differs from unit and service testing in that it exercises the **full stack** through HTTP, including serialization, routing, middleware (e.g., authentication, validation), and database access. Well-designed API tests complement unit and mock tests by catching integration failures that are invisible at lower levels.

The ESBot API follows REST conventions and returns standard HTTP status codes. All endpoints accept and return JSON. The base URL for a locally running instance is `http://localhost:8000` (Python reference implementation) or the equivalent for your stack.

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | `GET` | `/api/v1/health` | Liveness check |
| 2 | `POST` | `/api/v1/sessions` | Create a learning session |
| 3 | `GET` | `/api/v1/sessions?user_id={id}` | List sessions for a user |
| 4 | `GET` | `/api/v1/sessions/{session_id}` | Get session metadata |
| 5 | `DELETE` | `/api/v1/sessions/{session_id}` | Delete session |
| 6 | `POST` | `/api/v1/sessions/{session_id}/messages` | Send a chat message |
| 7 | `GET` | `/api/v1/sessions/{session_id}/messages` | Retrieve message history |
| 8 | `POST` | `/api/v1/sessions/{session_id}/quiz` | Generate a quiz |
| 9 | `POST` | `/api/v1/sessions/{session_id}/quiz/{question_id}/answer` | Submit a quiz answer |

> **LLM note:** Use a **mock** or **stub** LLM provider when running API tests so that chat and quiz endpoints return deterministic responses without a real AI inference engine.

---

## Learning Objectives

After completing this exercise, you should be able to:

- Reflect on and document a REST API for testability, including base URL, endpoints, HTTP methods, and expected request/response formats.
- Manually exercise an HTTP API using at least one tool (Postman, curl, Talend API Tester, HTTPie, or equivalent).
- Write automated API tests against a running service using a framework appropriate for your technology stack.
- Apply equivalence class partitioning and boundary value analysis to HTTP inputs (paths, query strings, request bodies, headers).
- Design and execute smoke, load, and stress tests for the ESBot API and interpret the results against defined non-functional requirements (NFRs).
- Document findings, anomalies, and performance bottlenecks in a structured test report.

---

## Pre-requisites

- Your ESBot repository with REST endpoints from **Exercise 8.4** implemented and passing local tests.
- A locally startable backend (any supported stack: Python/FastAPI, Java/Spring Boot, .NET/ASP.NET, Node.js/Express, or equivalent).
- Access to at least one manual testing tool: [Postman](https://www.postman.com/), [curl](https://curl.se/), [Talend API Tester](https://chrome.google.com/webstore/detail/talend-api-tester/aejoelaoggembcgapehfcdmlicigmgdi), or [HTTPie](https://httpie.io/).
- Basic knowledge of HTTP methods and status codes.
- ESBot application description: [`docs/esbot.md`](../esbot.md)

**Tech stack note:** All tasks below are written in stack-neutral terms. Use the testing tool or framework that fits your backend. Examples for common stacks are provided throughout.

---

## Exercise 10.1 (10 Points): Reflect on Your REST API

### Task

Review the REST API endpoints you implemented in **Exercise 8.4**. Verify that your backend provides support for **at least five** of the nine scenarios listed in the Background section above or appropriate for your stack. Start the backend locally and confirm it is reachable at its base URL.

### Step 1 — Start the backend

Start your backend and verify that the health or status endpoint responds successfully (e.g., `GET /api/v1/health` returns `200 OK`).

### Step 2 — Document your API

Create or update a file `docs/api/api-reference.md` in your repository containing:

- **Base URL** and any required environment variables to start the backend (e.g., database, LLM provider mock mode).
- **Endpoint table** — for each implemented endpoint: HTTP method, path, brief description, required request headers, request body schema (or `N/A`), expected success status code, and example success response body.
- **Error responses** — document at least the `404 Not Found`, `422 Unprocessable Entity`, and `500 Internal Server Error` cases with example response bodies.
- **Setup instructions** — step-by-step instructions for a fresh checkout: install dependencies, configure environment variables, start the backend, and verify the health endpoint.

### Deliverables (10.1)

- Running backend accessible at a documented base URL.
- `docs/api/api-reference.md` covering all implemented endpoints with request/response schemas and error behavior.

---

## Exercise 10.2 (10 Points): Manual API Testing

### Task

Use a manual API testing tool to interact with your running ESBot backend. Execute a **complete happy-path workflow** and at least **two error scenarios** to verify your implementation handles them correctly.

### Step 1 — Choose a tool

Select at least one of the following (or an equivalent tool approved by your instructor):

| Tool | Notes |
|------|-------|
| [Postman](https://www.postman.com/) | Desktop app; supports collections, variables, test scripts |
| [Talend API Tester](https://chrome.google.com/webstore/detail/talend-api-tester/aejoelaoggembcgapehfcdmlicigmgdi) | Free Chrome extension; imports Postman v2 collections |
| [HTTPie](https://httpie.io/) | Command-line tool; human-friendly syntax |
| [curl](https://curl.se/) | Universal command-line tool |
| [Bruno](https://www.usebruno.com/) | Open-source Postman alternative; stores collections as plain files |
| REST Client (VS Code extension) | `.http` files within VS Code |

### Step 2 — Execute a happy-path workflow

Run requests in an appropriate happy-path order, capturing the full request and response for each step ´, for example (may differ depending on your stack and API endpoints):

1. **Health check** — `GET /api/v1/health` → expect `200` with `"status": "ok"` (or equivalent).
2. **Create session** — `POST /api/v1/sessions` with a `user_id` and a `title` → expect `201`; save the returned `session_id`.
3. **List sessions** — `GET /api/v1/sessions?user_id={your_user_id}` → expect `200`; confirm the new session appears.
4. **Get session** — `GET /api/v1/sessions/{session_id}` → expect `200`.
5. **Send message** — `POST /api/v1/sessions/{session_id}/messages` with a non-empty `content` → expect `201`.
6. **Get message history** — `GET /api/v1/sessions/{session_id}/messages` → expect `200`; confirm message appears.
7. **Generate quiz** — `POST /api/v1/sessions/{session_id}/quiz` with a `topic` and a `count` → expect `201`; save `question_id` and `correct_answer`.
8. **Submit correct answer** — `POST /api/v1/sessions/{session_id}/quiz/{question_id}/answer` → expect `200`.
9. **Delete session** — `DELETE /api/v1/sessions/{session_id}` → expect `204` (optional cleanup).

### Step 3 — Execute error scenarios

Perform at least **two** invalid request tests and document the actual response for each. For example (may differ depending on your stack and API endpoints):

| Scenario | Expected behavior |
|----------|-------------------|
| `GET /api/v1/sessions/{non_existent_id}` | `404 Not Found` |
| `POST /api/v1/sessions` with an empty or missing `user_id` | `422 Unprocessable Entity` |
| `POST /api/v1/sessions/{session_id}/messages` with empty `content` | `422 Unprocessable Entity` |
| `POST /api/v1/sessions/{session_id}/quiz/{wrong_id}/answer` | `404 Not Found` |
| `POST /api/v1/sessions/{session_id}/messages` after the session is deleted | `404 Not Found` |

### Deliverables (10.2)

- Screenshots or exported request/response pairs for each step of the happy-path workflow (saved to `docs/api/manual-tests/`).
- Screenshots or request/response pairs for the two error scenarios.
- A short written summary (`docs/api/manual-tests/summary.md`) reflecting on what you observed: Were all status codes as expected? Did the error messages provide useful feedback? Did any request behave unexpectedly?

---

## Exercise 10.3 (10 Points): Automated API Testing

### Task

Implement an **automated API test suite** that starts (or assumes a running) backend and exercises it over HTTP using a testing framework. The test suite must cover the happy-path workflow and at least four negative/edge-case scenarios.

### Suggested frameworks by stack

| Stack | Framework / library |
|-------|---------------------|
| Python | [`pytest`](https://pytest.org/) + [`httpx`](https://www.python-httpx.org/) or [`requests`](https://requests.readthedocs.io/); or [`pytest`](https://pytest.org/) + [`FastAPI TestClient`](https://fastapi.tiangolo.com/tutorial/testing/) |
| Java | [REST Assured](https://rest-assured.io/) with JUnit 5; or Spring Boot's `MockMvc` / `WebTestClient` |
| .NET | [Microsoft.AspNetCore.Mvc.Testing](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests) with xUnit |
| Node.js | [Supertest](https://github.com/ladjs/supertest) with Jest or Mocha |
| Any stack | [Hurl](https://hurl.dev/) (plain-text `.hurl` files, language-agnostic) |

### Required test scenarios

Implement at least five tests covering the happy-path and at least four negative/edge-case scenarios. For example (may differ depending on your stack and API endpoints):

**Happy path (sequential workflow):**

1. Health endpoint returns `200` with expected status field.
2. Creating a session with valid data returns `201` and a non-empty `session_id`.
3. Listing sessions for the created user returns `200` and includes the new session.
4. Sending a message to the session returns `201` and a non-empty response body.
5. Retrieving message history returns `200` and the list contains the sent message.
6. Generating a quiz returns `201` with at least one question.
7. Submitting a correct quiz answer returns `200`.

**Negative / edge cases (choose at least four):**

| Case | Assertion |
|------|-----------|
| Session not found | `404` status code |
| Empty `user_id` on session create | `422` status code |
| Empty `content` on message send | `422` status code |
| Very long `content` (> configured max) | `422` or `400` status code |
| Invalid UUID in path | `404` or `422` status code |
| Duplicate answer submission for same question | `400` or `409` status code (if your implementation enforces this) |
| `GET /api/v1/sessions/{id}/messages` before any message is sent | `200` with empty list |

### Guidelines

- Use an **in-memory or test database** (e.g., SQLite in-memory, H2, or test-scoped PostgreSQL) so tests are self-contained and repeatable.
- Configure the **LLM provider to mock mode** (or inject a stub) so chat and quiz responses are deterministic.
- Tests should **not** depend on execution order — use setup/teardown hooks to create and clean up sessions per test or test class.
- **Assert response bodies**, not only status codes — verify that returned JSON fields have the expected types and non-empty values.

### Deliverables (10.3)

- Automated test suite committed to your repository (e.g., `tests/api/` or `src/test/api/`).
- All tests passing locally with a single command (document this command in `docs/api/automated-tests.md`).
- `docs/api/automated-tests.md` explaining: framework choice, how to run the suite, how the backend is started/configured for tests, and a brief description of each test group.

---

## Exercise 10.4 (10 Points): Performance & Load Testing

### Task

Design and execute **performance tests** for the ESBot API and evaluate the results against the defined non-functional requirements (NFRs). ESBot's NFR states:

> **Load:** up to **50 concurrent users**  
> **Response time:** **2–5 seconds** under normal load

Focus performance tests on **non-LLM endpoints** (health, session CRUD, message history) to keep results deterministic and reproducible without a live AI inference engine.

### Suggested tools

| Tool | Notes |
|------|-------|
| [Apache JMeter](https://jmeter.apache.org/) | GUI-based; generate HTML dashboards; `.jmx` plans |
| [Gatling](https://gatling.io/) | Code-as-tests (Scala/Java/Kotlin); rich HTML reports |
| [Locust](https://locust.io/) | Python-native; web dashboard; scriptable |
| [k6](https://k6.io/) | JavaScript-based; CLI; integrates with Grafana |
| [Artillery](https://www.artillery.io/) | YAML/JavaScript; Node.js-based |
| [wrk](https://github.com/wg/wrk) | Lightweight CLI benchmarking tool |

### Test plans

Implement the following **three test profiles**. Adapt thread counts and durations to your tool's configuration syntax:

#### Smoke test (sanity check)
- **Goal:** Verify the API handles minimal load without errors.
- **Load:** 1–2 virtual users, 3–5 iterations each.
- **Endpoints:** `GET /api/v1/health`, `POST /api/v1/sessions`, `GET /api/v1/sessions?user_id=...`.
- **Pass criteria:** All responses `2xx`, zero errors, response time < 1 s.

#### Load test (NFR validation)
- **Goal:** Verify the API meets the NFR under expected concurrent load.
- **Load:** 50 virtual users, 60-second ramp-up, 5-minute sustained run.
- **Endpoints:** Same as smoke test, plus `GET /api/v1/sessions/{id}` and `GET /api/v1/sessions/{id}/messages`.
- **Pass criteria:** 95th-percentile response time ≤ 2 s, error rate < 1%.

#### Stress test (breaking point exploration)
- **Goal:** Determine where the API begins to degrade.
- **Load:** Ramp from 50 to 200+ virtual users over 10 minutes; observe when errors or latency exceed acceptable thresholds.
- **Endpoints:** Same as load test.
- **Observe:** At which concurrency level does the error rate exceed 5%? What is the approximate throughput ceiling (requests/second)?

### Result analysis

After each test run, collect and document the following metrics:

| Metric | Description |
|--------|-------------|
| Throughput | Requests per second (RPS) |
| Average response time | Mean latency across all requests |
| 90th / 95th / 99th percentile | Tail latencies |
| Error rate | Percentage of non-2xx responses |
| Peak concurrency reached | Maximum VUs without exceeding the error threshold |

### Deliverables (10.4)

- Test plan files committed to your repository (e.g., `docs/api/performance/` — `.jmx`, Gatling simulation class, `locustfile.py`, or `k6` script).
- Generated test reports or screenshots of dashboards for all three profiles.
- A written performance report `docs/api/performance/report.md` covering:
  1. Tool chosen and rationale.
  2. Test environment (hardware, OS, backend configuration, database).
  3. Results table for each profile (throughput, percentile latencies, error rate).
  4. Interpretation: Does the ESBot backend meet the NFR under the load test? At what point does it degrade in the stress test?
  5. At least two observations or recommendations for improving backend performance.

---

## Hints and Common Pitfalls

- **Start fresh before each test run:** Use an in-memory SQLite database or a freshly migrated test database to avoid carryover state between test executions.
- **Mock the LLM for all testing:** Real LLM inference is non-deterministic and slow. Use `LLM_PROVIDER=mock` (Python reference) or inject an equivalent stub in your stack to keep tests fast and reliable.
- **Test isolation in automated tests:** Always create a dedicated session per test and delete it in a teardown step. Never share session IDs between tests — one failing test will cascade failures.
- **Path vs. query parameter validation:** Check both — e.g., an invalid UUID in a path parameter and a missing required query parameter should both be handled gracefully.
- **Don't assert exact LLM wording:** Even with a mock LLM, avoid asserting specific message content. Assert structure (non-empty string, correct JSON keys) rather than exact values.
- **Performance baseline first:** Always run the smoke test before the load and stress tests. If smoke fails, fix the issue before scaling up virtual users.
- **Single worker for in-memory SQLite:** When using SQLite in-memory for performance tests, configure your backend to use a single worker/process — in-memory SQLite is per-process and will return empty results under multiple workers.
- **Port conflicts:** Ensure no other process occupies the API port before starting the server for tests. Use environment variables to configure the port if needed.

---

## Submission

Commit all deliverables to your repository and submit the repository link via Moodle by the course deadline.

Ensure the following artefacts are present before submission:

- [ ] `docs/api/api-reference.md` — documented endpoints, request/response schemas, error codes (11.1)
- [ ] `docs/api/manual-tests/` — screenshots or exported request/response pairs for happy path and error scenarios (11.2)
- [ ] `docs/api/manual-tests/summary.md` — written reflection on manual testing observations (11.2)
- [ ] `tests/api/` (or equivalent folder) — automated API test suite with all required scenarios (11.3)
- [ ] `docs/api/automated-tests.md` — framework choice, run instructions, test descriptions (11.3)
- [ ] `docs/api/performance/` — test plan files (JMeter `.jmx`, Gatling simulation, Locust/k6 script, etc.) (11.4)
- [ ] `docs/api/performance/report.md` — results tables, NFR evaluation, observations, recommendations (11.4)
