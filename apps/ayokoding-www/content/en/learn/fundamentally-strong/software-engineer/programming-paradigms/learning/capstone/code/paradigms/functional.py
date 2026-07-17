"""Capstone -- Functional: Sequential Transaction Processor (co-09, co-11)."""

from functools import reduce


def process_transactions_functional(amounts: tuple[int, ...], starting_balance: int) -> tuple[int, tuple[int, ...]]:
    # => a PURE fold: the accumulator is a plain (balance, rejected) tuple, REPLACED every step, never mutated
    def step(acc: tuple[int, tuple[int, ...]], indexed: tuple[int, int]) -> tuple[int, tuple[int, ...]]:
        balance, rejected = acc  # => unpack the immutable accumulator carried in from the previous step
        index, amount = indexed
        if balance + amount < 0:  # => the SAME rejection rule as the other three paradigms
            return balance, rejected + (index,)  # => a BRAND NEW tuple -- the old `rejected` is untouched
        return balance + amount, rejected  # => a BRAND NEW accumulator -- nothing mutated in place

    return reduce(step, enumerate(amounts), (starting_balance, ()))  # => fold over (index, amount) pairs


if __name__ == "__main__":
    amounts: tuple[int, ...] = (50, -200, 30, -1000, 20)  # => identical shared input, as an immutable tuple
    final_balance, rejected = process_transactions_functional(amounts, starting_balance=100)
    print(final_balance, list(rejected))  # => must match the other two paradigms exactly
    # => Output: 200 [1, 3]
