"""Capstone -- Imperative: Sequential Transaction Processor (co-01, co-02)."""


def process_transactions_imperative(amounts: list[int], starting_balance: int) -> tuple[int, list[int]]:
    # => explicit loop, mutable balance, mutable rejected list -- the direct imperative shape
    balance = starting_balance  # => mutable running balance, updated in place as we go
    rejected: list[int] = []  # => mutable accumulator of rejected transaction indices
    for index, amount in enumerate(amounts):  # => step through transactions one at a time, in order
        if balance + amount < 0:  # => would this transaction drive the balance negative?
            rejected.append(index)  # => reject: record the index, balance stays UNCHANGED this step
        else:
            balance += amount  # => accept: mutate the running balance in place
    return balance, rejected  # => the final mutated state, handed back as a plain tuple


if __name__ == "__main__":
    amounts = [50, -200, 30, -1000, 20]  # => shared capstone input across all four paradigms
    final_balance, rejected = process_transactions_imperative(amounts, starting_balance=100)
    print(final_balance, rejected)  # => 100+50=150(ok), -200 rejected, +30=180(ok), -1000 rejected, +20=200(ok)
    # => Output: 200 [1, 3]
