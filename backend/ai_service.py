import os
from openai import OpenAI
import json

get_quiz_template = """You are ESBot, a helpful learning assistant that generates quizzes.
When given a topic, you create a quiz with 3 questions of varying difficulty (easy, medium, hard).
Each question should have a clear answer.
Format your response as JSON with the following structure:
{
  "quiz": {
    "topic": "Topic Name",
    "questions": [
      { "question": "Question text", "answer": "Correct answer" },
      ...
    ]
  }
}"""


class AIService:
    def __init__(self):

        #LLM_PROVIDER env var can be set to "mock" to enable mock mode, which returns hardcoded responses without calling the real API. This is useful for testing and development without incurring API costs or needing network access.
        self.mock_mode = os.getenv("LLM_PROVIDER", "real") == "mock"

        if self.mock_mode:
            return

        self.api_key = os.getenv("GROQ_API_KEY", None)
        if self.api_key is None:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1", api_key=self.api_key
        )

    def get_explanation(self, prompt: str):

        if self.mock_mode:
            return f"[Mock Response] This is a deterministic explanation for your prompt: '{prompt}'"
        
        system_prompt = """You are ESBot, a helpful learning assistant.
When asked a question, you should respond with a clear and concise explanation.
If a user requests a quiz, respond with the JSON:
{ "status": "error", "message": "The quiz feature is not enabled. Please press the quiz button to enable it." }.
                """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                model="llama-3.1-8b-instant",
            )
            content = chat_completion.choices[0].message.content
            return content
        except Exception as e:
            print(f"Error calling Groq API: {e}", flush=True)
            raise ConnectionError("AI service is currently unavailable")

    def evaluate_answer(
        self,
        question: str,
        correct_answer: str,
        user_answer: str,
    ) -> dict:
        """
        Returns one of:
          {"is_correct": bool, "feedback": str}
          {"needs_clarification": True, "clarification_question": str}
        """

        if self.mock_mode:
            # Scenario A: Clear answer evaluation
            return {"is_correct": True, "feedback": f"[Mock Feedback] Great job! Your answer '{user_answer}' is correct."}
        
        system_prompt = """You are ESBot, a language learning assistant that evaluates student answers.

You must respond ONLY with a valid JSON object. No extra text, no markdown, no explanation outside the JSON.

If the student's answer is clear enough to evaluate, respond with:
{"is_correct": true, "feedback": "<your feedback>"}
or
{"is_correct": false, "feedback": "<your feedback>"}

If the answer is too ambiguous to evaluate, respond with:
{"needs_clarification": true, "clarification_question": "<your question>"}"""

        user_prompt = (
            f"Question: {question}\n"
            f"Correct answer: {correct_answer}\n"
            f"Student's answer: {user_answer}\n\n"
            f"Evaluate the student's answer and respond with JSON only."
        )

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                model="llama-3.1-8b-instant",
                temperature=0.0,  # deterministic output for consistent JSON
            )
            raw = chat_completion.choices[0].message.content.strip()

            # Strip accidental markdown code fences the model might add
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()

            result = json.loads(raw)

            # Validate the shape so callers always get a predictable dict
            if "needs_clarification" in result:
                if "clarification_question" not in result:
                    raise ValueError("Missing clarification_question in AI response")
            elif "is_correct" in result:
                if "feedback" not in result:
                    raise ValueError("Missing feedback in AI response")
            else:
                raise ValueError(f"Unexpected AI response shape: {result}")

            return result

        except json.JSONDecodeError as e:
            raise ValueError(f"AI returned non-JSON response: {e}")
        except Exception as e:
            if isinstance(e, (ValueError,)):
                raise

    def get_quiz(self, topic: str):
        if self.mock_mode:
            return {
                "quiz": {
                    "topic": topic,
                    "questions": [
                        { "question": "What is 2+2?", "answer": "4" }
                    ]
                }
            }
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": get_quiz_template},
                    {
                        "role": "user",
                        "content": f"Generate a quiz on the topic: {topic}",
                    },
                ],
                model="llama-3.1-8b-instant",
            )
            raw_content = response.choices[0].message.content.strip()

            # Strip accidental markdown code fences
            if raw_content.startswith("```"):
                raw_content = raw_content.split("```")[1]
                if raw_content.startswith("json"):
                    raw_content = raw_content[4:]
                raw_content = raw_content.strip()

            return json.loads(raw_content)
        except json.JSONDecodeError:
            raise Exception("Unstructured format")
        except Exception:
            raise ConnectionError("AI service is currently unavailable")
