"""Example 26: The Accounting Method -- Credits That Never Go Negative."""

# The accounting method (co-02) charges each operation a fixed AMORTIZED cost
# (here, 3 credits per append), banking the surplus over what the operation
# actually spends. A resize later "cashes in" that banked surplus to pay for
# copying every existing element -- the proof this works is that the credit
# balance never dips below zero, across the ENTIRE sequence of operations.


class AccountedArray:  # => a doubling array instrumented to track its credit ledger
    def __init__(self) -> None:
        self.capacity: int = 1  # => starts with room for 1 element
        self.size: int = 0  # => elements actually stored
        self.credit_balance: int = 0  # => the running amortized-credit ledger

    def append(self, value: int) -> None:  # => charges 3, an amortized O(1) cost
        actual_cost = 1  # => the baseline cost: writing one new element
        if self.size == self.capacity:  # => full -- a resize must happen first
            actual_cost += self.size  # => ALSO pays 1 per existing element it copies
            self.capacity *= 2  # => doubles capacity, same as Example 25
        self.credit_balance += 3  # => charges this append the fixed amortized rate
        self.credit_balance -= actual_cost  # => pays for whatever actually happened
        assert (
            self.credit_balance >= 0
        )  # => THE PROOF: banked credit always covers the real cost
        self.size += 1  # => one more element now stored


arr = AccountedArray()  # => starts empty
balances: list[int] = []  # => records the credit balance after every single append
for i in range(500):  # => 500 appends -- several of them trigger a doubling resize
    arr.append(i)  # => charges 3, pays the real cost, asserts balance >= 0 internally
    balances.append(arr.credit_balance)  # => snapshots the balance for inspection

print(min(balances))  # => Output: 2 -- the balance dips low but never below zero
print(arr.credit_balance)  # => Output: 489 -- the final leftover credit
print(arr.size)  # => Output: 500

assert min(balances) >= 0  # => confirms the balance NEVER went negative, at any point
assert arr.size == 500  # => confirms every append actually landed
print("ex-26 OK")  # => Output: ex-26 OK
