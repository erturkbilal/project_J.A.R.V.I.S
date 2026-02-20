from __future__ import annotations

from dataclasses import dataclass

from jarvis_assistant.clients.openrouter_client import OpenRouterClient
from jarvis_assistant.core.language import LanguageService
from jarvis_assistant.memory.session import ShortTermMemory
from jarvis_assistant.memory.store import MemoryStore

SYSTEM_PROMPT = (
    "You are JARVIS, a serious and practical personal desktop AI assistant. "
    "Be concise, accurate, and action-oriented. "
    "If a language code is provided, respond in that language."
)


@dataclass(slots=True)
class AssistantRuntime:
    llm: OpenRouterClient
    language: LanguageService
    memory: MemoryStore
    short_memory: ShortTermMemory

    def respond(self, user_input: str) -> str:
        language_code = self.language.resolve_language(user_input)

        self.memory.save_message("user", user_input, language_code)
        self.short_memory.add("user", user_input)
        self.memory.remember_command(user_input)

        context = self.memory.recent_messages(limit=10)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "system",
                "content": f"Output language must be: {language_code}",
            },
            *context,
        ]

        assistant_output = self.llm.chat(messages)

        self.memory.save_message("assistant", assistant_output, language_code)
        self.short_memory.add("assistant", assistant_output)
        self.memory.set_preference("last_language", {"code": language_code})

        return assistant_output
