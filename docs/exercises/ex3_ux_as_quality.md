# Exercise 3: UX Factors and Quality Assurance

## Scope of the Exercise

In this exercise, you will analyze and improve the user experience (UX) of the ESBot application based on the system description in `docs/esbot.md` and the project constitution `.specify/memory/constitution.md` created as part of Exercise 2.

The focus is not only on UI appearance, but on measurable UX quality factors, user learning support, and quality assurance methods that make UX requirements testable and reviewable.

After this exercise, your repository should contain a UX-oriented quality model,
UX requirements, and a practical UX evaluation concept for ESBot.

## Learning Objectives

After completing this exercise, you should be able to:

* Identify relevant UX factors for an AI-powered learning assistant
* Translate UX expectations into testable quality requirements
* Apply ISO/IEC 25010 quality characteristics to UX-related concerns
* Design transfer-oriented and experience-oriented question sets for ESBot
* Document a structured UX evaluation approach with clear acceptance criteria

---

## Pre-requisites

You need to have access and/or installed the following tools:
* Markdown editor
* The ESBot application description in `docs/esbot.md`
* The project constitution in `.specify/memory/constitution.md`
* Your results from Exercise 2 (`docs/spec/requirements.md`, `docs/spec/quality.md`,
  and optionally `docs/spec/spec.md`)
* Read the article “[Faktoren der User Experience: Systematische Übersicht über produktrelevante UX-Qualitätsaspekte](https://www.researchgate.net/publication/281784277_Faktoren_der_User_Experience_Systematische_Ubersicht_uber_produktrelevante_UX-Qualitatsaspekte)“ – English version: „[Applicability of User Experience and Usability Questionnaires](https://core.ac.uk/download/pdf/395662617.pdf)“. 

---

## Exercise 3.1 (10 Points): UX Factor Identification

In your opinion, identify and justify the **five most relevant UX factors** for ESBot in a learning context based on `docs/esbot.md`

Examples of UX factors you may consider include:
* learnability
* clarity/comprehensibility
* feedback quality
* trust and transparency of AI responses
* error tolerance and recovery support
* interaction efficiency
* accessibility

For each factor, provide:
1. A concise definition in your own words
2. Why this factor is relevant for ESBot users (CS students)
3. A concrete example interaction in ESBot where this factor is critical

Document your findings in `docs/spec/ux-factors.md`.

## Exercise 3.2 (10 Points): ISO 25010 Mapping for UX

Map your selected UX factors to relevant ISO/IEC 25010 quality characteristics (for example: Usability, Functional Suitability, Reliability, Security, Maintainability, Compatibility).

For each mapping, define:
1. UX factor -> ISO 25010 characteristic(s)
2. A measurable quality criterion
3. A verification method (how you would evaluate or test it)

Important:
* Avoid vague wording such as "easy", "good", or "fast" without measurable criteria
* Ensure each criterion can be verified by a test, review, or measurable observation

Document your findings in `docs/spec/ux-quality-model.md`.

## Exercise 3.3 (15 Points): UX Evaluation Plan and Acceptance Criteria

Create a compact UX evaluation plan for ESBot that can be executed in your team.

Your plan must include:
1. **Evaluation scope** (which UX factors and user journeys you will test)
2. **Method set** (e.g., heuristic evaluation, cognitive walkthrough,
   think-aloud sessions, scenario-based tests)
3. **Participants and setup** (target users, session duration, materials)
4. **Metrics and acceptance criteria** (measurable thresholds)
5. **Findings template** (issue description, severity, evidence, recommendation)
6. **Quality gate proposal** explaining when UX findings must block release

Align your acceptance criteria with:
* ISO/IEC 25010-based quality requirements
* Constitution principles (testability, architecture-aware contracts, and
  reviewable quality expectations)

Document your plan in `docs/spec/ux-evaluation-plan.md`.

---

## Submission

Submit your findings in form of a link to your repository via moodle.
