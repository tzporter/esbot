# Exercise 7: Test Design Techniques

## Scope of the Exercise

In this exercise, you will practice systematic **black-box and state-based test design
techniques** applied to the *ESBot* application.

In black-box testing you have no access to the internal source code — only the feature
specification and observable behaviour. Your task is to exercise three core test design
techniques from the lecture to derive representative, non-redundant test cases that
cover all crucial scenarios, including valid conditions, invalid input, boundary values,
and state transitions.

After completing this exercise, your repository should contain a structured test design
document for the targeted ESBot features, including derived equivalence classes, a
decision table, a state transition diagram, and a set of concrete test cases.

---

## Learning Objectives

After completing this exercise, you should be able to:

* Apply **Equivalence Class Partitioning (ECP)** to partition an input domain into valid
  and invalid classes and identify representative test values including boundary conditions
* Construct a **Decision Table** to systematically derive test cases from combinations of
  conditions and actions
* Model **State Transition** behaviour and derive a transition table and coverage-based
  test sequences
* Relate the designed test cases back to ESBot requirements and acceptance criteria from exercise 2.
* Justify why each designed test case represents its class or transition and which
  requirement it verifies

---

## Pre-requisites

You need to have access to the following materials:

* ESBot application description: `docs/esbot.md`
* Your results from Exercise 2 (`docs/spec/requirements.md`, `docs/spec/use-cases.md`)
  and Exercise 4 (`docs/spec/data-model.md`)
* Lecture slides covering: *Equivalence Class Partitioning*, *Boundary Value Analysis*,
  *Decision Tables*, and *State Transition Testing*

---

## Exercise 7.1 (20 Points): Black-Box Testing Techniques

### Background

ESBot receives user input at multiple points: when a student submits a **chat message**
(FR-001, FR-002) and when a student submits a **quiz request** (FR-003). Both operations
are subject to input validation rules that determine whether the request is accepted or
rejected. In addition, the answer evaluation feature (FR-004) produces different outcomes
depending on a combination of conditions that can be modelled as a decision table.

The relevant validation rules for a **QuizRequest** are:

* **Topic length**: The topic string must be between 3 and 100 characters (inclusive).
* **Requested question count**: Must be an integer between 1 and 10 (inclusive).
* **Difficulty hint**: Must be one of the accepted values: `easy`, `medium`, or `hard`.
  Any other value (including blank/null) is invalid.

In black-box testing you have no access to the source code. Use only the specification
above and the requirements from exercise 2.

---

### Steps for ECP (Equivalence Class Partitioning)

#### Step 1 — Identify Valid and Invalid Equivalence Classes

For each of the three input parameters of `QuizRequest` (`topic`, `count`, `difficulty`),
identify all **valid** and **invalid equivalence classes**.

Present your results in the following table format (one table per input parameter):

| Parameter | Class ID | Class Type | Partition Description | Representative Test Value |
|-----------|----------|------------|-----------------------|--------------------------|
| `topic`   | EC-T-1   | Valid       | …                     | …                        |
| `topic`   | EC-T-2   | Invalid     | …                     | …                        |
| …         | …        | …           | …                     | …                        |

#### Step 2 — Justify Each Class

For each identified equivalence class, provide a brief explanation (2–4 sentences) of:

1. Why the chosen representative value is a valid representative for the whole class.
2. Whether the class contains a boundary value, and if so, which concrete boundary
   values you derive (lower bound, upper bound, and one value just outside each bound).
3. Which ESBot requirement (e.g., FR-003) or acceptance scenario the class maps to.

**Important:** Boundary values must be derived explicitly for all numeric and
length-constrained inputs. For the `topic` parameter, derive test values for the
minimum-length boundary (2, 3, and 4 characters) and the maximum-length boundary
(99, 100, and 101 characters).

#### Step 3 — Decision Table for Answer Evaluation

The answer evaluation feature (FR-004) combines three independent conditions to
determine the type of feedback returned to the student:

| Condition | Values |
|-----------|--------|
| **Answer correctness** | Correct / Partially correct / Incorrect |
| **Answer is empty or blank** | Yes / No |
| **Quiz item still exists in session** | Yes / No |

