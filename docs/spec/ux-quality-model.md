# UX Quality Model Mapping (ISO/IEC 25010)

This document maps the identified User Experience (UX) factors for the ESBot application to the ISO/IEC 25010 software quality characteristics. To ensure rigorous quality assurance, each UX expectation is translated into strictly measurable quality criteria and paired with a concrete verification method, avoiding any vague terminology.

### 1. UX Factor: Learnability and Intuitive Use

**ISO 25010 Characteristic(s):** Usability (Learnability, Appropriateness recognizability)

**Measurable Quality Criterion:** A first-time student user without prior exposure to ESBot must be able to locate the chat input field, submit a course-related query, and successfully interpret the AI's response within a maximum of 60 seconds. The interface must not require any external manuals or tutorials for this initial core interaction.

**Verification Method:** Scenario-based Usability Test (Cognitive Walkthrough). Conduct testing sessions involving a minimum of 5 first-time CS students. Use screen recording and a stopwatch to measure the Time-to-First-Successful-Interaction (TTFSI). The test passes only if 100% of participants complete the task in under 60 seconds.

### 2. UX Factor: Clarity and Comprehensibility

**ISO 25010 Characteristic(s):** Functional Suitability (Functional correctness, Functional appropriateness)

**Measurable Quality Criterion:** AI-generated responses designed for pedagogical purposes must maintain a strict structural format to ensure readability. Specifically, 100% of responses exceeding 100 words must incorporate formatting elements (e.g., bullet points, bold text for keywords, or numbered lists) to reduce cognitive load. Additionally, the content must have a 0% hallucination rate regarding the uploaded course context.

**Verification Method:** Expert Review and Automated Text Analysis. A domain expert (e.g., TA or Professor) will evaluate a randomized sample of 30 AI-generated outputs against the source material to verify factual correctness. Concurrently, an automated script will parse the Markdown output of the Groq API to assert the presence of formatting tags (e.g., `*`, `-`, `#`) in lengthy responses.

### 3. UX Factor: Information Efficiency

**ISO 25010 Characteristic(s):** Usability (Operability) / Performance Efficiency (Resource utilization)

**Measurable Quality Criterion:** When a student requests a summary or specific information, the system must deliver a concise response with a maximum word count threshold of 250 words, avoiding tangential information unless explicitly instructed to "elaborate". Furthermore, the UI must allow the user to trigger secondary actions (like "Generate Quiz") with a maximum of two clicks from the main chat interface.

**Verification Method:** Automated End-to-End (E2E) and Unit Testing. Develop automated test cases using Cypress to calculate the click-depth for core features, ensuring it never exceeds 2 clicks. Additionally, use backend unit tests with mocked Groq API calls to validate that the prompt engineering correctly restricts the LLM output length to the 250-word limit.

### 4. UX Factor: Trust and Transparency of AI Responses

**ISO 25010 Characteristic(s):** Reliability (Maturity) / Security (Authenticity, Integrity)

**Measurable Quality Criterion:** To foster appropriate trust, 100% of the AI-generated responses presented in the Streamlit frontend must be accompanied by a persistently visible disclaimer (e.g., "AI-generated content; verify with course materials"). Furthermore, if the AI references specific course materials, the exact source file or lecture slide must be explicitly cited in the output at least 95% of the time.

**Verification Method:** Automated UI Component Testing. Utilize a testing framework like Selenium to scrape the rendered Streamlit DOM in 50 simulated chat sessions. The test will automatically assert the presence of the disclaimer text block and search for regex patterns matching document citations within the AI's response text.

### 5. UX Factor: Error Handling

**ISO 25010 Characteristic(s):** Reliability (Fault tolerance, Recoverability) / Usability (User error protection)

**Measurable Quality Criterion:** The application must gracefully handle both external failures (e.g., Groq API timeout > 5 seconds) and user errors (e.g., malformed inputs). In such events, the Streamlit UI must absolutely not crash (0% crash rate). Instead, the system must intercept the error and display a clear, non-technical, and actionable error message to the user within 3 seconds of the failure.

**Verification Method:** Fault Injection and Chaos Testing. Intentionally block network requests to the external API or return HTTP 500 / malformed JSON responses during testing. Measure the backend's retry mechanisms and verify via E2E testing that the frontend renders the designated fallback error message component without halting the application state.
