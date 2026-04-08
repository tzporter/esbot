# UX Evaluation Plan



## 1. Evaluation Scope

### UX Factors Under Evaluation

This plan covers the five UX factors listed in `docs/spec/ux-factors.md`

1. Learnability and Intuitive Use
2. Clarity and Comprehensibiity
3. Information Efficiency
4. Trust and Transparency of AI Responses
5. Error Handling

### User Journeys Covered 

The following journeys are selected because they exercise all five UX Factors listed above.

**Journey A — First-Time Opening the System**
A student opens ESBot for the first time, locates the input field, submits their first question, and reads the response.

*Primarily tests:* Learnability, Clarity


**Journey B — Topic Explanation Request**
A student requests for an explanation of a topic and evaluates whether the response is accurate.

*Primarily tests:* Clarity, Information Efficiency, Error Handling

**Journey C — Quiz Generation**
A student requests multiple-choice quiz questions on a topic, submits their answer and receives feedback.

*Primarily tests:* Clarity, Information Efficiency

**Journey D — Source and Transparency Review**
A student inspects how ESBot gave a certain answer via checking the sources it used, AI-generated warnings, and data usage disclosures.

*Primarily tests:* Trust and Transparency

**Journey E — API Failure Recovery**
A simulated API Error occurs mid-session; the student observes how the system responds and recovers.

*Primarily tests:* Error handling, Trust

---

## 2. Method Set

### Method 1: Heuristic Evaluation


**Description:** Two evaluators independently assess the ESBot interface against Nielsen's 10 usability heuristics, cross-referenced with the five UX factors above.

**When:** Before user testing sessions, to identify obvious issues early.

**Focus heuristics:**
- Visibility of system status 
- Match between system and real world 
- Error prevention and recovery 

**Output:** A list of heuristic violations with severity ratings (0–4 scale).

## Method 2: Cognitive Walkthrough


**Description:** Evaluators simulate a first-time user stepping through each of the five user journeys and evaluate if the journeys are easy to navigate for first time users.

**When:** After heuristic evaluation, before participant sessions.

**Focus:** Primarily Learnability and Clarity.

**Output:** Per-step analysis for each journey with identified breakdowns.

## Method 3: Think-Aloud Sessions
**Description** Participants work through assigned scenarios while narrating their thoughts out loud. A facilitator observes without intervening. Sessions are recorded with consent.

**When:** Main data collection phase.

**Scenarios assigned:**
- Scenario 1: "You are preparing for your Data Structures and Algorithms exam. Use ESBot to get a summary of linked lists."
- Scenario 2: "Ask ESBot to generate 5 quiz questions on sorting algorithms and answer them."

**Output:** Qualitative observations

## Method 4: Automated End-to-End Testing  

**Description** Automated E2E tests simulate the full Streamlit → FastAPI → PostgreSQL → Streamlit flow for Journey E. 

**When:** Run as part of the CI pipeline before any evaluation session, to confirm the test environment is stable.

**Output:** Pass/fail test report with response latency measurements and logged validation events.

---

### 3. Participants and Setup

## Target Users 
SWB Students in Hochschule Esslingen

## Session Structure 

| Phase | Duration | Activity |
|-------|----------|----------|
| Introduction | 5 min | Explain process, obtain recording consent |
| Warm-up | 5 min | Free exploration of ESBot interface |
| Think-aloud scenarios | 20 min | Scenarios 1–3, participant narrates thoughts |
| Scenario-based tasks | 15 min | Timed tasks, silent completion |
| SUS questionnaire | 5 min | Written questionnaire |
| Debrief interview | 10 min | Open questions on trust, clarity, and satisfaction |
| **Total** | **~60 min** | |

### Materials Required
- ESBot running in a stable test environment 
- Scenario instruction cards (printed or on-screen)
- Screen and audio recording software
- SUS questionnaire (printed or digital form)
- Observation sheet for facilitator
- Simulated API error trigger (for Journey E) — a pre-configured mock that returns a malformed LLM response to exercise the FastAPI validation and retry logic

---

## 4. Metrics and Acceptance Criteria


### Factor 1: Learnability and Intuitive Use
| Metric | Acceptance Criterion |
|--------|----------------------|
| Time to first successful interaction (Journey A) | ≤ 90 seconds without external help for ≥ 80% of participants |
| First-attempt task success rate on Journey A | ≥ 80% of participants complete without error |
| SUS score (learnability sub-questions) | Average score ≥ 70 out of 100 |

### Factor 2: Clarity and Comprehensibility
| Metric | Acceptance Criterion |
|--------|----------------------|
| Response accuracy (verified against course materials) | ≥ 90% of sampled responses contain no factual errors |
| Participant comprehension rating (post-task, 1–5 scale) | Average ≥ 4.0 across scenarios |
| Heuristic violation count for clarity-related heuristics | ≤ 3 violations rated severity ≥ 2 |

### Factor 3: Information Efficiency
| Metric | Acceptance Criterion |
|--------|----------------------|
| Time to locate the key answer within a response | ≤ 30 seconds for ≥ 75% of participants |
| Participant rating of response conciseness (1–5 scale) | Average ≥ 3.8 |

### Factor 4: Trust and Transparency
| Metric | Acceptance Criterion |
|--------|----------------------|
| Percentage of participants who locate data usage disclosure unprompted | ≥ 60% during Journey D |
| Percentage of AI responses that include a source reference or warning about AI fallibility | ≥ 80% of sampled responses |
| Participant trust rating after session (1–5 scale) | Average ≥ 3.5 |


### Factor 5: Error Handling
| Metric | Acceptance Criterion |
|--------|----------------------|
| Proportion of retried requests that resolve transparently without user re-prompting | ≥ 90% |
| Participant frustration rating during error scenario (1–5, lower is better) | Average ≤ 2.5 |
| Response latency under normal conditions (measured via FastAPI structured logs) | ≤ 5 seconds for ≥ 90% of requests |

---

## 5. Findings Template

Each identified issue is documented using the following structure:

---

**Issue ID:** `UX-[NNN]`

**UX Factor:** 
- The UX factor that this observation concerns

**ISO 25010 Characteristic:** 
- The ISO 25010 equivalent of the said factor

**Journey / Scenario:** 
- In which journey or scenario did this issue occur

**Description:**
A concise, neutral description of the observed problem. 

**Evidence:**
- Observation, quote, or screen recording timestamp

**Severity:** 0 = Cosmetic | 1 = Minor | 2 = Moderate | 3 = Major | 4 = Critical

**Frequency:** 
- Frequency of the said observation

**Affected Metric:** 
- Which metric is affected by this observation

**Recommendation:**
A concrete suggestion for resolving the issue.

---

## 6. Quality Gate Proposal

Below is the quality gate that defines when UX issues are severe enough to block a release.

### Gate Levels

**Release is Blocked: must be fixed before deployment**
- Any issue rated Severity 4 
- Any acceptance criterion from Factor 4 (Trust) or Factor 5 (Error Handling) not met, as these directly affect user safety and data integrity
- SUS score below 50 
- Task completion rate below 60% for any user journey
- Automated E2E tests failing

**Release is Conditional: must be tracked**
- Any acceptance criterion from Factors 1–3 not met
- Three or more Severity 3 (Major) issues identified during evaluation
- Any issue affecting ≥ 60% of participants, regardless of severity rating

**Release Approved**
- No severity 4 issues
- Factor 4 and 5 acceptence criteria are met
- SUS score ≥ 70 
- Primary journey task completion rates ≥ 80%




