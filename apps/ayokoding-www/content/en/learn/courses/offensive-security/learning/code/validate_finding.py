"""Validate an actionable report structure for synthetic lab findings only."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Finding:
    reproduction: str
    impact: str
    severity: str
    remediation: str


def is_actionable(finding: Finding) -> bool:
    """Require the four report sections, not operational exploitation detail."""
    return all(value.strip() for value in vars(finding).values())


if __name__ == "__main__":
    local_finding = Finding(
        reproduction="Review the bundled synthetic owner-mismatch record.",
        impact="A fictional peer record could be disclosed in the local lab.",
        severity="High in this deliberately vulnerable training model.",
        remediation="Authorize subject, action, and object on every server request.",
    )
    assert is_actionable(local_finding)
    print("synthetic local finding is actionable")
