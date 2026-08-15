"""Ordered leaf index that exposes split boundaries for the teaching store."""

from __future__ import annotations

from bisect import bisect_left


class BTree:
    def __init__(self, leaf_size: int = 3) -> None:
        self.leaf_size = leaf_size
        self._items: list[tuple[str, dict[str, str]]] = []

    def insert(self, key: str, value: dict[str, str]) -> None:
        keys = [item[0] for item in self._items]
        position = bisect_left(keys, key)
        if position < len(self._items) and self._items[position][0] == key:
            self._items[position] = (key, value)
        else:
            self._items.insert(position, (key, value))

    def get(self, key: str) -> dict[str, str] | None:
        keys = [item[0] for item in self._items]
        position = bisect_left(keys, key)
        if position < len(self._items) and self._items[position][0] == key:
            return self._items[position][1]
        return None

    def scan(self) -> list[tuple[str, dict[str, str]]]:
        return list(self._items)

    def leaf_chunks(self) -> list[list[tuple[str, dict[str, str]]]]:
        return [
            self._items[index : index + self.leaf_size]
            for index in range(0, len(self._items), self.leaf_size)
        ]
