"""Example 53: reject work when a bounded queue has no admission slot."""

# => The fixture queue has one occupied slot and therefore no capacity for another request.
capacity, queued = 1, ["first-job"]
# => Admission is a policy result rather than an unbounded append.
admitted = len(queued) < capacity
# => The assertion proves overload is reported before it consumes more memory.
assert admitted is False
# => Output makes the queue decision visible to callers.
print("queue full: request not admitted")
