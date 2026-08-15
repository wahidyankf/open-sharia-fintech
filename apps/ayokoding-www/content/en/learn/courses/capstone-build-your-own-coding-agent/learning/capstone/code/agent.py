from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Action:
    tool: str
    path: str


def approve(workspace: Path, action: Action) -> bool:
    candidate = (workspace / action.path).resolve()
    return action.tool in {"read", "test"} and candidate.is_relative_to(
        workspace.resolve()
    )


def run_fake(workspace: Path, action: Action) -> dict[str, str]:
    if not approve(workspace, action):
        return {"status": "denied", "audit": f"denied:{action.tool}:{action.path}"}
    return {"status": "ok", "audit": f"approved:{action.tool}:{action.path}"}
