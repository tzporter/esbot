# Manual UI Test Report

**Tester Name:** Truman Porter
**Date:** 23-06-2026
**Environment:** 
- **OS:** Linux
- **Browser:** Firefox 150.0.1 (64-bit)
- **Deployment:** Docker Compose (`esbot-frontend-app` on port 8501, `esbot-backend-app` on port 8000)
- **LLM Configuration:** `LLM_PROVIDER=real` (Groq API, `llama-3.1-8b-instant`)

---

## Test Case: TC-UI-01
**Scenario Mapping:** Successfully ask a course question and receive an explanation (`ask_question.feature`)

### Steps Performed
1. Navigate to `http://localhost:8501`.
2. Enter "Python Basics" into the "New Session Title" input and click "Create Session".
3. Select the "Python Basics" session from the sidebar.
4. Go to the "💬 Explanations & Chat" tab.
5. Type "Explain what are basic math operations in python" into the chat input and press enter.

### Expected Result
- The message "Explain what are basic math operations in python" appears as a user message bubble.
- The UI shows a loading spinner indicating analysis.
- The assistant replies with a structured explanation about math operations in python.

### Actual Result
- The expected steps were followed and the expected result was achieved. The user message appeared, A loading spinner appeared below it, then the AI response appeared in place of the loading spinner.
- The AI response was structured, providing a clear and concise explanation of basic math operations in Python. It included well-formatted and clear explanations, and code examples.

### Status
**Pass**

---

## Test Case: TC-UI-02
**Scenario Mapping:** Successfully request and receive a quiz on a valid topic (`request_quiz.feature`)

### Steps Performed
1. Ensure you are in an active session (e.g., "German Basics").
2. Switch to the "📝 AI Knowledge Quiz" tab.
4. Enter "Python Data Types" into the topic input.
5. Click the "✨ Generate AI Quiz" button.

### Expected Result
- The UI shows a loading spinner.
- A success toast "Quiz loaded!" appears.
- The new quiz is automatically added to the dropdown and selected.
- The quiz questions (e.g., "What is the data type of the value 42?") are displayed on the screen with input fields.

### Actual Result
- The expected steps were followed and the expected result was mostly achieved. The UI shows a loading spinner. A success toast never appeared. The new quiz is automatically added to the dropdown and selected. The quiz questions (e.g., "What is the data type of the value 42?") are displayed on the screen with input fields.
- The quiz questions were formatted as expected, with a reasonable variety of questions. However all questions required single answer responses. A mix of question types would be better.
- The lack of success toast is not a critical issue but it would be nice to have.


### Status
**Pass**

---

## Test Case: TC-UI-03
**Scenario Mapping:** Successfully submit and evaluate a correct answer (`evaluate_answer.feature`)

### Steps Performed
1. Continuing from TC-UI-02, locate the first quiz question (e.g., "What is the data type of the number 5 in Python").
2. Type the correct answer (e.g., "int") into the answer input field.
3. Click the "Submit Answer" button below the input.

### Expected Result
- The UI shows a loading state ("Evaluating response...").
- The input field becomes disabled so the answer cannot be changed.
- A success message appears saying "✅ **Correct!**" along with the AI's feedback.
- If you switch to another tab and come back, the answer and feedback are preserved.

### Actual Result
- The expected steps were followed and the expected result was achieved. The UI shows a loading state ("Evaluating response..."). The input field becomes disabled so the answer cannot be changed. A success message appears saying "✅ **Correct!**" along with the AI's feedback.
- The feedback was clear and concise ("Your answer is correct. The data type of the number 5 in Python is indeed int."). However, it could have benefited from a more thorough explanation of why the answer was correct. For example, it could have provided a link to the documentation or a more detailed explanation of the data type.

### Status
**Pass**

---

## Reflection on Manual Testing
Manual testing is simple and straightforward. However it is also tedious and error prone, especially when setting up the initial state for each test. Test TC-UI-03 requires two other tests to be run first, which makes it more tedious. In addition, Manually checking the correctnes of the AI responses is time consuming and error prone.

Manual testing did help provide insights into how the UI and AI responses could be improved, that automatic testing could not provide. For example, we found that the AI responses could be improved by providing more thorough explanations, and the UI could be improved by sorting workspaces reverse chronologically by last activity, instead of chronologically by first creation. Automatic testing could not provide these insights because it would not have been able to evaluate the correctness of the AI responses, and it would not have been able to identify that the UI was unclear.

Automation could help with the tedious parts of manual testing, such as setting up the initial state for each test, or carrying out entire E2E test scenarios. However, it could not provide all the insights that manual testing did. Ideally, we would use automation for the tedious parts of manual testing, and manual testing for the parts that require human judgment. Automatic testing could be ran first and once all errors are fixed, manual testing could be used to ensure that the UI and AI responses are improved.

**AI was used to generate the outline for this report. All results, and the reflection were written by Truman Porter.**