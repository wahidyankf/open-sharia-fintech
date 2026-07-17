"""Kata 1 (after): mutable-state aliasing bug fixed -- each instance gets its own fresh list."""


class WordCounter:
    def __init__(self, words: list[str] | None = None) -> None:
        self.words: list[str] = words if words is not None else []  # fresh list per instance, never shared

    def add(self, word: str) -> None:
        self.words.append(word)


first = WordCounter()
first.add("alpha")
second = WordCounter()
second.add("beta")
print(first.words)
print(second.words)
