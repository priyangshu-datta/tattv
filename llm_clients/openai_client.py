import os
import openai
from .base import LLMClient
from .prompts import BASE_PROMPT

class OpenAIClient(LLMClient):
    def __init__(self, model_name="gpt-3.5-turbo"):
        openai.api_key = os.getenv("LLM_API_KEY")
        self.model_name = model_name

    def extract_fields(self, text: str) -> dict:
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{
                "role": "user",
                "content": BASE_PROMPT.replace("{{content}}", text)
            }],
            temperature=0.2,
        )
        try:
            return eval(response["choices"][0]["message"]["content"])
        except Exception:
            return {}