Build a **complete decision table** covering all meaningful condition combinations and
specify the expected action (system output / feedback type) for each column. Use `–`
(don't-care) where a condition is irrelevant given another condition's value.

For each rule in your decision table, note the corresponding ESBot requirement or edge
case from exercise 2 (e.g., FR-004, or the edge case "empty input").

**Expected Deliverables:**

* Equivalence class tables for all three `QuizRequest` input parameters.
* Boundary value analysis documentation for `topic` length and `count`.
* A complete decision table for the answer evaluation feature with requirement
  references per rule.
* All artefacts committed to `docs/spec/test-design.md` in your repository.

---

## Exercise 7.2 (15 Points): State Transition Testing — Learning Session Lifecycle

### Background

ESBot manages **UserSession** objects that persist a student's learning context
(FR-005). A session transitions through a defined lifecycle from creation to
termination. Based on the requirements mentioned in `docs/esbot.md`, a `UserSession` can be in the
following states:

| State | Description |
|-------|-------------|
| `NEW` | Session created; no messages exchanged yet. |
| `ACTIVE` | At least one interaction has occurred (question asked, quiz requested, or answer submitted). |
| `IDLE` | No activity for a defined inactivity threshold; session is still restorable. |
| `EXPIRED` | Session has exceeded the maximum lifetime or was explicitly closed; no further interactions are accepted. |

The following **events** trigger transitions:

* `submit_message` — Student submits a chat message or question.
* `request_quiz` — Student requests a quiz for a topic.
* `submit_answer` — Student submits an answer to a quiz item.
* `inactivity_timeout` — System detects that the inactivity threshold has been exceeded.
* `session_timeout` — System detects that the maximum session lifetime has been exceeded.
* `close_session` — Student or system explicitly closes the session.
* `resume_session` — Student returns and re-activates an `IDLE` session.

### Tasks

#### Step 1 — State Transition Diagram

Draw a **state transition diagram** for the `UserSession` lifecycle covering all states
and events listed above. You may use any notation (hand-drawn and photographed, a text-based diagram such as Mermaid, or a UML tool). Include:

* All states as named nodes.
* All valid transitions as directed edges labelled with the triggering event.
* Guard conditions where relevant (e.g., a `submit_message` event in `EXPIRED` state
  must be rejected — show this as an invalid or self-loop with an error output).

#### Step 2 — State Transition Table

Derive a **complete state transition table** from your diagram. Use the following format:

| Current State | Event | Next State | Output / Action |
|---------------|-------|------------|-----------------|
| `NEW` | `submit_message` | `ACTIVE` | Message accepted; session context updated |
| … | … | … | … |

For transitions that are invalid (i.e., the event cannot occur in that state), record
the current state and event and specify `–` (invalid) as the next state and the expected
error behaviour (e.g., "Return controlled error: session expired").

#### Step 3 — Test Case Derivation

From your state transition table, derive a set of **test sequences** that together
achieve **all-transitions coverage** (every valid transition is exercised at least
once).

For each test sequence, document:

1. The start state.
2. The ordered list of events applied.
3. The expected state after each event and the expected system output.
4. The ESBot requirement or edge case the sequence verifies (e.g., FR-005, or the edge
   case "session state missing or expired").

Provide at least one test sequence that exercises an **invalid transition** (an event
applied to a state where it is not allowed) and verify that the system returns a
controlled response consistent with FR-009 and NFR-003.

**Expected Deliverables:**

* State transition diagram (image, Mermaid code block, or equivalent), committed to
  `docs/spec/test-design.md` or a linked asset.
* Complete state transition table covering all states × all events.
* A minimum set of test sequences achieving all-transitions coverage, with requirement
  references, committed to `docs/spec/test-design.md`.

---

## Exercise 7.3 (5 Points): Reflection — Test Design Technique Comparison

In `docs/spec/test-design.md`, add a short reflective section (roughly half a page)
addressing the following questions:

1. **Complementarity:** Which scenarios are best covered by ECP/BVA, which by decision
   tables, and which by state transition testing? Give a concrete ESBot example for
   each.
2. **Gaps:** Are there ESBot behaviours that none of the three techniques cover well?
   What alternative technique would you apply and why?
3. **Effort vs. value:** For the ESBot project specifically, which technique produced
   the highest defect-detection value relative to the design effort? Justify your
   answer with reference to at least one requirement from the specification.

---

## Submission

Commit all deliverables to your repository and submit the repository link via Moodle.

Ensure the following artefacts are present before submission:

- [ ] `docs/spec/test-design.md` containing:
  - Equivalence class tables for all three `QuizRequest` parameters
  - Boundary value analysis for `topic` and `count`
  - Decision table for answer evaluation with requirement references
  - State transition diagram (inline or linked asset)
  - State transition table (all states × all events)
  - All-transitions test sequences with requirement references
  - Reflective comparison section (Exercise 7.3)
