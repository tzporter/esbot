import os
from openai import OpenAI

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