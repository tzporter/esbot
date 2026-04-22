
# ESBot Test Strategy

## 1. Introduction

This document reflects on how ESBot's automated tests should be organised in the
project's Continuous Integration (CI) pipeline. In particular, it addresses the
question:

> *When should BDD/acceptance tests be executed relative to unit tests? Should
> they always run together, or should they be treated differently (e.g., executed
> less frequently, in a separate CI stage)?*

The discussion is grounded in ESBot's concrete situation: a FastAPI backend
tested with `pytest` (unit level) and `behave` (BDD level), where the BDD step
definitions mock the AI inference service to remain deterministic.

---

## 2. Unit Tests vs. BDD / Acceptance Tests

Unit tests and BDD tests serve different purposes and have very different
runtime characteristics. The table below summarises the main differences as
they apply to ESBot.

| Aspect              | Unit Tests (`pytest`)                              | BDD / Acceptance Tests (`behave`)                                      |
|---------------------|----------------------------------------------------|------------------------------------------------------------------------|
| **Execution time**  | Milliseconds per test; whole suite in seconds      | Seconds per scenario; whole suite noticeably slower                    |
| **Scope**           | A single class, function, or validation rule       | An end-to-end user flow across API, database, and (mocked) AI service  |
| **Purpose**         | "Is this unit of code internally correct?"         | "Does the system behave as the user expects?"                          |
| **Target audience** | Developers, during refactoring                     | Developers *and* non-technical stakeholders who read Gherkin scenarios |
| **Dependencies**    | None (entities tested in isolation, in-memory DB)  | HTTP client, database, mocked AI provider, test data lifecycle         |
| **Failure signal**  | "Logic in module X is broken"                      | "A user-facing behaviour is broken, somewhere in the chain"            |

These differences matter because they place the two test categories at different
layers of the well-known *test pyramid*: unit tests form the broad, fast base,
while BDD tests sit higher up and are fewer but more expensive to run.

---

## 3. Recommendation for ESBot's CI Pipeline

### 3.1 Recommendation

For ESBot, we recommend a **hybrid, two-tier strategy**:

- **On every commit (push to any branch):** run the full `pytest` unit suite.
- **On pull requests targeting `main`:** run the full `pytest` suite *and* the
  complete `behave` BDD suite, as separate but mandatory pipeline stages.
- Optionally, a small set of critical BDD scenarios can be tagged `@smoke`
  (for example: "student asks a question and receives an answer") and also
  executed on every commit, to catch severe regressions early without running
  the full acceptance suite.

### 3.2 Justification

The recommendation balances three competing concerns: developer feedback
speed, coverage confidence, and resource cost.

**Developer feedback speed.** Unit tests complete in seconds and confirm that a
change did not break low-level logic. If the pipeline on every commit were
several minutes long, developers would lose context while waiting and the
short feedback loop that makes CI valuable would be eroded. Running only the
unit suite on every commit preserves this loop.

**Coverage confidence at merge time.** The most valuable guarantees about
ESBot live at the integration boundary — the FastAPI endpoints, the SQLModel
persistence layer, and the AI service working together. A bug in the `/chat`
or `/quiz-request` flow is typically *not* caught by unit tests alone. Running
the full BDD suite on every pull request provides this guarantee exactly at
the moment it matters most: before code is integrated into a shared branch
that other developers depend on.

**Resource cost.** Running the full BDD suite on every single commit would
accumulate significant CI time across a working day, with diminishing returns,
because most commits are small and unlikely to break a user-facing flow.
Restricting the BDD suite to pull requests concentrates the cost at a
meaningful checkpoint.

### 3.3 Alternatives considered

Several alternative strategies were considered and rejected for ESBot:

- *Run everything on every commit.* Simplest, but scales poorly as the BDD
  suite grows over subsequent exercises (performance, UI automation).
- *Run only unit tests, never BDD in CI.* Fastest, but defeats the entire
  purpose of acceptance tests as a regression safety net.
- *Run BDD tests only on a nightly schedule.* Acceptable for large projects,
  but for ESBot it delays feedback too much — a broken `/chat` flow would
  persist in `main` for up to a day before being noticed.

The hybrid approach above is a deliberate middle ground between these
extremes.

---

## 4. The Role of AI Mockability

The recommendation in Section 3 depends critically on the fact that ESBot's
BDD step definitions replace the real AI provider with a mock. Without this,
acceptance tests in CI would be impractical for three reasons.

**Non-determinism.** Real language models do not produce identical outputs
for identical prompts. A scenario such as *"the response should contain
feedback 'Correct! Mache is the right conjugation...'"* could pass on one run
and fail on the next, not because the code changed, but because the model
phrased its answer differently. Tests that flake like this are actively
harmful: developers learn to ignore failures, which defeats the safety net.
Mocking `ai_provider.get_explanation`, `get_quiz`, and `evaluate_answer`
makes the outputs fully deterministic.

**External dependencies in CI.** The CI runner is a short-lived machine that
does not, and should not, have access to a production AI endpoint (e.g. a
Groq or OpenAI API key). Depending on such an endpoint would couple every
test run to network availability, third-party quotas, and paid API usage —
none of which are properties of the code being tested. The mocks eliminate
this coupling entirely: BDD tests run offline, with no API keys, and no cost
per run.

**Speed.** A real AI call can take seconds of latency, and the BDD suite
exercises the AI inference interface across many scenarios. With the mocks
in place, each invocation returns instantly, keeping the full acceptance
suite well under a minute even as it grows.

Taken together, these three properties are what make it *realistic* to
include BDD tests in CI at all, and specifically in the pull-request stage
recommended above. If ESBot's acceptance tests required a live model, the
only viable strategy would be to run them manually or on a sparse schedule —
losing most of the regression-prevention value they were written for.

---

## 5. Summary

Unit tests and BDD tests address different questions ("is the code correct?"
vs. "does the system behave correctly?") and have different costs. For
ESBot, the recommended CI strategy is to run unit tests on every commit and
the full BDD suite on every pull request, with an optional `@smoke` subset
running alongside the unit tests on commits. This strategy is only feasible
because ESBot's step definitions mock the AI inference service, which
guarantees deterministic, offline, low-latency execution of acceptance
tests in CI.


<!-- This file was created with AI assistance. AI was used to brainstorm the
two-tier CI strategy.. -->
