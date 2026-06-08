# Exercise 9: Continuous Integration (CI)

## Scope of the Exercise

In this exercise, you will set up a **Continuous Integration (CI)** pipeline using **GitHub Actions** to automatically build, test, and verify your **ESBot** project on every relevant change.

ESBot is an AI-powered learning assistant for students (see `docs/esbot.md`). By this point in the course, your repository should already contain backend domain models, unit tests, mock-based service tests, repository tests, REST endpoints (Exercise 8), and locally runnable static analysis from Exercise 6. CI does not replace that work — it **automates the same checks** you already trust on your machine.

This exercise deliberately follows a **local-first, then CI** workflow:

1. **Local verification** — define and run the exact commands (tests, linters, builds) that must pass before you push.
2. **CI workflow** — encode those commands in `.github/workflows/ci.yml` so GitHub runs them on push and pull requests.
3. **Pipeline enhancement** — add at least one further GitHub Actions integration from the categories below (coverage, security, matrix builds, caching, etc.).

After completing this exercise, your repository should contain a working GitHub Actions workflow, documentation of your pipeline design decisions, and an updated top-level `README.md` showing the pipeline status badge.

---

## Learning Objectives

After completing this exercise, you should be able to:

* Define a **repeatable local quality gate** for ESBot (test suite + at least one static check aligned with your stack)
* Create a **GitHub Actions workflow** (`ci.yml`) with appropriate triggers, runner, checkout, environment setup, and test execution
* Explain **why** you chose specific triggers, runners, and job structure for a three-tier application with external AI dependencies
* Integrate **additional workflow actions** (security, coverage, linting in CI, build matrix, caching, etc.) and articulate their value for ESBot
* Add a **CI status badge** to `README.md` and keep local vs. CI commands documented and in sync

---

## Pre-requisites

You need access to the following:

* ESBot application description: [`docs/esbot.md`](../esbot.md)
* Your team’s implementation and tests from Exercises 4–8 (domain models, BDD, reviews, test design, mocks, repositories, REST API)
* Static analysis setup from **Exercise 6.3** (`docs/spec/static-analysis.md`) — at least two tools run **locally**
* A **GitHub repository** for your ESBot project with push access
* Lecture materials on CI/CD and GitHub Actions
* Optional: `.devcontainer/` setup in this course template (Java 17, Node 20) if you develop in a dev container

**Tech stack note:** Teams may use different backends (e.g., Java/Spring Boot, Python/FastAPI, Node/Express). All tasks below are written in stack-neutral terms; substitute the correct runtime, package manager, and test command for **your** ESBot backend and frontend as decided in Exercise 1.

---

## Background: What CI Should Verify for ESBot

ESBot’s architecture (presentation, backend, persistence, optional LLM) implies a practical CI scope for this course:

| Layer | Typical CI checks (examples) |
|-------|------------------------------|
| **Backend** | Compile/build, unit tests (domain, services with mocks), repository tests (in-memory DB), optional integration tests without a live LLM |
| **Frontend** (if present) | Install dependencies, lint, unit tests |
| **Container / deploy** (if present) | Dockerfile lint (Hadolint), image build smoke test |
| **Quality** | Linters or formatters you configured in Exercise 6 (e.g., Flake8, Checkstyle, ESLint) |

**Important:** CI jobs should **not** depend on a running Ollama/vLLM instance unless you explicitly design a separate, optional job with mocks or contract tests. Service tests from Exercise 8 should use mocks so pipelines remain fast and deterministic — consistent with NFR testability in `docs/esbot.md`.

---

## Exercise 9.1 (10 Points): Local Verification and Basic CI Setup

### Phase A — Local verification (do this before writing `ci.yml`)

**Objective:** Establish the single command (or short script) that proves “ESBot is healthy” on your machine. Your CI workflow must run the **same** steps (or a documented subset).

#### Step A.1 — Run the test suite locally

Execute your full automated test suite from the repository root using your build tool, for example:

| Stack | Example command |
|-------|-------------------|
| Java (Maven) | `./mvnw test` or `mvn test` |
| Java (Gradle) | `./gradlew test` |
| Python | `pytest` or `uv run pytest` |
| Node.js | `npm test` |

**Requirements:**

