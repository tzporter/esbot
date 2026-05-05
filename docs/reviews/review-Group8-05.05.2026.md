# Review Report (Inspection / Technical Review)

**Project / product:** ESBot  (https://github.com/Mooh9876/esbot)
**Review object(s):** GitHub repository   
**Review type:** Technical review / inspection  
**Date (planned / actual):** 2026-05-05  
**Moderator:** Sena Zeynep Yamak 
**Author(s):** Mooh9876 et al.  
**Reviewers:** Zeynep Pektas, Truman Porter, Melek Gokler 

---

## 1. General instructions

This review is based on inspection of the ESBot GitHub repository.  
The project is a bot system with:

No direct communication with authors was conducted due to time constraints.

---

## 2. Master Plan (MP)

### 2.1 Masterplan — header

| Field | Value |
|-------|-------|
| Review No. | REV-2026-ESBOT-001 |
| Project | ESBot |
| Project manager | — |
| Quality expert / manager | — |
| Moderator | Sena Zeynep Yamak |
| Author(s) | Mooh9876 et al. |

---

### 2.2 Review objects

### 2.2 Review objects

| # | Review objects | Abbr. |
|---|----------------|-------|
| 1 | `docs/esbot.md` | EB |
| 2 | `docs/spec/requirements.md` | REQ |
| 3 | `docs/spec/spec.md` | SPEC |
| 4 | `docs/spec/data-model.md` | DM |
| 5 | `docs/spec/plan.md` | PLAN |
| 6 | `docs/spec/quality.md` | QUAL |
| 7 | `docs/spec/test-strategy.md` | TS |
| 8 | `docs/spec/use-cases.md` | UC |
| 9 | `docs/spec/ux-factors.md`, `docs/spec/ux-evaluation-plan.md`, `docs/spec/ux-quality-model.md` | UX |
| 10 | `docs/setup.md` | SETUP |
| 11 | `docs/Project_Outline.md` | OUTLINE |
| 12 | `backend/app/models/*.py` | MOD |
| 13 | `backend/app/main.py` | API |
| 14 | `backend/app/ai_provider.py` | AI |
| 15 | `backend/tests/*.py` | TEST |
| 16 | `backend/features/*.feature`, `backend/features/steps/*.py` | BDD |
| 17 | `backend/Dockerfile`, `docker-compose.yml`, `.devcontainer/devcontainer.json` | DEV |

---

### 2.3 Reference documents

| # | Reference documents | Abbr. |
|---|---------------------|-------|
| 1 | ESBot Case Study Description | CSD |
| 2 | ESBot Requirements Specification | RS |
| 3 | Repository README.md | README |
| 4 | Source code (frontend, backend, database) | SRC |

---

### 2.4 Checklists / scenarios

| # | Checklists / scenarios |
|---|-------------------------|
| 1 | Code structure and modularity |
| 2 | Security (input validation, secrets) |
| 3 | External service integration safety |
| 4 | Error handling and logging |
| 5 | Documentation completeness |

---

### 2.5 Reviewer assignment

| Reviewer | Scope | Abbr. |
|:--------:|-------|-------|
| 1 | Architecture & modularity | R1 |
| 2 | Security & integrations | R2 |
| 3 | Documentation & usability | R3 |

---

### 2.7 Individual preparation

| Individual preparation | Value | Unit |
|------------------------|-------|------|
| Submission of findings by | 2026-05-05 | — |
| Size of review objects | Medium (~5k–10k LOC estimated) | NLOC |
| Optimal inspection rate | 250 | NLOC/h |
| Optimal inspection time | ~12 | h |

---

## 3. List of findings (LoF)

| ID | Location | Summary | Type | Severity | Status | Owner | Notes |
|----|----------|---------|------|----------|--------|-------|-------|
| F-01 | AI | Lack of Token Rate Limiting: No logic to handle LLM rate limits, leading to potential service crashes. | Stability | Major | Open | Authors | - |
| F-02 | MOD | Using Integer for Primary Keys in a web-facing bot can lead to ID Enumeration attacks. If an attacker knows one evaluation ID, they can guess others by incrementing the integer. | Security | Major | Open | Authors | - |
| F-03 | MOD/EvaluationResult.md | Using Text for feedback without a length constraint in the application layer could lead to "Database Bloat" if the AI provider returns unexpectedly large responses. | Suggestion | Minor | Open | Authors | - |
| F-04 | database.py | The use of create_engine and a synchronous SessionLocal inside FastAPI means every database query blocks the entire event loop. This negates the performance benefits of FastAPI. | Architecture | Major | Open | Authors | Direct conflict with NFR1 (Performance). |
| F-05 | database.py | create_engine is called with default parameters. Without pool_size or max_overflow limits, the bot may exhaust PostgreSQL connections during peak usage. | Stability | Major | Open | Authors | Critical when the user traffic is unpredictable. |
| F-06 | API | lifespan is an async def, yet it uses engine.connect() (blocking) to check the DB. This pauses the startup of the entire application until the DB responds or times out | Architecture | Major | Open | Authors | Leads to slow recovery in containerized environments. |
| F-07 | MOD | There is no persistent User model to store long-term data (e.g., student name, preferences, or learning history). All data appears tied to ephemeral sessions. | Architecture | Critical | Open | Authors | Prevents longitudinal progress tracking.|
| F-08 | MOD/user_session.py | Use of sessions as a proxy for identity means a user loses all conversational context and quiz results upon session termination. | Defect | Major | Open | Authors | Impacts usability and data persistence. | 
| F-09 | REQ | "Contextualized answers" and "integrate an LLM" lack quality metrics. Without defining accuracy or hallucination thresholds, the system cannot be formally validated. | Defect | Major | Open | Authors | High risk for educational software.|
| F-10 | REQ | "Multiple concurrent users" is not quantified. This ambiguity led to the architectural decision to use synchronous DB drivers | Defect | Major | Open | Authors | Needs a specific load target. |
| F-11 | BDD/ask_question.feature | The test accepts an email parameter ({email}) but explicitly notes that the domain model cannot store it. This confirms the system is incapable of identifying a specific student across different test runs.| Architecture | Critical | Open | Authors | Direct conflict with "Registered" requirement. |


---

## 4. Data Summary (DS)

| Metric | Value | Notes |
|--------|-------|-------|
| Size of review object | ~5k–10k LOC | Estimated |
| Preparation effort | ~10–12 hours | — |
| Number of findings (initial) | 11 | — |
| Number of findings after meeting | 11 | No meeting |
| Rework effort | — | Not available |
| Re-inspection required? | Yes | Multiple major issues |

---

## 5. Review Report (RR)

### 5.1 Summary

The technical inspection reveals a project with strong initial feature work but significant architectural bottlenecks. The most critical concern is the "Identity Gap": while the requirements and BDD tests describe a system for registered students, the database and code only support anonymous, short-lived sessions. Furthermore, the mismatch between the asynchronous API framework and the synchronous database driver creates a "performance ceiling" that prevents true scalability.

---

### 5.2 Review outcome

- **Review object state after review:** Accepted with major required changes  
- **Major risks:**
  - Identity Fragmentation: Loss of all user data upon session timeout.  
  - Concurrency Deadlock: Sync database calls blocking the FastAPI event loop. 

---

### 5.3 Decisions and follow-up

| Topic | Decision | Responsible | Due date |
|-------|----------|-------------|----------|
| Identity Refactor | Implement a persistent User model to replace the current ephemeral session-only identity. | Authors |2026-05-19|
| Test Integrity | Align BDD step definitions with the domain model to ensure tests reflect actual system capabilities. | Authors |2026-05-19 |
| Async Migration | Replace psycopg2 with an asynchronous driver (e.g., asyncpg) to prevent event-loop blocking. | Authors | 2026-05-09 |

---

### 5.4 Positive observations

- The choice of FastAPI and Pydantic-Settings provides a strong foundation for high-performance, type-safe development. 
- The presence of a Dockerfile and decvontainer configuration indicates a commitment to consistent development environments. 
- The extensible architecture allows for easy addition of new features without altering core logic. 

---

### 5.5 Lessons learned

- The Async-Sync Conflict: Utilizing an asynchronous framework like FastAPI requires a fully non-blocking stack; a single synchronous DB driver can bottleneck the entire system.  
- Requirements-Code Alignment: Technical reviews are essential to catch "Identity Gaps," where test scenarios promise features that the underlying data model does not support.   

---

### 5.6 Sign-off

| Role | Name | Signature / date |
|------|------|------------------|
| Moderator | Sena Zeynep Yamak | 2026-05-05 |
| Reviewer 1 | Zeynep Pektas |2026-5-05|
| Reviewer 2| Truman Porter | 2026-05-05 |
| Reviewer 3 | Melek Gokler | 2026-05-05 |

Google Gemini was used in the development of this document as a form of brainstorming and revising work. All AI-edited content was thoroughly checked.