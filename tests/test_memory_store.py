from pathlib import Path

from jarvis_assistant.memory.store import MemoryStore


def test_memory_store_roundtrip(tmp_path: Path) -> None:
    db_file = tmp_path / "test.db"
    store = MemoryStore(db_file)

    store.save_message("user", "hello", "en")
    store.save_message("assistant", "hi", "en")
    history = store.recent_messages(limit=10)

    assert history[-1]["content"] == "hi"

    store.set_preference("theme", {"mode": "dark"})
    assert "dark" in (store.get_preference("theme") or "")

    store.remember_command("open chrome")
    store.remember_command("open chrome")
