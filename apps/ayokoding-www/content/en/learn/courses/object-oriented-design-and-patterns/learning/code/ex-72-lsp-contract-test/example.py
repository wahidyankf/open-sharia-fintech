"""Example 72: LSP -- Contract Test.

co-03: a single contract-test suite that ANY Stack implementation must satisfy --
LIFO push/pop order, size tracking, and raising on pop-from-empty. A conforming
subtype passes every check; a subtype that violates the Liskov substitution
principle (silently behaving like a queue instead of a stack) fails the SAME
contract, without writing a separate test file per implementation.
"""

from __future__ import annotations  # => defers type-hint evaluation, not strictly required here but kept for consistency

from typing import Protocol  # => Protocol declares the structural contract every Stack implementation must satisfy


# => this Protocol is the SINGLE source of truth both implementations below are measured against
# => four clauses total: push, pop, is_empty, size -- run_stack_contract below exercises all four
class StackLike(Protocol):  # => the contract every Stack implementation promises to honor
    def push(self, item: int) -> None: ...  # => clause: adds one item
    def pop(self) -> int: ...  # => clause: removes and returns the MOST RECENTLY pushed item
    def is_empty(self) -> bool: ...  # => clause: reports whether any items remain
    def size(self) -> int: ...  # => clause: reports how many items remain


# => ListStack and BuggyQueueAsStack both satisfy StackLike STRUCTURALLY -- only the contract test below catches the difference
class ListStack:  # => a conforming implementation -- true last-in-first-out order
    def __init__(self) -> None:  # => the constructor
        self._items: list[int] = []  # => the backing storage, empty at construction

    def push(self, item: int) -> None:  # => satisfies StackLike's push clause
        self._items.append(item)  # => appends to the END of the list -- pop() below removes from here too

    def pop(self) -> int:  # => satisfies StackLike's pop clause
        if self.is_empty():  # => satisfies the "raises on pop-from-empty" clause of the contract
            raise IndexError("pop from empty stack")  # => an honest failure, never a silent wrong answer
        return self._items.pop()  # => removes and returns the LAST item pushed -- LIFO

    def is_empty(self) -> bool:  # => satisfies StackLike's is_empty clause
        return len(self._items) == 0  # => true exactly when nothing has been pushed and not yet popped

    def size(self) -> int:  # => satisfies StackLike's size clause
        return len(self._items)  # => the current count of pushed-but-not-popped items


# => notice this class's method SIGNATURES are identical to ListStack's -- only pop()'s BEHAVIOR differs
class BuggyQueueAsStack:  # => LSP VIOLATION: looks like a Stack, secretly behaves like a queue (FIFO)
    def __init__(self) -> None:  # => the constructor -- identical to ListStack's
        self._items: list[int] = []  # => the backing storage, empty at construction

    def push(self, item: int) -> None:  # => IDENTICAL to ListStack.push -- the bug is not here
        self._items.append(item)  # => appends to the END of the list, same as ListStack

    def pop(self) -> int:  # => structurally satisfies StackLike's pop clause -- but VIOLATES its LIFO promise
        if self.is_empty():  # => still raises on empty, so this clause alone would pass
            raise IndexError("pop from empty stack")  # => an honest failure for the empty case
        return self._items.pop(0)  # => BUG: removes the FIRST item -- FIFO order, not LIFO

    def is_empty(self) -> bool:  # => IDENTICAL to ListStack.is_empty
        return len(self._items) == 0  # => same logic, same correctness

    def size(self) -> int:  # => IDENTICAL to ListStack.size
        return len(self._items)  # => same logic, same correctness


# => a type-level parameter, not an instance -- run_stack_contract works for ANY conforming class, unmodified
def run_stack_contract(make_stack: type[StackLike]) -> None:  # => the ONE contract every subtype must pass
    stack = make_stack()  # => constructs whichever implementation was passed in, generically
    # => the SAME four assertions below run for both ListStack and BuggyQueueAsStack -- only the outcome differs
    assert stack.is_empty()  # => clause 1: starts empty
    stack.push(1)  # => pushed first -- should be the LAST one popped, if LIFO holds
    stack.push(2)  # => pushed second
    stack.push(3)  # => pushed third and last -- should be the FIRST one popped, if LIFO holds
    assert stack.size() == 3  # => clause 2: size tracks pushes
    top = stack.pop()  # => the value under test -- LIFO demands this be 3
    assert top == 3, f"LSP violation: expected LIFO top 3, got {top}"  # => clause 3: LIFO order
    assert stack.size() == 2  # => clause 4: size tracks pops
    # => reaching this line without an AssertionError means every clause of the contract held


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    # => no separate ListStackTest / BuggyQueueAsStackTest classes exist -- one contract function serves both
    run_stack_contract(ListStack)  # => the SAME contract function, applied to the conforming implementation
    print("ListStack: contract satisfied")  # => reached only if every assertion above passed
    # => Output: ListStack: contract satisfied

    try:  # => catches the assertion failure so this demonstration can print it, instead of crashing
        run_stack_contract(BuggyQueueAsStack)  # => the SAME contract function, now applied to the buggy one
        print("BuggyQueueAsStack: contract satisfied")  # => unreached -- the LIFO assertion fails first
    except AssertionError as error:  # => catches the SAME contract's failure, without a separate test file
        print(f"BuggyQueueAsStack: contract VIOLATED -- {error}")  # => the LSP violation surfaces here
    # => Output: BuggyQueueAsStack: contract VIOLATED -- LSP violation: expected LIFO top 3, got 1
