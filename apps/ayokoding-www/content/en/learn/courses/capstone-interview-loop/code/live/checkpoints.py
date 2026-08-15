"""Tiny green increments for a narrated live-coding rehearsal."""


def add_checkpoint(completed: list[str], checkpoint: str) -> list[str]:
    """Return a new ordered list after naming a non-empty completed checkpoint."""
    if not checkpoint.strip():
        raise ValueError("checkpoint must name the increment")
    return [*completed, checkpoint]
