import os
from groq import Groq
from .base import LLMClient
import json
from .prompts import BASE_PROMPT

class GroqAIClient(LLMClient):
    def __init__(self, model_name="llama-3.3-70b-versatile"):
        self.client = Groq(
            api_key=os.environ.get("LLM_API_KEY"),
        )
        self.model_name = model_name

    def extract_fields(self, text: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{
                "role": "user",
                "content": BASE_PROMPT.replace("{{content}}", text)
            }],
            temperature=0.2,
        )
        response_text = response.choices[0].message.content
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            return {}
