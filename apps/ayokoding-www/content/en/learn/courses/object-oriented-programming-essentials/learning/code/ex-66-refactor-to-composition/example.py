"""Example 66: Refactoring Stack to Composition."""


class Stack:  # => no longer subclasses list -- HOLDS one instead
    def __init__(
        self,
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self._items: list[
            int
        ] = []  # => a private collaborator, not an inherited interface

    def push(self, item: int) -> None:  # => defines the push() method
        self._items.append(
            item
        )  # => delegates to the list, but does not EXPOSE the list

    def pop(self) -> int:  # => defines the pop() method
        return self._items.pop()  # => returns this value to the caller

    def peek(self) -> int:  # => defines the peek() method
        return self._items[
            -1
        ]  # => only push/pop/peek exist -- insert() is simply not here


s: Stack = Stack()  # => constructs s
s.push(1)
s.push(2)
print(s.peek())  # => reads the top without removing it
# => Output: 2
print(s.pop())  # => removes and returns the top
# => Output: 2
print(
    hasattr(s, "insert")
)  # => the leaked method from Example 65 no longer exists on Stack
# => Output: False
# => Composing a `list` as `self._items` and forwarding only `push`/`pop`/`peek` gives `Stack` an interface entirely of its own choosing
