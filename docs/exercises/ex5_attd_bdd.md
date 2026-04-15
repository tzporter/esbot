# Exercise 5: ATDD, BDD, and Gherkin Syntax

## Scope of the Exercise

In this exercise, you will practice Acceptance Test Driven Development (ATDD) and
Behaviour Driven Development (BDD) applied to the *ESBot* application.

Building on the use cases, requirements, and domain models from previous exercises, the
goal is to describe ESBot's expected behaviour from an end-user perspective using the
Gherkin syntax, and then implement those descriptions as automated acceptance tests
using a BDD framework matching your tech stack.

After completing this exercise, your repository should contain Gherkin feature files
that describe ESBot's core user-facing behaviour, a corresponding step definition
implementation, and a fully automated BDD test run integrated into your project build.

---

## Learning Objectives

After completing this exercise, you should be able to:

* Explain the difference between unit tests and acceptance/BDD tests and their
  respective roles in a test strategy
* Write well-structured Gherkin scenarios (`Given`/`When`/`Then`) for ESBot user
  interactions
* Implement step definitions that translate Gherkin steps into executable test code
* Integrate BDD tests into your project build so they can be executed automatically
* Reason about when BDD/acceptance tests should be run relative to unit tests in a CI
  pipeline
* Apply AI mockability to acceptance tests so Gherkin scenarios remain deterministic
  and repeatable

---

## Pre-requisites

You need to have access and/or installed the following tools:

* Your configured backend project from Exercise 4 (project skeleton, domain entities,
  unit tests passing)
* Your results from Exercise 2 (`docs/spec/use-cases.md`, `docs/spec/requirements.md`)
  and Exercise 3 (`docs/spec/ux-factors.md`)
* A BDD framework compatible with your tech stack:
  * Java: [Cucumber for Java](https://cucumber.io/docs/installation/java/)
  * Python: [behave](https://behave.readthedocs.io/)
  * JavaScript/TypeScript: [Cucumber.js](https://cucumber.io/docs/installation/javascript/)
* Review lecture slides set 05: *"ATDD, BDD, TDD"* and the
  [Gherkin best practices guide](https://cucumber.io/docs/bdd/better-gherkin/)
* Reference implementation for a working BDD setup:
  [xyzTesting repository](https://github.com/dgrewe-hse/xyzTesting/)

---

## Exercise 5.1 (10 Points): Gherkin Scenario Definition

Based on your use cases from Exercise 2 (`docs/spec/use-cases.md`) and the ESBot
requirements baseline (`specs/esbot.md`), select
**three ESBot features** and write acceptance scenarios for each using the Gherkin
syntax.

Good candidates for ESBot scenarios include:

* A student asks a course question and receives a structured explanation
* A student requests a quiz for a specific topic and receives practice questions
* A student submits an answer to a quiz question and receives evaluation feedback
* A student resumes an existing learning session and prior context is available
* ESBot gracefully handles an AI service failure and returns a fallback response

For each selected feature, write **at least two scenarios** covering:

1. The **happy path** - expected successful interaction
2. An **alternative or error path** - edge case, missing input, or system failure

**Important - AI scenarios:** When a scenario involves AI-generated content
(explanations, quiz items, evaluation feedback), the step definitions implemented in
Exercise 5.2 MUST use a mock/stub AI provider rather than a live model. Describe
the expected deterministic output in your scenario steps accordingly.

**Task:** Create one or more `*.feature` files and place them in the appropriate
folder for your tech stack (e.g., `src/test/resources/features/` for Java). Make sure
your project dependency configuration (e.g., `pom.xml`, `requirements.txt`,
`package.json`) already includes the required BDD framework dependency.

**Expected Deliverables:** At least three `*.feature` files (or one file with three
feature blocks) containing well-formed Gherkin scenarios for ESBot interactions,
committed to your repository.

---

## Exercise 5.2 (10 Points): Step Definition Implementation

Implement the step definitions for the three feature scenarios you defined in
Exercise 5.1.

Create step definition files in the appropriate location for your tech stack, for
example:

* Java: `src/test/java/de/hse/esbot/steps/`
* Python: `features/steps/`
* JavaScript: `features/step_definitions/`

Name each step file to reflect the ESBot scenario it covers (e.g.,
`AskQuestionSteps.java`, `QuizGenerationSteps.java`, `AnswerEvaluationSteps.java`).

**Requirements for step implementations:**

* Each `Given`, `When`, and `Then` step in your feature files MUST have a matching
  step definition
* Steps that trigger AI-dependent behaviour MUST inject a mock/stub implementation of
  the AI inference interface instead of calling a live model — this keeps acceptance
  tests deterministic and fast
* Steps that involve database state (e.g., an existing session, stored messages) MUST
  set up and tear down test data within the step lifecycle (before/after hooks) so tests
  remain independent of each other
* Step definitions MUST NOT contain business logic — delegate to application services
  or use case handlers

For a working reference setup, see:
[xyzTesting repository](https://github.com/dgrewe-hse/xyzTesting/)

**Expected Deliverables:** A complete step definition file per scenario. All defined
Gherkin steps are implemented and the BDD tests pass when executed via the build tool.

---

## Exercise 5.3 (10 Points): BDD Test Automation and Test Strategy

### Part A — Automated Execution

Ensure that your BDD tests are detected and executed automatically as part of your
project build.

Depending on your tech stack, this may require additional configuration:

* **Java (Cucumber):** Create a JUnit runner class (e.g., `CucumberRunnerTest.java`)
  annotated with `@Suite` / `@SelectClasspathResource` or `@RunWith(Cucumber.class)`,
  and verify the Cucumber plugin entry in your `pom.xml` or `build.gradle`
* **Python (behave):** No additional runner needed; `behave` is invoked directly
* **JavaScript (Cucumber.js):** Add a script entry to `package.json` and verify
  the Cucumber configuration file

Verify that running your full test suite (e.g., `./mvnw test`, `pytest`, or
`npm test`) executes both unit tests from Exercise 4 and BDD acceptance tests.

**Expected Deliverables:** BDD tests run automatically via the project build command.
Document the exact command(s) needed to execute the full test suite in your
`README.md` or `docs/setup.md`.

### Part B — Test Strategy Reflection

Discuss and document the following question in `docs/spec/test-strategy.md`:

> **When should BDD/acceptance tests be executed relative to unit tests?**
> Should they always run together, or should they be treated differently
> (e.g., executed less frequently, in a separate CI stage)?

Your discussion must address:

1. The differences in execution time, scope, and purpose between unit tests and
   BDD/acceptance tests
2. A reasoned recommendation for ESBot's CI pipeline (e.g., always together, or
   unit tests on every commit and BDD tests on pull requests only)
3. How the AI mockability requirement affects this decision — specifically, why using
   mock AI providers makes acceptance tests feasible in CI even without a live model

---

## Submission

Submit your findings in form of a link to your repository via moodle.
