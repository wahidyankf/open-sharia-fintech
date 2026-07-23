"""Example 51: The Mutable Class-Attribute Pitfall, Reproduced and Fixed."""


class BuggyCart:  # => begins the BuggyCart class body
    items: list[
        str
    ] = []  # => BUG: declared on the CLASS -- ONE list shared by every instance

    def add(self, item: str) -> None:  # => defines the add() method
        self.items.append(
            item
        )  # => looks like instance state, but mutates the SHARED list


class Cart:  # => begins the Cart class body
    def __init__(
        self,
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.items: list[
            str
        ] = []  # => FIX: a fresh list is created INSIDE __init__, per instance

    def add(self, item: str) -> None:  # => defines the add() method
        self.items.append(
            item
        )  # => now genuinely mutates only THIS instance's own list


if (
    __name__ == "__main__"
):  # => guards the demo so IMPORTING this module (for pytest) stays side-effect-free
    buggy_a, buggy_b = (
        BuggyCart(),
        BuggyCart(),
    )  # => two "separate" carts sharing one class list
    buggy_a.add(
        "apple"
    )  # => appends to the class-level list every BuggyCart instance sees
    print(buggy_b.items)  # => the bug: buggy_b sees buggy_a's item too
    # => Output: ['apple']

    fixed_a, fixed_b = (
        Cart(),
        Cart(),
    )  # => two GENUINELY separate carts, each with its own list
    fixed_a.add("apple")  # => appends to fixed_a's own list only
    print(fixed_b.items)  # => the fix: fixed_b's own list stays empty
    # => Output: []
    # => `items: list[str] = []` in the class body creates ONE list shared by every instance forever
