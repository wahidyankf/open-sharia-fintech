"""Kata 5 (after): Stack HOLDS a list instead of BEING one -- insert() is simply gone."""


class Stack:
    def __init__(self) -> None:
        self._items: list[int] = []

    def push(self, item: int) -> None:
        self._items.append(item)

    def pop_top(self) -> int:
        return self._items.pop()


s = Stack()
s.push(1)
s.push(2)
print(s._items)
print(hasattr(s, "insert"))
