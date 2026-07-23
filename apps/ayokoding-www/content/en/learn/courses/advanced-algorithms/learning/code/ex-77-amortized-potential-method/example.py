"""Example 77: The Potential Method -- Proving a Multi-Pop Stack is O(1) Amortized."""

# multipop(k) alone costs O(k) -- popping 1,000,000 elements from a 40-element
# stack ACTUALLY only pops 40, but a naive worst-case bound (O(k) per call)
# would wildly overcharge it. The potential method (co-02) uses Phi = stack
# size: amortized_cost = actual_cost + (Phi_after - Phi_before). Because Phi
# never goes negative and starts at 0, total actual cost across ANY sequence
# of operations is bounded by the sum of amortized costs -- each O(1).


class MultiPopStack:  # => a stack instrumented to report each op's ACTUAL cost
    def __init__(self) -> None:  # => an empty stack
        self.items: list[int] = []  # => the underlying storage

    def push(self, value: int) -> int:  # => returns the actual cost: always 1
        self.items.append(value)  # => a single O(1) append
        return 1  # => push always does exactly 1 unit of real work

    def multipop(self, k: int) -> int:  # => returns the actual cost: min(k, size)
        removed = min(k, len(self.items))  # => can NEVER pop more than what exists
        for _ in range(removed):  # => pops exactly as many as actually exist
            self.items.pop()  # => one real O(1) pop
        return removed  # => the REAL work done, regardless of how large k was


def potential(stack: MultiPopStack) -> int:  # => Phi(D) = current stack size
    return len(stack.items)  # => always >= 0, and 0 for an empty stack


stack = MultiPopStack()  # => the shared stack instance under test
amortized_costs: list[int] = []  # => one entry per operation call, in order
total_actual = 0  # => the TRUE sum of work done, op by op

BIG_K = 1_000_000  # => a deliberately absurd request -- far larger than the stack


def run_push(value: int) -> None:  # => wraps push with the potential-method bookkeeping
    global total_actual  # => accumulates the TRUE running total across all calls
    phi_before = potential(stack)  # => Phi BEFORE this operation runs
    actual = stack.push(value)  # => the operation's REAL cost
    phi_after = potential(stack)  # => Phi AFTER this operation runs
    amortized_costs.append(  # => opens the amortized-cost recording
        actual  # => this operation's real cost
        + (phi_after - phi_before)  # => actual cost plus the potential's own change
    )  # => THE potential-method formula
    total_actual += actual  # => accumulates the running TRUE total


def run_multipop(k: int) -> None:  # => wraps multipop with the same bookkeeping
    global total_actual  # => accumulates the TRUE running total across all calls
    phi_before = potential(stack)  # => Phi BEFORE this operation runs
    actual = stack.multipop(k)  # => the operation's REAL cost
    phi_after = potential(stack)  # => Phi AFTER this operation runs
    amortized_costs.append(  # => opens the amortized-cost recording
        actual + (phi_after - phi_before)
    )  # => THE potential-method formula
    total_actual += actual  # => accumulates the running TRUE total


for _ in range(40):  # => 40 pushes -- Phi climbs from 0 to 40
    run_push(1)  # => each push costs 1, actual and amortized
run_multipop(BIG_K)  # => actual cost is 40 (capped by stack size), NOT 1,000,000
for _ in range(25):  # => 25 more pushes
    run_push(1)  # => each push costs 1, actual and amortized
run_multipop(BIG_K)  # => actual cost is 25, again capped by size, not BIG_K
for _ in range(10):  # => 10 more pushes, building up potential again
    run_push(1)  # => each push costs 1, actual and amortized
run_multipop(3)  # => a NORMAL partial pop: k=3 is smaller than the stack's 10 elements
run_multipop(BIG_K)  # => pops the remaining 7

print(total_actual)  # => Output: 150 -- bounded by pushes+pops, NEVER by the huge k's
print(  # => opens the worst-case-amortized-cost print call
    max(amortized_costs)  # => the single worst-case amortized cost across all ops
)  # => Output: 2 -- EVERY single op costs at most 2, amortized
print(len(amortized_costs))  # => Output: 79 -- 75 pushes + 4 multipop calls

assert (  # => opens the exact-total-actual-cost check
    total_actual == 150  # => the exact expected total across every real pop/push
)  # => confirms actual work stayed proportional to real operations
assert (  # => opens the every-op-O(1)-amortized check
    max(amortized_costs) <= 2  # => no single operation ever amortizes above 2
)  # => THE PROOF: every op is O(1) amortized, push or multipop
assert total_actual <= 2 * len(  # => opens the 2x-bound comparison
    amortized_costs  # => the operation count, for the 2x-bound comparison
)  # => total actual cost never exceeds 2x the operation count
assert stack.items == []  # => the stack ends empty -- everything pushed got popped
print("ex-77 OK")  # => Output: ex-77 OK
