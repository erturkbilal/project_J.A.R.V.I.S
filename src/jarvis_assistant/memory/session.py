from __future__ import annotations

from collections import deque


class ShortTermMemory:
    def __init__(self, max_turns: int = 8) -> None:
        self._turns: deque[dict[str, str]] = deque(maxlen=max_turns * 2)

    def add(self, role: str, content: str) -> None:
        self._turns.append({"role": role, "content": content})

    def to_messages(self) -> list[dict[str, str]]:
        return list(self._turns)
