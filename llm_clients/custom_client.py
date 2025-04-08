import os
from transformers import pipeline
from .base import LLMClient
import json
from .prompts import BASE_PROMPT

class CustomClient(LLMClient):
    def __init__(self, model_name="mistralai/Mistral-7B-Instruct-v0.2"):
        self.generator = pipeline(
            "text-generation",
            model=model_name,
            token=os.environ.get("LLM_API_KEY"),
            trust_remote_code=True,
        )

    def extract_fields(self, text: str) -> dict:
        prompt = BASE_PROMPT.replace("{{content}}", text)
        try:
            result = self.generator(prompt, max_new_tokens=512, do_sample=False)
            response_text = result[0]["generated_text"].split(prompt, 1)[-1].strip()
            return json.loads(response_text)
        except Exception:
            return {}
