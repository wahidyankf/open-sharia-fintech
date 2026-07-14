"""Example 68: Typed Signatures, ruff-clean."""

# Defers annotation evaluation (not needed on 3.14, kept here for portability).
from __future__ import annotations


# `str | None` (PEP 604) is the modern spelling of `Optional[str]`.
def join_names(names: list[str], sep: str | None = None) -> str:
    # sep defaults to ", " when the caller omits it or passes None explicitly.
    separator = sep if sep is not None else ", "
    return separator.join(names)  # => joins names using the resolved separator


# ruff-clean means `ruff check` reports zero findings against this file.
print(join_names(["Ada", "Grace"]))  # => Output: Ada, Grace