* Tests must pass **without** a live LLM inference engine (use mocks/stubs as in Exercise 8).
* If tests need a database, use in-memory or test-scoped configuration (e.g., H2, SQLite, Testcontainers) — document any required env vars in `README.md` or `docs/setup.md`.
* Fix or skip (with justification in docs) any flaky tests before enabling CI.

Record the exact command(s) in `docs/ci/local-verification.md` (create this file).

#### Step A.2 — Run static analysis locally

Re-use the tools from **Exercise 6.3**. At minimum, run your **linter** locally and document the command. Use the official documentation for your stack:

| Stack / artefact | Tool | Documentation |
|------------------|------|----------------|
| Java (Maven) | Checkstyle (Maven plugin) | [Maven Checkstyle Plugin — Usage](https://maven.apache.org/plugins/maven-checkstyle-plugin/usage.html) |
| Python | Flake8 | [Flake8 documentation](https://flake8.pycqa.org/en/latest/) |
| Docker | Hadolint | [Hadolint — How to use](https://github.com/hadolint/hadolint?tab=readme-ov-file#how-to-use) |
| JavaScript/TypeScript | ESLint | [ESLint docs](https://eslint.org/docs/latest/) |

Add the linter command(s) to `docs/ci/local-verification.md`. If the linter reports issues, either fix them or document waivers and follow-up in `docs/spec/static-analysis.md`.

#### Step A.3 — Optional: local automation before push

To avoid pushing broken commits, you may wire the same commands into **Git hooks** (e.g., [pre-commit](https://pre-commit.com/) or a simple `pre-push` hook) or a `Makefile` / `package.json` script target such as `make verify` or `npm run verify`.

This step is **recommended** but not strictly required for full points on 9.1; if you implement hooks, document how to install and run them in `docs/ci/local-verification.md`.

**Deliverable (Phase A):** `docs/ci/local-verification.md` listing:

* Test command(s) and expected outcome
* Linter/static analysis command(s)
* Optional hook/script setup
* Any environment variables or services required locally

---

### Phase B — GitHub Actions basic workflow

**Objective:** Create a GitHub Actions workflow that mirrors Phase A on `ubuntu-latest`.

#### Task: Create `ci.yml`

Create a workflow file at **`.github/workflows/ci.yml`** with the following requirements:

| Requirement | Guidance |
|-------------|----------|
| **Trigger** | Use a suitable trigger mechanism — e.g. `push` to any branch **and** `pull_request` events — so every contribution is verified before merge |
| **Runner** | Use a standard hosted runner (e.g. `ubuntu-latest`) unless you document a strong reason for another image |
| **Checkout** | Check out your code using [`actions/checkout@v4`](https://github.com/actions/checkout) |
| **Environment setup** | Use official setup actions for **your** ESBot backend (and frontend if tested in CI), e.g. [`actions/setup-java`](https://github.com/actions/setup-java), [`actions/setup-python`](https://github.com/actions/setup-python), [`actions/setup-node`](https://github.com/actions/setup-node) — match versions to your project |
| **Test execution** | Run the **same** test command(s) documented in Phase A; fail the job if tests fail |

**Example structure (illustrative — adapt to your stack):**

```yaml
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Java
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "17"
          cache: maven
      - name: Run tests
        run: ./mvnw test
```

#### Task: Document your pipeline

Create **`docs/ci/pipeline.md`** and explain your configuration in prose (not only YAML comments), including:

1. **Triggers** — Why `push` and/or `pull_request`? Would you add `workflow_dispatch` for manual runs?
2. **Runner** — Why `ubuntu-latest` (or another image)?
3. **Environment** — Which language versions and caches did you configure?
4. **Jobs and steps** — What runs today; what is intentionally *out* of CI (e.g., live LLM, production DB)?
5. **Parity with local** — How Phase A commands map to CI steps; what to do when CI fails locally but passes on GitHub (or vice versa)

#### Task: README status badge

Update the **top-level `README.md`** with a GitHub Actions status badge for your workflow, for example:

```markdown
![CI](https://github.com/<ORG>/<REPO>/actions/workflows/ci.yml/badge.svg)
```

Replace `<ORG>` and `<REPO>` with your GitHub organization/user and repository name. Place the badge near the top of the README with your other shields.

**Deliverables (Exercise 9.1):**

* `docs/ci/local-verification.md` (Phase A)
* `.github/workflows/ci.yml` — working basic pipeline (Phase B)
* `docs/ci/pipeline.md` — design documentation (Phase B)
* Updated `README.md` with CI status badge

---

## Exercise 9.2 (10 Points): Explore More GitHub Actions

### Background

Basic CI proves that tests pass on a clean runner. Production-grade projects add **security**, **coverage**, **lint gates**, **matrix builds**, and **caching** to shorten feedback loops and catch more defect classes early.

Explore GitHub Actions capabilities:

* [GitHub Actions features](https://github.com/features/actions)
* [GitHub Marketplace — Actions](https://github.com/marketplace?type=actions)
* [Running variations of jobs in a workflow (matrix)](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/running-variations-of-jobs-in-a-matrix)

### Categories to explore

Choose **one additional integration** from the categories below (or a closely related action documented on the Marketplace). Integrate it into your existing workflow (or a clearly named additional job in the same `ci.yml` file).

| Category | Examples relevant to ESBot |
|----------|----------------------------|
| **Security & dependency management** | Dependabot config; `npm audit`; [pip-audit](https://pypi.org/project/pip-audit/); [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/) |
| **Code quality & testing** | Code coverage upload (Codecov, Coveralls); **linting in CI** (ESLint, Flake8, Checkstyle via Maven/Gradle); **test matrix** across language versions (e.g. Python 3.10–3.12, Java 17 and 21) |
| **Build performance** | Dependency caching (`actions/cache`, built-in cache in setup-* actions) |
| **Pull request governance** | Branch protection with required status checks; required reviewers (document in `docs/ci/pipeline.md` — configuration is in GitHub repo settings) |

**Linting in CI (recommended if not done in 9.1):** If you only ran linters locally in Exercise 6, add a CI job step that runs the same linter (Flake8, Checkstyle, ESLint, or Hadolint for `Dockerfile`) and fails the build on violations. This directly extends your local Phase A.2 setup.

**Test matrix (example):** For a Python ESBot backend, a matrix job can run `pytest` on multiple Python versions to catch compatibility issues:

```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
```

See the [GitHub documentation on matrix strategies](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/running-variations-of-jobs-in-a-matrix).

### Task

1. **Select** one enhancement from the table above (or an approved equivalent from the Marketplace).
2. **Integrate** it into `.github/workflows/ci.yml` (additional job or steps).
3. **Verify** it runs successfully on a push or pull request (green workflow run).
4. **Document** the enhancement in **`docs/ci/pipeline.md`** under a section **“Exercise 9.2 enhancements”**, covering:
   * What action or tool you added
   * Why it fits ESBot (concrete benefit: security, speed, quality, compatibility)
   * Added value vs. cost (runtime, maintenance, false positives)
   * Whether the same check still runs locally (keep local and CI in sync)

**Deliverables (Exercise 9.2):**

* Enhanced `.github/workflows/ci.yml` (or additional workflow file, if justified and documented)
* Updated `docs/ci/pipeline.md` with the 9.2 section
* Evidence of at least one successful workflow run (link or screenshot referenced in the doc or PR)

---

## Hints and Common Pitfalls

* **Secrets:** Do not commit API keys, database passwords, or LLM tokens. Use GitHub **Secrets** only when necessary and document which steps need them.
* **Services:** Prefer embedded or in-memory databases in CI; avoid requiring PostgreSQL on `ubuntu-latest` unless you add a `services:` container and document it.
* **Flaky AI tests:** Never assert exact LLM wording in CI; assert service **behavior** with mocks (Exercise 8).
* **Monorepos:** If frontend and backend live in subfolders, set `working-directory` on steps or use separate jobs.
* **Failed badge:** The README badge stays red until the default branch workflow passes — fix failing steps rather than removing the badge.
* **Free tier limits:** Keep jobs reasonably fast; use caching (9.2) if dependency install dominates runtime.

---

## Submission

Commit all deliverables to your repository and submit the repository link via Moodle, following the course deadline and naming conventions.

Ensure the following artefacts are present before submission:

- [ ] `docs/ci/local-verification.md` — local test and linter commands (Phase A)
- [ ] `.github/workflows/ci.yml` — basic CI (9.1) plus 9.2 enhancement
- [ ] `docs/ci/pipeline.md` — triggers, runner, environment, local/CI parity, 9.2 rationale
- [ ] `README.md` — GitHub Actions CI status badge
- [ ] Green workflow run on the default branch (or documented reason for pending fix)


