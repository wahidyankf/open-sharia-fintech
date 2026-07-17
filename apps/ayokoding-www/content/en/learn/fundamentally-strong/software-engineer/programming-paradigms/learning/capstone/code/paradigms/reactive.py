"""Capstone -- Reactive: Sequential Transaction Processor (co-08, co-17)."""

from collections.abc import Callable


class ReactiveAccount:  # => a reactive source: rejections PUSH to subscribers automatically, no polling
    def __init__(self, starting_balance: int) -> None:
        self._balance = starting_balance  # => the account's current balance
        self._on_reject: list[Callable[[int], None]] = []  # => subscribers notified on every rejection

    def on_reject(self, fn: Callable[[int], None]) -> None:  # => register a rejection subscriber
        self._on_reject.append(fn)  # => append -- does NOT replay past rejections to a late subscriber

    def apply(self, index: int, amount: int) -> None:  # => process one transaction, reactively
        if self._balance + amount < 0:  # => the SAME rejection rule as the other three paradigms
            for fn in self._on_reject:  # => PUSH: every subscriber is notified automatically, right here
                fn(index)
        else:
            self._balance += amount  # => accept: update the balance

    def balance(self) -> int:  # => the only sanctioned way to read the current balance
        return self._balance


def process_transactions_reactive(amounts: list[int], starting_balance: int) -> tuple[int, list[int]]:
    account = ReactiveAccount(starting_balance)  # => construct the reactive source
    rejected: list[int] = []  # => a subscriber's own recorder -- filled ENTIRELY via the push callback below
    account.on_reject(lambda index: rejected.append(index))  # => subscribe BEFORE processing any transaction
    for index, amount in enumerate(amounts):  # => drive the reactive account through every transaction in order
        account.apply(index, amount)
    return account.balance(), rejected  # => `rejected` was never appended to directly -- only via the push


if __name__ == "__main__":
    amounts = [50, -200, 30, -1000, 20]  # => identical shared input to the other three paradigms
    final_balance, rejected = process_transactions_reactive(amounts, starting_balance=100)
    print(final_balance, rejected)  # => must match the other three paradigms exactly
    # => Output: 200 [1, 3]
