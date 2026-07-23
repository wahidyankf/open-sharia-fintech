"""Example 28: the shared workload both profiling methods below are pointed at."""

from __future__ import annotations


def render_widget(name: str, count: int) -> str:
    return "-".join(f"{name}{i}" for i in range(count))


def render_page(widgets: list[tuple[str, int]]) -> list[str]:
    return [render_widget(name, count) for name, count in widgets]


def run_workload() -> None:
    widgets = [("btn", 4000)] * 50
    render_page(widgets)
