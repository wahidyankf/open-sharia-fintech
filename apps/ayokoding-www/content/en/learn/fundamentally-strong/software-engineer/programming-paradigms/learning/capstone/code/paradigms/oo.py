"""Capstone -- OO: Sequential Transaction Processor (co-05, co-06)."""


class TransactionProcessor:  # => bundles balance + rejection tracking as encapsulated instance state
    def __init__(self, starting_balance: int) -> None:
        self._balance = starting_balance  # => private state, only this class's own methods touch it
        self._rejected: list[int] = []  # => private state: which transaction indices were rejected

    def apply(self, index: int, amount: int) -> None:  # => the ONE sanctioned way to process a transaction
        if self._balance + amount < 0:  # => the same rejection rule as the imperative version
            self._rejected.append(index)  # => reject: record it, balance untouched
        else:
            self._balance += amount  # => accept: mutate this instance's own balance

    def process_all(self, amounts: list[int]) -> tuple[int, list[int]]:  # => drive apply() over every transaction
        for index, amount in enumerate(amounts):  # => same ordering guarantee as the imperative version
            self.apply(index, amount)
        return self._balance, list(self._rejected)  # => a defensive copy of the rejected list


if __name__ == "__main__":
    amounts = [50, -200, 30, -1000, 20]  # => identical shared input to the imperative version
    processor = TransactionProcessor(starting_balance=100)
    final_balance, rejected = processor.process_all(amounts)
    print(final_balance, rejected)  # => must match the imperative version exactly
    # => Output: 200 [1, 3]
