"""Kata 5 (before): Stack(list) leaks the full list interface, including insert()."""


class Stack(list[int]):
    def push(self, item: int) -> None:
        self.append(item)

    def pop_top(self) -> int:
        return self.pop()


s = Stack()
s.push(1)
s.push(2)
s.insert(0, 99)  # never meant to be part of a stack's interface
print(list(s))
