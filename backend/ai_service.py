import os
from openai import OpenAI

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
        self.api_key = os.getenv("GROQ_API_KEY", "mock_key")
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=self.api_key
        )

    def get_explanation(self, prompt: str):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are ESBot, a helpful learning assistant."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192",
            )
            return chat_completion.choices[0].message.content
        except Exception:
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
                model="llama3-8b-8192",
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
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", 
                     "content": get_quiz_template},
                    {"role": "user", "content": f"Generate a quiz on the topic: {topic}"}
                ],
                model="llama3-8b-8192",
            )
            return response.choices[0].message.content
        except Exception:
            raise ConnectionError("AI service is currently unavailable")