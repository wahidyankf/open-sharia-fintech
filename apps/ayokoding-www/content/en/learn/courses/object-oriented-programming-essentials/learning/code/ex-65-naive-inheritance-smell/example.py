"""Example 65: A Naive Stack(list) Leaks the Wrong Interface."""


class Stack(
    list[int]
):  # => "is-a list" -- inherits EVERY list method, not just stack operations
    def push(self, item: int) -> None:  # => defines the push() method
        self.append(item)  # => reuses list.append -- convenient, but see the leak below

    def pop_top(self) -> int:  # => defines the pop_top() method
        return self.pop()  # => reuses list.pop -- also convenient


s: Stack = Stack()  # => constructs s
s.push(1)  # => pushes 1 -- goes through the intended push() method
s.push(2)  # => pushes 2 -- still through the intended push() method
s.insert(0, 99)  # => LEAK: insert() was never meant to be part of a stack's interface
# => a real stack only supports push/pop at ONE end -- insert(0, ...) breaks that guarantee
print(list(s))  # => 99 was inserted at an arbitrary position, not pushed
# => Output: [99, 1, 2]
# => `class Stack(list[int])` inherits `list`'s ENTIRE public interface, not just the parts a stack conceptually needs
