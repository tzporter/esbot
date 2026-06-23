# Exercise 11 – UI and End-to-End Testing

## Goal

The goal of this exercise is to validate the **ESBot** application from the user's perspective. You will start from a working frontend (either the provided Vue reference implementation or your own), perform structured manual UI testing, implement automated end-to-end (E2E) tests that exercise the full stack through the browser, and document your results.

---

## Background

Unit tests verify individual functions in isolation. API tests verify the backend over HTTP. **UI and E2E tests** close the loop by driving a real browser through real user workflows: e.g., clicking buttons, filling forms, and asserting what the user actually sees on screen.

ESBot's frontend is a single-page application that interacts with the backend REST API (Exercise 10).
According to the lecture notes, all interactive elements in the reference frontend should carry stable **`data-testid`** attributes designed for automated testing. No brittle CSS selectors or XPaths are required. The following table lists the `data-testid` attributes for the interactive elements in the reference frontend:

Examples for test identifiers to consider could be in your project:

| Element | `data-testid` |
|---------|---------------|
| API health badge | `health-status` |
| Error banner | `error-banner` |
| User ID input | `user-id-input` |
| New session button | `new-session-btn` |
| Session list | `session-list` |
| Session item | `session-item-{uuid}` |
| Message list | `message-list` |
| Message input | `message-input` |
| Send button | `send-message-btn` |
| Chat loading indicator | `chat-loading` |
| User message bubble | `user-message` |
| Assistant message bubble | `assistant-message` |
| Quiz topic input | `quiz-topic-input` |
| Generate quiz button | `generate-quiz-btn` |
| Quiz question text | `quiz-question` |
| Quiz option (0-based) | `quiz-option-0` … `quiz-option-3` |
| Submit answer button | `submit-answer-btn` |
| Quiz feedback | `quiz-feedback` |

> **LLM mock note:** For testing purpuses, you should consider using a mock LLM provider. Start the backend with your mock provider so chat and quiz responses are deterministic.

---

## Learning Objectives

After completing this exercise, you should be able to:

- Set up and run a full-stack local development environment (backend + frontend) for UI/E2E testing.
- Execute structured manual UI test cases and record outcomes in a test report.
- Identify stable test selectors (`data-testid`, roles, labels) and explain why they are preferable to CSS class or XPath selectors.
- Implement automated E2E tests for at least two complete user flows using a framework of your choice (Cypress, Playwright, or Selenium).
- Run E2E tests in both interactive/headed and headless (CI-style) modes.
- Reflect on the trade-offs between manual UI testing, automated E2E testing, and lower-level unit/API testing.
- Integrate E2E tests into a CI pipeline so they run automatically on every push.

---

## Pre-requisites

- Your ESBot repository with a running backend (from Exercise 8.4 / Exercise 10) and the enpoints you have implemented.
- A working frontend. Ensure it covers either session creation, chat, or quiz flows, and that it exposes stable `data-testid` selectors (or equivalent) for automated testing. You only need to implement a single flow.
- Node.js 18+ (required for Cypress and Playwright; not required for Selenium-only setups).
- Your BDD scenarios from **Exercise 5** — use these as the source of user flows to automate.
- ESBot application description: [`docs/esbot.md`](../esbot.md)

**Tech stack note:** The E2E testing tool is your choice. Cypress and Playwright require Node.js and work across all operating systems. Selenium with Python, Java and other language bindings, is an alternative for teams that prefer an alternative toolchain. Please note that Selenium does not support `linux-arm64`. Use Cypress or Playwright instead.

---

## Exercise 11.1 (10 Points): UI Setup and Manual Testing

### Task

Start your backend and frontend using the commands appropriate for your stack. Confirm the health check endpoint is reachable and the UI renders without errors.
Execute a set (at least two) of your BDD test senarios in a manual setup. 
For each test case, record the following in `docs/ui/manual-tests/report.md`:

1. Test case ID (e.g. TC-UI-03)
2. Date and tester name
3. Environment: OS, browser, LLM mock used for the test
4. Steps performed
5. Expected vs. actual result
6. Pass / Fail
7. Screenshot for any failed or unexpected outcome (if necessary)

### Deliverables (11.1)

- `docs/ui/manual-tests/report.md` — completed test report for your test cases.
- Screenshots or screen recordings for any failed test cases (stored in `docs/ui/manual-tests/screenshots/`).
- A short paragraph at the end of the report reflecting on the manual testing experience: What was straightforward? What was tedious or error-prone? How could automation help?

