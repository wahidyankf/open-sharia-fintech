"""Example 33: the workload behind this example's single .prof file."""

from __future__ import annotations


def normalize_sku(sku: str) -> str:
    return sku.strip().upper()


def load_catalog(n: int) -> list[str]:
    return [normalize_sku(f"  sku-{i}  ") for i in range(n)]


def index_catalog(skus: list[str]) -> dict[str, int]:
    return {sku: i for i, sku in enumerate(skus)}


def run() -> None:
    skus = load_catalog(100_000)
    index_catalog(skus)
