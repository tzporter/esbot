# Test Design Document

## Exercise 7.1: Black-Box Testing Techniques

### Step 1 & 2: Equivalence Class Partitioning (ECP) and Boundary Value Analysis (BVA)

#### Parameter 1: `topic`
**Rules:** The topic string must be between 3 and 100 characters (inclusive).

| Parameter | Class ID | Class Type | Partition Description | Representative Test Value |
|-----------|----------|------------|-----------------------|--------------------------|
| `topic`   | EC-T-1   | Valid      | Length is between 3 and 100 characters | "Software Testing" (16 chars) |
| `topic`   | EC-T-2   | Valid      | Length is between 3 and 100 characters | "CPU" (3 chars) |
| `topic`   | EC-T-3   | Valid      | Length is between 3 and 100 characters | "LLMs" (4 chars) |
| `topic`   | EC-T-4   | Invalid    | Length is less than 3 characters | "AI" (2 chars) |
| `topic`   | EC-T-5   | Valid      | Length is between 3 and 100 characters | "A" repeated 99 times |
| `topic`   | EC-T-6   | Valid      | Length is between 3 and 100 characters | "A" repeated 100 times |
| `topic`   | EC-T-7   | Invalid    | Length is greater than 100 characters | "A" repeated 101 times |

**Justification for `topic` classes:**
- **EC-T-1 (Valid):** The representative value "Software Testing" is 16 characters long, which safely falls within the valid range. This tests the typical expected input for FR-003.
- **EC-T-2 (Valid):** The representative value "CPU" is 3 characters long, which acts as the boundary value just inside the minimum length (3). This verifies that the system accepts the minimum valid input (NFR-10.2).
- **EC-T-3 (Valid):** The representative value "LLMs" is 4 characters long, which safely falls within the valid range. This tests the typical expected input for FR-003.
- **EC-T-4 (Invalid):** The representative value "AI" is 2 characters long, which acts as the boundary value just outside the minimum length (3). This verifies that the system rejects overly short inputs (NFR-10.2).
- **EC-T-5 (Valid):** The representative value of 99 "A" characters is the boundary value just inside the maximum length (100). This verifies that the system accepts the maximum valid input (NFR-10.2).
- **EC-T-6 (Valid):** The representative value of 100 "A" characters is the maximum valid input. This verifies that the system accepts the maximum valid input (NFR-10.2).
- **EC-T-7 (Invalid):** The representative value of 101 "A" characters is the boundary value just outside the maximum length (100). This ensures the system rejects excessively long input to prevent prompt injection or resource strain (NFR-10.2).

#### Parameter 2: `count`
**Rules:** Must be an integer between 1 and 10 (inclusive).

| Parameter | Class ID | Class Type | Partition Description | Representative Test Value |
|-----------|----------|------------|-----------------------|--------------------------|
| `count`   | EC-C-1   | Invalid    | Integer less than 1 | 0 |
| `count`   | EC-C-2   | Valid      | Integer between 1 and 10 | 1 |
| `count`   | EC-C-3   | Valid      | Integer between 1 and 10 | 5 |
| `count`   | EC-C-4   | Valid      | Integer between 1 and 10 | 10 |
| `count`   | EC-C-5   | Invalid    | Integer greater than 10 | 11 |
| `count`   | EC-C-6   | Invalid    | Non-integer / text format | "five" |

**Justification for `count` classes:**
- **EC-C-1 (Invalid):** The value 0 acts as the concrete lower boundary value just outside the valid range. It ensures the system safely rejects a request for zero questions (NFR-10.2).
- **EC-C-2 (Valid):** The value 1 acts as the concrete lower boundary value just inside the valid range. It ensures the system accepts the minimum valid input (NFR-8.3).
- **EC-C-3 (Valid):** The value 5 represents a typical integer within the valid range, acting as a standard quiz request for FR-003.
- **EC-C-4 (Valid):** The value 10 acts as the concrete upper boundary value just inside the valid range. It ensures the system accepts the maximum valid input (NFR-8.3).
- **EC-C-5 (Invalid):** The value 11 acts as the concrete upper boundary value just outside the valid range. It prevents excessive load by verifying too many questions cannot be requested (NFR-8.3).
- **EC-C-6 (Invalid):** The value "five" verifies that the system correctly enforces data types and rejects non-numeric input (NFR-10.2).

#### Parameter 3: `difficulty`
**Rules:** Must be one of `easy`, `medium`, or `hard`.

| Parameter | Class ID | Class Type | Partition Description | Representative Test Value |
|-----------|----------|------------|-----------------------|--------------------------|
| `difficulty` | EC-D-1 | Valid      | Value is exactly "easy" | "easy" |
| `difficulty` | EC-D-2 | Valid      | Value is exactly "medium" | "medium" |
| `difficulty` | EC-D-3 | Valid      | Value is exactly "hard" | "hard" |
| `difficulty` | EC-D-4 | Invalid    | Any string other than accepted values | "expert" |
| `difficulty` | EC-D-5 | Invalid    | Empty or null value | "" |
| `difficulty` | EC-D-6 | Invalid    | Empty or null value | null |


**Justification for `difficulty` classes:**
- **EC-D-1, EC-D-2, EC-D-3 (Valid):** The discrete values "easy", "medium", and "hard" are the only valid choices, so each forms its own partition. They map to FR-003 for generating the appropriate quiz difficulty. No numeric boundaries exist.
- **EC-D-4 (Invalid):** The value "expert" checks any valid string not in the enumerated set, ensuring the system defaults or rejects unhandled difficulties (NFR-10.2).
- **EC-D-5 (Invalid):** An empty string represents the missing string value edge case, ensuring the system handles missing required data (NFR-10.2).
- **EC-D-6 (Invalid):** A null value represents the non-string edge case, ensuring the system handles missing required data (NFR-10.2).

---

### Step 3: Decision Table for Answer Evaluation

The answer evaluation feature (FR-004) generates feedback based on three main conditions:
1. **Answer correctness:** Correct (C), Partially correct (P), Incorrect (I)
2. **Answer is empty or blank:** Yes (Y), No (N)
3. **Quiz item still exists in session:** Yes (Y), No (N)

| Rule | C1: Correctness | C2: Empty | C3: Exists | Expected Action / Output | Requirement / Edge Case |
|------|-----------------|-----------|------------|--------------------------|-------------------------|
| R1   | -               | -         | N          | Return controlled error: "Quiz item not found or expired" | FR-4 / Edge case: session expired / missing item |
| R2   | -               | Y         | Y          | Prompt user to provide an answer | FR-4 / Edge case: empty input |
| R3   | C               | N         | Y          | Provide positive feedback and mark item as solved | FR-4.1, FR-4.3 |
| R4   | P               | N         | Y          | Provide constructive feedback with hints | FR-4.1, FR-4.3 |
| R5   | I               | N         | Y          | Provide explanatory feedback with the correct answer | FR-4.1, FR-4.3 |

*(Note: The `-` denotes a "don't-care" condition. If the quiz item no longer exists, neither the correctness nor whether the answer is empty matter. If the answer is empty, correctness is irrelevant since it cannot be evaluated.)*


AI was used to assist in the creation of this document. All AI produced material has been thoroughly checked and edited.