"""Parse synthetic local-lab evidence without making a network request."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_local_evidence(path: Path) -> dict[str, Any]:
    """Accept only the course's local localhost fixture."""
    evidence = json.loads(path.read_text(encoding="utf-8"))
    if evidence.get("authorization") != "I OWN THIS LAB":
        raise ValueError("owner authorization is missing")
    if evidence.get("target") not in {"localhost", "127.0.0.1"}:
        raise ValueError("target must be localhost or 127.0.0.1")
    return evidence


def summarize(evidence: dict[str, Any]) -> str:
    services = evidence["services"]
    findings = evidence["findings"]
    return f"local services={len(services)} findings={len(findings)} target={evidence['target']}"


if __name__ == "__main__":
    fixture = Path(__file__).with_name("lab-evidence.json")
    print(summarize(load_local_evidence(fixture)))
