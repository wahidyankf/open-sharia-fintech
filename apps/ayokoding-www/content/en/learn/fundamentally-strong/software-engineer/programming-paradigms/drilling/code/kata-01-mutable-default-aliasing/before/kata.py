"""Kata 1 (before): mutable-state aliasing bug -- a mutable default argument is shared across calls."""


class WordCounter:
    def __init__(self, words: list[str] = []) -> None:  # SMELL: mutable default shared across every instance
        self.words = words

    def add(self, word: str) -> None:
        self.words.append(word)


first = WordCounter()
first.add("alpha")
second = WordCounter()  # meant to start EMPTY -- but shares the same default list object as `first`
second.add("beta")
print(first.words)
print(second.words)
