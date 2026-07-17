"""Example 30: Four Ways -- OO."""


class WordFrequencyCounter:  # => way #2 of 4: state and behavior bundled in a class
    def __init__(self) -> None:  # => constructor runs once, before count() is ever called
        self._counts: dict[str, int] = {}  # => private state, only this class's methods touch it
        # => starts empty -- every instance gets its own independent dict, never shared

    def count(self, text: str) -> "WordFrequencyCounter":  # => behavior: process text, mutate self
        for word in text.split():  # => same tokenization as example 29
            self._counts[word] = self._counts.get(word, 0) + 1  # => mutate this instance's own state
        return self  # => returning self allows chaining, a common OO idiom

    def result(self) -> dict[str, int]:  # => behavior: read this instance's own state
        return dict(self._counts)  # => defensive copy


sample = "red blue red green blue red"  # => identical sample to example 29
counter = WordFrequencyCounter().count(sample)  # => construct, then chain the count() call
print(counter.result())  # => must match example 29's dict exactly
# => Output: {'red': 3, 'blue': 2, 'green': 1}
