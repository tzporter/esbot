# Exercise 11.3 — E2E Execution Summary and Reflections

## 1. Test Execution Summary
- **Framework & Version:** Cypress v15.18.0
- **Execution Engine:** Node v22.13.1 running inside Electron 138 (Headless)
- **Total Tests Executed:** 3 (2 Happy Paths, 1 Negative Scenario)
- **Passed:** 3 | **Failed:** 0
- **Total Duration:** 13 seconds
- **Spec File Found:** `cypress/e2e/esbot.cy.js`

## 2. Headless Output

```text
  Running:  esbot.cy.js                                                                (1 of 1)

  ESBot E2E User Flows
    ✓ Happy Path 1: Should create a new session and successfully send/receive a chat message (3720ms)
    ✓ Happy Path 2: Should generate a quiz and submit an answer (3962ms)
    ✓ Negative Scenario 1: Should show a warning when submitting an empty quiz answer (3617ms)

  3 passing (14s)

  ┌────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ Spec                                         Tests  Passing  Failing  Pending  Skipped  │
  ├────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ √  esbot.cy.js                      00:13        3        3        -        -        - │
  └────────────────────────────────────────────────────────────────────────────────────────────────┘
    √  All specs passed!                00:13        3        3        -        -        -
```

## 3. Interactive Run Verification
The visual automated run has been successfully validated through the interactive test runner execution suite, showing all 3 tests passing cleanly in Chrome.

![Cypress Interactive Success](docs/ui/automated-tests/interactive-run-verification.jpg)
 

---

## 4. Flakiness Observations

One challenge observed during execution was related to Streamlit’s frontend rendering behavior. Since Streamlit frequently updates UI state through WebSocket-based rerendering, DOM elements may temporarily unmount, move, or become covered by overlay components during execution.

During initial runs, rapid user actions occasionally triggered interaction failures because temporary transparent loading overlays intercepted click events.

To reduce flakiness and improve reliability, explicit Cypress interaction overrides using `{ force: true }` were applied where appropriate in `.click()` and `.type()` commands. Combined with Cypress’s built-in retry mechanism and visibility checks, these adjustments produced stable and repeatable executions across multiple runs.

---

## 5. Reflection Prompts

### What was easy about writing E2E tests compared to unit or API tests?

Writing E2E tests felt relatively intuitive because the scripts follow user behavior directly. Actions such as entering inputs, navigating pages, clicking buttons, and validating visible results mirror real application usage.

Unlike unit tests, E2E testing does not require isolating components or building extensive mocks. Compared with API testing, there is less emphasis on request construction and backend inspection because the application is evaluated from the user perspective.

### What was difficult or surprising?

The most difficult aspect was handling Streamlit’s dynamically generated interface. Components are often rendered without predictable identifiers and may appear inside changing container structures.

Selecting stable elements required using user-visible labels and strategic selectors such as `cy.contains()` and positional targeting methods like `.last()` rather than relying on static IDs.

Another challenge was synchronizing test execution with frontend rerender cycles to avoid timing-related interaction failures.

### At which layer of the test pyramid (unit, API, E2E) would you detect each of the bugs your tests could catch? Why?

**Unit Layer:**
Suitable for validating isolated logic components.

**API Layer:**
Best for detecting backend failures including incorrect responses, routing problems, failed database operations, invalid payload handling, or service communication issues.

**E2E Layer:**
Most effective for identifying full-system integration issues that only appear in realistic user workflows, such as blocked buttons, rendering failures, broken navigation, session management errors, or frontend/backend synchronization problems.

### How would these tests behave with a real (non-mock) LLM? What would you change?

Executing the suite against a production LLM would introduce variable response times, network delays, token streaming behavior, and non-deterministic output generation.

To improve reliability under real conditions:

* Replace exact text assertions with structural validations.
* Increase timeout thresholds to account for inference delays.
* Validate output properties instead of specific generated sentences.
* Prefer stable UI-state assertions over token-level content assertions to minimize false failures caused by natural variation in model responses.


Google Gemini was used to generate the outline of this report. All AI generated content has been thoroughly checked. 