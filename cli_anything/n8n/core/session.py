"""In-memory session state for the REPL."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Session:
    """Holds ephemeral state during an interactive REPL session."""

    base_url: str = ""
    api_key: str = ""
    last_workflow_id: str = ""
    last_execution_id: str = ""
    history: list[str] = field(default_factory=list)

    def record(self, cmd: str) -> None:
        self.history.append(cmd)
