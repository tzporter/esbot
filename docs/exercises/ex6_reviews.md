# Exercise 6: Reviews and Static Code Analysis

## Scope of the Exercise

In this exercise, you will apply **formal review practices** to artefacts of the *ESBot* project and complement them with **static code analysis** executed **locally** on your machine (or in your development container).

The goals are to:

* Plan and conduct a structured review of ESBot-related documents and code, record findings, and reflect on the review method.
* Select and adopt **two** static analysis approaches (from different categories) that fit your tech stack, run them **without test automation integration** in this exercise, and document setup, usage, and impact.

After completing this exercise, your repository should contain review documentation (following the course review template), a short retrospective, and documentation of two static analysis tools with **local** execution instructions.

---

## Learning Objectives

After completing this exercise, you should be able to:

* Plan and run a review (roles, type, preparation, meeting/sessions) for a small software project
* Use a review template to capture issues, severity, and follow-up consistently
* Reflect on the usefulness of reviews for your team and for ESBot-type systems
* Name common categories of static analysis tools (linters, type checkers, security scanners, coverage, complexity, style, dependency checks, dead-code detection, etc.)
* Select tools appropriate to your stack, configure them locally, and interpret their output in the context of ESBot (API, persistence, AI integration boundaries)

---

## Pre-requisites

You need access to the following:

* ESBot baseline description: `docs/esbot.md`
* Your team’s earlier artefacts (requirements, specification, data model, tests) under `docs/spec/` and related paths, as produced in Exercises 2–5
* A clone of **another team’s ESBot repository** for the peer review (pairing or rotation is announced via the course / Moodle)
* Review templates supplied by the course (e.g. via Moodle); if templates are mirrored in a course repository, use the version linked there
* Lecture materials on inspections, walkthroughs, technical reviews, and static analysis
* For Exercise 6.3: ability to install and run tools locally (terminal, language runtimes, package managers for your stack)

---

## Exercise 6.1 (20 Points): Conduct a Review of Another Team’s ESBot Work

**Objective:** Practice the review process presented in the lecture (planning, kick-off, preparation, review session, follow-up) on real ESBot artefacts.

Your team reviews **another team’s** ESBot project (repository URL as assigned). The review must cover at least:

* The ESBot-oriented **introductory / system description** (equivalent to `docs/esbot.md` or the team’s merged variant)
* **Functional requirements and specification** (e.g. `docs/spec/requirements.md`, `docs/spec/spec.md`, or Spec Kit output paths used by that team)
* **Relevant implementation** to date (e.g. backend domain model, unit tests, BDD tests, etc.)

### Tasks

1. Assign **review roles** inside your team (e.g. moderator, expert reviewers, recorder/note-taker, author liaison if applicable).
2. Choose a **review type** (e.g. walkthrough, technical review, inspection) and justify why it fits the artefacts and timebox.
3. Hold a **preparation** phase: reviewers study the materials; record questions and assumptions. If required, you can ask the other team for clarifications or schedule a meeting to discuss the artefacts and to understand the project.
4. Run the **review session(s)** using the course review template: log defects, inconsistencies, ambiguities, and improvement suggestions with clear references (file, section, or module).
5. **Document** the review type, participants, scope, and outcomes in your **own** repository (e.g. `docs/reviews/review-<team-reviewed>-<date>.md` or as a filled template uploaded in the same form as required by Moodle).

**Expected deliverables:**
* Written evidence of planning (roles, review type, scope, schedule) in your repository.
* Completed review protocol / issue list using the course template in your repository.
* Brief summary of major findings and agreed follow-up (if any) in your repository.

---

## Exercise 6.2 (5 Points): Retrospective on the Review

**Objective:** Reflect on the review experience for ESBot.

Answer briefly in your repository (e.g. `docs/reviews/review-retrospective.md` or a section in the same document as Exercise 6.1):

* What worked well? What was difficult?
* Are formal reviews a suitable method for your team? For which artefacts (spec, design, code) would you use them again?
* One concrete improvement you would make for the next review round.

**Expected deliverables:** Short reflective text (roughly half to one page), committed to the repo unless Moodle instructions specify upload-only for this part.

---

## Exercise 6.3 (10 Points): Static Code Analysis — Local Execution for ESBot

**Objective:** Choose **two different categories** of static analysis and adopt **one tool per category** that supports your implementation stack. Run both tools **locally** against your ESBot codebas (local codebase execution).

Review the following **categories** (align with lecture slides as needed). You are not limited to the examples listed under each category.

| Category | Example tools (illustrative) |
|----------|------------------------------|
| **Linters** | Java: Checkstyle, PMD — Python: Pylint, Flake8 — JS/TS: ESLint |
| **Type checkers** | Python: mypy |
| **Security scanners** | Java: SpotBugs — Python: Bandit — JS/TS: `npm audit` (mind: registry/network) |
| **Code coverage** | Java: JaCoCo — Python: coverage — JS/TS: coverage via Jest or similar |
| **Complexity** | Java: PMD — Python: Radon — JS/TS: ESLint complexity rules |
| **Dependency checkers** | Java: OWASP Dependency-Check — Python: safety/pip-audit — JS/TS: `npm audit` |
| **Style / format checkers** | Java: Checkstyle — Python: black, ruff format — JS/TS: Prettier |
| **Dead code** | Java: PMD — Python: vulture — JS/TS: ESLint `no-unused-vars`, knip, etc. |

### Tasks

1. **Select two categories** and **two distinct tools** (one tool per category). Briefly  **justify** why these categories matter most for ESBot (e.g. API correctness, security around user data, maintainability of AI integration boundaries).
2. **Install and configure** the tools locally. Add configuration files to the repo where appropriate (e.g. `.eslintrc`, `pyproject`/`setup.cfg`, `pmd-ruleset.xml`, `.prettierrc`). Prefer defaults plus minimal project-specific rules; document any important choices.
3. **Run the tools locally** and capture how to invoke them (shell commands or `npm`/`mvn`/`gradle`/`make` targets). Document the exact commands in `README.md` or `docs/setup.md` and, if useful, in `docs/spec/static-analysis.md`.
4. **Evaluate impact:** In `docs/spec/static-analysis.md`, discuss usefulness for code quality and defect prevention, noise/false positives, and whether local runs slow down the development process or provide too much feedback. Optionally note what you would **not** automate in test automation pipeline yet and why (still keeping Exercise 6 focused on **local** execution only).

**Expected deliverables:**

* Two tool categories chosen, two tools configured, configuration committed where applicable
* Written justification + evaluation in `docs/spec/static-analysis.md`
* Reproducible **local** command lines documented in the repository

---

## Submission

Submit your results as a link to your repository via Moodle, following the course’s deadline and naming conventions.
