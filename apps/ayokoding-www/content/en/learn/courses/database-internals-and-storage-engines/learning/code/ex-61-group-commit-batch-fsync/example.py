"""Example 61: Group Commit Batches N Commits into One fsync."""
# Group commit (co-26) amortizes ONE fsync's cost across many commits, instead of one fsync per commit.


class GroupCommitLog:  # => batches pending commits and counts how many real fsync calls actually happen
    def __init__(self) -> None:  # => starts with nothing pending and nothing durable
        self.pending: list[int] = []  # => transaction ids waiting for the NEXT fsync
        self.durable: set[int] = (
            set()
        )  # => transaction ids confirmed durable by a completed fsync
        self.fsync_count: int = (
            0  # => how many ACTUAL fsync syscalls this log has issued so far
        )

    def commit(
        self, txn_id: int
    ) -> None:  # => a transaction requests to become durable
        self.pending.append(
            txn_id
        )  # => queued, not yet durable -- waits for the group's fsync

    def flush(
        self,
    ) -> None:  # => one fsync call durably commits EVERY pending transaction at once
        self.durable.update(self.pending)  # => all of them become durable together
        self.pending.clear()  # => nothing left waiting
        self.fsync_count += 1  # => exactly ONE fsync served this whole batch


log = GroupCommitLog()  # => a fresh log with nothing committed yet
for txn_id in range(1, 6):  # => five separate transactions all requesting commit
    log.commit(txn_id)  # => each is queued, not yet durable
log.flush()  # => a SINGLE fsync makes all five durable at once
print(log.fsync_count)  # => Output: 1
print(sorted(log.durable))  # => Output: [1, 2, 3, 4, 5]

assert log.fsync_count == 1  # => only one real fsync was needed for all five commits
assert len(log.durable) == 5  # => yet all five transactions are durable
print("ex-61 OK")  # => Output: ex-61 OK
