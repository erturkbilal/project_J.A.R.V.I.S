from __future__ import annotations

from rich.console import Console
from rich.panel import Panel

from jarvis_assistant.clients.openrouter_client import OpenRouterClient
from jarvis_assistant.config import load_settings
from jarvis_assistant.core.assistant import AssistantRuntime
from jarvis_assistant.core.language import LanguageService
from jarvis_assistant.memory.session import ShortTermMemory
from jarvis_assistant.memory.store import MemoryStore


def run_cli() -> None:
    console = Console()
    settings = load_settings()

    runtime = AssistantRuntime(
        llm=OpenRouterClient(api_key=settings.openrouter_api_key, model=settings.openrouter_model),
        language=LanguageService(),
        memory=MemoryStore(settings.app_db_path),
        short_memory=ShortTermMemory(),
    )

    console.print(Panel("[bold cyan]J.A.R.V.I.S Phase 1[/]\nType 'exit' to quit."))

    while True:
        user_input = console.input("\n[bold green]You:[/] ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            console.print("[yellow]Session ended.[/]")
            break

        console.print("[magenta]Thinking...[/]")
        try:
            answer = runtime.respond(user_input)
            console.print(f"[bold cyan]JARVIS:[/] {answer}")
        except Exception as exc:
            console.print(f"[bold red]Error:[/] {exc}")
