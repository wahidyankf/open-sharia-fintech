# pyright: strict
"""Example 22: Transaction Atomicity -- all commit or all roll back. (co-11)

Two writes inside one transaction: when both succeed they commit together;
when a failure occurs MID-transaction, both roll back and neither write
survives. This is the ACID atomicity guarantee -- an all-or-nothing commit
boundary.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => a typed account -- avoids dict[str, str|int] inference problems
class Account:
    name: str  # => the account label (for readable write descriptions)
    balance: int  # => the balance mutated inside the transaction


@dataclass  # => co-11: a transaction collects writes and commits or rolls them back atomically
class Transaction:
    writes: list[str] = field(default_factory=list[str])  # => staged writes, in order
    committed: bool = False  # => whether the transaction reached commit


def transfer(from_account: Account, to_account: Account, amount: int) -> Transaction:
    # => co-11: two writes (debit + credit) that must be ATOMIC
    tx = Transaction()  # => open the transaction
    tx.writes.append(f"debit {from_account.name} {amount}")  # => stage write 1: debit
    if from_account.balance < amount:  # => a mid-transaction FAILURE (insufficient funds)
        return tx  # => co-11: rollback -- neither write is committed (committed stays False)
    from_account.balance -= amount  # => apply write 1
    tx.writes.append(f"credit {to_account.name} {amount}")  # => stage write 2: credit
    to_account.balance += amount  # => apply write 2
    tx.committed = True  # => co-11: both writes succeeded -> commit atomically
    return tx  # => the committed transaction


# Case A: enough funds -> both writes commit together.
alice = Account("alice", 100)  # => account 1
bob = Account("bob", 50)  # => account 2
ok = transfer(alice, bob, 30)  # => co-11: both writes land
print(f"success: committed={ok.committed}, alice={alice.balance}, bob={bob.balance}")  # => Output: True, 70, 80
print(f"  writes: {ok.writes}")  # => Output: both debit and credit

# Case B: insufficient funds -> failure mid-transaction -> both roll back.
carol = Account("carol", 10)  # => account with too little
dave = Account("dave", 0)  # => account 2
failed = transfer(carol, dave, 500)  # => co-11: fails after staging the debit -> rollback
print(f"failure: committed={failed.committed}, carol={carol.balance}, dave={dave.balance}")  # => Output: False, 10, 0
print(f"  writes: {failed.writes}")  # => Output: only the staged debit (never applied/committed)

assert ok.committed and alice.balance == 70 and bob.balance == 80  # => co-11: success committed both
assert not failed.committed and carol.balance == 10 and dave.balance == 0  # => co-11: failure rolled both back