---

## Exercise 11.2 (10 Points): Automated E2E Tests

### Task

Implement an automated E2E test suite that exercises the core ESBot user flows through the browser. Your suite must automate **at least two complete flows** from your BDD test scenarios and should also cover **at least one negative/error scenario**.

Select one of the following frameworks and implement your E2E test suite and document the setup in `docs/ui/e2e-setup.md`:

| Framework | Language | Run command | Best for |
|-----------|----------|-------------|----------|
| [Cypress](https://www.cypress.io/) | JavaScript | `npm run test:e2e:cypress` | Interactive debugging, visual test runner |
| [Playwright](https://playwright.dev/) | JavaScript / TypeScript | `npm run test:e2e:playwright` | Cross-browser, trace viewer, codegen |
| [Selenium](https://www.selenium.dev/) | Python (pytest) | `pytest e2e/selenium/` | Python-native teams; not available on linux-arm64 |

#### Guidance on selectors

Always use `data-testid` selectors — never CSS classes or positional XPaths, e.g., using Cypress:

```javascript
// Cypress
cy.get('[data-testid="send-message-btn"]').click()

// Playwright
await page.getByTestId('send-message-btn').click()

// Selenium (Python)
driver.find_element(By.CSS_SELECTOR, '[data-testid="send-message-btn"]').click()
```

Never assert on **exact mock LLM text** beyond what is guaranteed by the mock — assert that the reply is non-empty and contains the known mock prefix.

#### Guidance on waiting

E2E tests interact with an asynchronous UI. Use the built-in waiting mechanisms — never use fixed `sleep()`:

| Framework | Wait strategy |
|-----------|---------------|
| Cypress | Auto-retry built in; use `.should('be.visible')` |
| Playwright | Auto-wait built in; use `expect(locator).toBeVisible()` |
| Selenium | Use `WebDriverWait` + `expected_conditions` |

### Deliverables (11.2)

- E2E test files committed to your repository (extend the `cypress/e2e/`, `playwright/`, or `e2e/selenium/` folders, or create equivalent structure for your own frontend).
- All tests passing locally with a single command (document this in `docs/ui/e2e-setup.md`).
- `docs/ui/e2e-setup.md` covering: framework chosen, installation steps, how to start the application before running tests, and the exact run command.

---

## Exercise 11.3 (10 Points): Execute, Record, and Reflect

### Task

Run your full E2E test suite in both **interactive/headed mode** and **headless mode**. Capture the output and reflect on what you observed.

### Step 1 — Headless run (CI-style)

Run all E2E tests without a visible browser window:

| Framework | Headless command |
|-----------|-----------------|
| Cypress | `npm run test:e2e:cypress` (headless by default) |
| Playwright | `npm run test:e2e:playwright` |
| Selenium | `pytest e2e/selenium/ -v` (headless Chrome via Selenium Manager) |

Capture the terminal output (copy–paste or screenshot).

### Step 2 — Interactive / headed run

Observe the browser executing the tests in real time:

| Framework | Interactive command |
|-----------|---------------------|
| Cypress | `npm run test:e2e:cypress:open` → Click **E2E Testing** → select spec → choose browser |
| Playwright | `npx playwright test --headed` or `npx playwright test --ui` |
| Playwright (debug) | `npx playwright test --debug` — step through line by line |
| Selenium | Tests run in visible Chrome; Selenium has no separate interactive mode |

Take a screenshot of the interactive test runner showing green/passing tests.

### Step 3 — Handle failures

If any test fails:

1. Read the error message and stack trace.
2. Use the framework's debugging tools (Cypress screenshots in `cypress/screenshots/`, Playwright traces via `npx playwright show-trace`, Selenium `NoSuchElementException` messages).
3. Fix the issue or document it as a known limitation in your report.

### Step 4 — Write the reflection

Create `docs/ui/e2e-report.md` with the following sections:

1. **Test execution summary** — how many tests ran, how many passed/failed, total runtime, framework and version used.
2. **Headless output** — paste or screenshot the terminal output from the headless run.
3. **Interactive run screenshot** — embed a screenshot of the interactive runner showing results.
4. **Flakiness observations** — did any test pass on one run and fail on another? If so, what caused it (timing, LLM non-determinism, state leakage)?
5. **Reflection** — answer the following questions in a few sentences each:
   - What was easy about writing E2E tests compared to unit or API tests?
   - What was difficult or surprising?
   - At which layer of the test pyramid (unit, API, E2E) would you detect each of the bugs your tests could catch? Why?
   - How would these tests behave with a real (non-mock) LLM? What would you change?

### Deliverables (11.3)

- `docs/ui/e2e-report.md` — execution summary, outputs, screenshots, and reflection.
- All E2E tests passing in headless mode on a clean run (or failures explained and justified in the report).

---

## Exercise 11.4 (10 Points): CI Pipeline Integration (Optional)

### Task

Extend your GitHub Actions workflow (from Exercise 9) by creating a new workflow file with a dedicated job that runs the E2E test suite automatically on every push or pull request.

Create a new job in a new workflow file (e.g., `.github/workflows/e2e.yml`). The job must:

1. Check out the code.
2. Set up Node.js (18+) and install frontend dependencies.
3. Set up the backend runtime and start the backend with an appropriate LLM mock.
4. Start the frontend dev server.
5. Run the E2E tests in headless mode.
6. Upload test artifacts (screenshots, videos, traces) on failure.

> **Selenium note:** Selenium requires a Chrome installation on the runner. Add the appropriate steps before running Selenium tests on `ubuntu-latest`.

1. Push your changes and confirm the workflow turns green on GitHub.
2. Deliberately break one test (e.g., change an assertion) to verify the pipeline goes red; then revert.
3. Document the pipeline design in `docs/ui/ci-e2e.md`:
   - Trigger conditions (push, pull request, manual)
   - How the backend and frontend are started in CI
   - Which framework you used and why
   - How artifacts (screenshots/traces) are preserved on failure
   - Any trade-offs: runtime, flakiness, resource cost

### Deliverables (11.4)

- Updated `.github/workflows/ci.yml` (or new `e2e.yml`) with the E2E job.
- Evidence of at least one successful green pipeline run (link or screenshot in `docs/ui/ci-e2e.md`).
- `docs/ui/ci-e2e.md` — pipeline design documentation.

---

## Hints and Common Pitfalls

- **Always use `data-testid` selectors.** CSS classes and positional selectors (`:nth-child`) break whenever the UI is refactored. `data-testid` attributes are stable contracts between the UI and the test suite.
- **Never use fixed `sleep()` waits.** Async UI operations (API calls, DOM updates) complete at variable times. Use Cypress's built-in retry, Playwright's auto-wait, or Selenium's `WebDriverWait` instead.
- **Do not assert exact LLM text.** Even with a mock LLM, only assert that the response is visible and contains the known mock prefix. Asserting the full sentence makes tests fragile if the mock changes.
- **Test isolation matters in E2E too.** If one test leaves data behind (e.g., a session with messages), the next test may see unexpected state. Use a unique `user_id` per test or clean up with a `beforeEach`/`afterEach` hook.
- **Selenium on ARM (Apple Silicon / linux-arm64):** Google does not publish ChromeDriver for `linux-arm64`. On ARM containers use Cypress or Playwright instead; Selenium is available on macOS, Windows, and x86_64 Linux.
- **Frontend proxy vs. direct URL:** Leave `VITE_API_BASE_URL` empty in `.env` so the Vite dev proxy routes `/api` requests to port 8000. Setting it to `http://localhost:8000` bypasses the proxy and triggers CORS in the Cypress Electron browser.
- **CI service startup order:** Ensure the backend is healthy before starting the frontend, and the frontend is reachable before running tests. Use `wait-on` or a short health-check loop rather than fixed `sleep` in CI.
- **BDD scenarios as a test source:** Your Gherkin feature files from Exercise 5 describe the exact user flows to automate in this exercise. Map each `Given`/`When`/`Then` step to an E2E action and assertion.

---

## Submission

Commit all deliverables to your repository and submit the repository link via Moodle by the course deadline.

Ensure the following artefacts are present before submission:

- [ ] `docs/ui/manual-tests/report.md` — completed test report for TC-UI-01 through TC-UI-06 (12.1)
- [ ] `docs/ui/manual-tests/screenshots/` — screenshots for any failed or noteworthy test cases (12.1)
- [ ] E2E test files in `cypress/e2e/`, `playwright/`, or `e2e/selenium/` (12.2)
- [ ] `docs/ui/e2e-setup.md` — framework choice, installation, run command (12.2)
- [ ] `docs/ui/e2e-report.md` — execution summary, outputs, reflection (12.3)
- [ ] `.github/workflows/ci.yml` or `e2e.yml` — E2E CI job (12.4)
- [ ] `docs/ui/ci-e2e.md` — CI pipeline design documentation and evidence of green run (12.4)
