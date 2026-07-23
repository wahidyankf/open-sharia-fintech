"""Example 6: OO Word Count."""


class WordCounter:  # => bundles state (the tally) with the behavior that acts on it (co-05)
    def __init__(self) -> None:  # => constructor: every instance starts with its own private tally
        self._tally: dict[str, int] = {}  # => state lives INSIDE the object, not floating in main()

    def add(self, word: str) -> None:  # => behavior #1: mutate this object's own state
        self._tally[word] = self._tally.get(word, 0) + 1  # => bump the count for this instance only

    def result(self) -> dict[str, int]:  # => behavior #2: read this object's own state
        return dict(self._tally)  # => a defensive copy -- callers can't mutate our internal box


counter = WordCounter()  # => construct one instance with its own private tally
for word in "the cat sat on the mat the cat ran".split():  # => same sentence as example 1
    counter.add(word)  # => state and behavior are bundled together -- no separate loop+dict pair

print(counter.result()["the"])  # => read the count back out via the method, not a bare dict access
# => Output: 3
print(counter.result()["cat"])  # => same second count as the imperative version
# => Output: 2

other = WordCounter()  # => a second, independent instance
other.add("solo")  # => mutating `other` never touches `counter`'s state
print(counter.result()["the"], other.result())  # => the two instances stay fully isolated
# => Output: 3 {'solo': 1}
