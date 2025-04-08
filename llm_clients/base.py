from abc import ABC, abstractmethod

class LLMClient(ABC):
    @abstractmethod
    def extract_fields(self, text: str) -> dict:
        """
        Extract structured information from unstructured text.
        Returns a dict like:
        {
            "company_name": "...",
            "description": "...",
            ...
        }
        """
        pass
