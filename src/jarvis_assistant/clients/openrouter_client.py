from __future__ import annotations

from dataclasses import dataclass

import requests


@dataclass(slots=True)
class OpenRouterClient:
    api_key: str
    model: str
    base_url: str = "https://openrouter.ai/api/v1/chat/completions"

    def chat(self, messages: list[dict[str, str]], temperature: float = 0.3) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
