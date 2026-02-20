# J.A.R.V.I.S (Production-Oriented Personal AI Assistant)

This repository contains **Phase 1** of a serious, modular, local-first desktop assistant inspired by J.A.R.V.I.S.

> Main language: Python  
> LLM provider: OpenRouter API  
> Target runtime: Windows PC (local execution)

## Phase 1 Scope (Implemented)

- ✅ Core text chat loop
- ✅ OpenRouter chat completion integration
- ✅ Conversation context handling
- ✅ Short-term memory buffer (in-process)
- ✅ Basic long-term memory with SQLite
- ✅ Language detection
- ✅ Language override commands (`Answer in English`, `Türkçe konuş`, etc.)
- ✅ Preference storage foundation
- ✅ Learned command frequency tracking foundation

---

## High-Level Architecture

```text
UI (CLI for Phase 1)
  -> Assistant Runtime Orchestrator
      -> Language Service
      -> OpenRouter Client
      -> Memory Layer
           -> ShortTermMemory (session)
           -> MemoryStore (SQLite)
```

### Module communication

1. User enters text in UI (`ui/cli.py`).
2. Runtime (`core/assistant.py`) resolves response language using `core/language.py`.
3. Runtime stores user turn in SQLite (`memory/store.py`) and in short-term buffer (`memory/session.py`).
4. Runtime builds prompt + recent history and sends request via `clients/openrouter_client.py`.
5. Assistant response is persisted to memory and printed to the user.

---

## Project Structure

```text
project_J.A.R.V.I.S/
├─ .env.example
├─ pyproject.toml
├─ README.md
├─ data/
│  └─ (SQLite DB created at runtime)
├─ src/
│  └─ jarvis_assistant/
│     ├─ main.py
│     ├─ config.py
│     ├─ clients/
│     │  └─ openrouter_client.py
│     ├─ core/
│     │  ├─ assistant.py
│     │  └─ language.py
│     ├─ memory/
│     │  ├─ session.py
│     │  └─ store.py
│     ├─ ui/
│     │  └─ cli.py
│     └─ utils/
│        └─ crypto.py
└─ tests/
   └─ test_memory_store.py
```

---

## Installation

### 1) Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2) Install dependencies

```bash
pip install -e .
```

(For development tests)

```bash
pip install -e .[dev]
```

### 3) Configure environment variables

```bash
copy .env.example .env
```

Then update `.env`:

- `OPENROUTER_API_KEY` (required)
- `OPENROUTER_MODEL` (default is set)
- `APP_DB_PATH` (optional)
- `ENCRYPTION_KEY` (optional for now; generated at runtime if missing)

---

## Running Phase 1

```bash
python -m jarvis_assistant.main
```

Type `exit` to quit.

---

## Required Python Libraries (Phase 1)

- `python-dotenv` (environment loading)
- `requests` (OpenRouter HTTP)
- `langdetect` (automatic language detection)
- `cryptography` (encryption foundation)
- `rich` (clean terminal UI)
- `pytest` (dev/testing)

---

## Security Foundations

- API keys are loaded from `.env`.
- Runtime configuration uses environment variables.
- `utils/crypto.py` provides encryption/decryption utility for sensitive persistence in upcoming phases.
- System-command execution is intentionally not implemented in Phase 1 (reserved for secured tool-permission layer in Phase 3).

---

## Roadmap (Do not implement yet)

- **Phase 2**: Web search + retrieval + synthesis
- **Phase 3**: Tool registry + app control + email/notes/reminders + safe command execution permissions
- **Phase 4**: Voice I/O (STT/TTS), mode switching, state indicators
- **Phase 5**: Advanced learning, optimization, vector memory (Chroma/FAISS), personalization hardening

---

## Scalability Advice (for next phases)

1. Introduce strict interfaces (`Protocol`) for LLM, memory, and tools to swap implementations safely.
2. Separate command/event bus from UI so desktop app and CLI can share the same backend runtime.
3. Add structured logging + telemetry early to debug tool execution and latency.
4. Move from direct SQLite usage to repository pattern before vector DB and multi-agent behavior.
5. Add migration tooling (Alembic-like strategy for SQLite schema evolution).
6. Keep each phase independently runnable behind feature flags.

