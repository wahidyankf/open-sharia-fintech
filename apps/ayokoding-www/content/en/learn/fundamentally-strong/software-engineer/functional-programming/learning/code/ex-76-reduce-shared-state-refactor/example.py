"""Example 76: Refactoring Shared-Mutable Code to Pass State Explicitly."""

_shared_balance = (
    0  # => the BEFORE state: a module-level global every function silently depends on
)


def deposit_impure(
    amount: int,
) -> int:  # => reads AND writes the hidden global -- a shared-state trap
    global _shared_balance  # => declares intent to mutate the MODULE-level balance
    _shared_balance += (
        amount  # => any other function could ALSO be mutating this concurrently
    )
    return _shared_balance  # => the new, globally-visible balance


def deposit_pure(
    balance: int, amount: int
) -> int:  # => the AFTER state: balance passed explicitly
    return (
        balance + amount
    )  # => no globals, no hidden dependency -- callers control the state directly


_shared_balance = 0  # => resets the impure global before demonstrating it
impure_result_1 = deposit_impure(100)  # => mutates _shared_balance to 100
impure_result_2 = deposit_impure(
    50
)  # => mutates _shared_balance to 150 -- depends on the call BEFORE it

pure_result_1 = deposit_pure(0, 100)  # => explicit starting balance, explicit result
pure_result_2 = deposit_pure(
    pure_result_1, 50
)  # => explicit threading -- no hidden state anywhere

# => this refactor is functional-core/imperative-shell applied to a single function pair
print(
    impure_result_2 == pure_result_2
)  # => Output: True -- same final answer, radically different design
print(
    _shared_balance
)  # => Output: 150 -- the global STILL exists in the impure version
