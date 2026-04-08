# Exercise 4: ESBot Core Domain Models and First Unit Tests

## Scope of the Exercise

In this exercise, you will begin the implementation of the *ESBot* backend by setting
up the project environment and implementing the core domain model. You will then write
a first suite of unit tests covering the most important entities and their business
rules.

After completing this exercise, your repository should contain a working backend
project skeleton, a set of implemented domain entities consistent with the ESBot data
model, and a comprehensive unit test suite for those entities.

**Note on data model consistency:** ESBot uses a the database you described in your tech stack as part of exercise 1.
All domain entities are persisted relationally and mapped using JPA annotations. This is
an intentional design choice. The AI inference component is
explicitly *not* a domain entity — it is a backend service interface that is isolated
and mockable. Do not model it as a database entity.

---

## Learning Objectives

After completing this exercise, you should be able to:

* Set up a backend project (e.g., Java Spring Boot, Node.js Express, etc.) with all required dependencies for
  data persistence and unit testing
* Implement ESBot's core domain entities (e.g., as JPA-annotated classes) consistent with the
  data base model
* Understand and document the relationships between ESBot domain entities
* Write meaningful unit tests (e.g., using JUnit 5, pytest, jest, etc.) that cover entity construction, validation
  constraints, and relationship behaviour
* Distinguish domain entities (persisted data) from service abstractions (e.g., the
  AI inference interface), and understand why that distinction matters for testability

---

## Pre-requisites

You need to have access and/or installed the following tools:

* Backend technology of your tech stack decision from Exercise 1 (e.g., Java Spring Boot, Node.js Express, etc.) 
* A build tool (e.g., Maven, Gradle, npm whichever your team selected)
* An IDE with backend technology support (e.g., IntelliJ IDEA, VS Code with Java extensions, etc.)
* Access to a local or containerized database instance (a pre-configured Docker Compose
  setup is for a containerized postgres database is available in `.devcontainer/docker-compose.yml`)
* The ESBot application description in `docs/esbot.md`
* Your results from Exercise 2 (`docs/spec/requirements.md`, `docs/spec/quality.md`)

---

## Exercise 4.1 (10 Points): Project Setup and Environment Configuration

**Objective:** Create a properly configured backend project that
includes all necessary dependencies for persistence (e.g.,Spring Data JPA, PostgreSQL driver),
unit testing (e.g., JUnit 5, pytest, jest, etc.), and application configuration.

Your setup must satisfy the following conditions:

* The project compiles without errors and all required dependencies are resolved
* A database connection to the database you described in your tech stack as part of exercise 1 is configured (e.g., via `application.properties`
  or `application.yml`), with a separate test profile that uses an in-memory database or
  a Testcontainers-based instance so unit/integration tests do not require
  a running production database
* The test framework you selected from your tech stack decision from Exercise 1 is the test framework; confirm this is correctly wired into the build tool
* A simple "smoke test" (e.g., a Spring context load test) passes successfully
* All setup steps and any required environment variables are documented in your
  repository (e.g., in `README.md` or a `docs/setup.md` file)

**Expected Deliverables:** A properly configured backend project skeleton with all
required dependencies for persistence and unit testing. The initial project setup must
be reproducible from your repository without manual configuration steps.

---

## Exercise 4.2 (10 Points): Core Domain Model Implementation

**Objective:** Implement the core domain entities for *ESBot*.

Based on `docs/esbot.md` and your specification, define a **minimal but complete**
domain model for persistence. The following are **candidate core models** (recommended
baseline), but teams may adapt naming and decomposition when justified:
`UserSession`, `Message`, `QuizRequest`, `QuizItem`, `SubmittedAnswer`,
`EvaluationResult`.

For the ESBot baseline architecture, persistence is expected in PostgreSQL with a
relational model. If your team has previously justified a different storage model in the
project documentation, keep the same conceptual entities and relationships but document
how they are mapped in your storage technology.

**Expected Deliverables:** Implementation of your selected core entities with mapped
relationships, and appropriate validation constraints (e.g., `@NotNull`,
`@NotBlank` or equivalent in your stack). Helper methods for entity construction and
relationship management are encouraged. Document your design decisions in
`docs/spec/data-model.md`, including:
1. the final list of entities you selected,
2. relationship cardinalities,
3. persistence mapping strategy (relational or alternative, with justification),
4. and an entity-relationship/data-model diagram (text-based or drawn).

---

## Exercise 4.3 (15 Points): Unit Testing the Domain Models

**Objective:** Develop a comprehensive suite of unit tests for the ESBot domain
entities using a testing framework matching your tech stack (e.g., Java -> Jupiter; Python -> pytest, etc.). Test classes must be created for each entity you implemented
in Exercise 4.2 and cover the following scenarios:

* **Object creation with valid data** – verify that an entity can be instantiated with
  all required fields and that getters return the expected values
* **Validation constraints** – verify that invalid or missing required fields are
  detected (e.g., null `content` on `Message`, null `topic` on `QuizRequest`)
* **Relationships between entities** – verify that bidirectional associations are
  consistent (e.g., a `Message` added to a `UserSession` is retrievable from the
  session's message list, and vice versa)
* **Helper method and factory logic** – if you defined helper methods for constructing
  or updating entities, test those explicitly

**Constitution alignment:** These unit tests run entirely without a database and
without calling any AI service. All AI-related behaviour is out of scope for this
exercise. 

**Test class naming convention:** Follow the naming conventions of the tech 
stack you used. Check the official documentation of your backend technology
to figure out the structure (e.g.,`<EntityName>Test.java` placed under
`src/test/java` following the same package structure as the source, etc).

**Expected Deliverables:** A complete unit test class for each entity from Exercise 4.2.
All tests must pass. The test suite must be executable via the build tool (e.g.,
`./mvnw test` or `./gradlew test`) without any external services running.
Provide documentation and instructions on how to run your tests.

---

## Submission

Submit your findings in form of a link to your repository via moodle.
