class Worker:  # => co-05: models one server PROCESS -- its own local memory, no memory shared with peers
    def __init__(self, name: str) -> None:
        self.name = name
        self._local_cache: dict[str, int] = {}  # => in-process state -- this is what statelessness FORBIDS relying on

    def handle_request(self, shared_db: dict[str, int], key: str, increment: int) -> int:
        # => co-05: the ONLY state this handler is allowed to depend on is the SHARED store, not local memory
        self._local_cache[key] = self._local_cache.get(key, 0) + 1  # => a LOCAL counter -- diverges per worker
        shared_db[key] = shared_db.get(key, 0) + increment  # => co-05: durable state lives in ONE shared place
        return shared_db[key]  # => every worker reads/writes the SAME shared value, regardless of which handled it

    def local_count(self, key: str) -> int:  # => a PUBLIC accessor -- for this kata's inspection only
        return self._local_cache.get(key, 0)


shared_db: dict[str, int] = {}  # => co-05: stands in for "the database" -- the one place real state lives
worker_a = Worker("worker-a")  # => co-05: two independent workers, as if behind a load balancer
worker_b = Worker("worker-b")

result1 = worker_a.handle_request(shared_db, "views", 1)  # => request 1 happens to land on worker A
result2 = worker_b.handle_request(shared_db, "views", 1)  # => request 2 happens to land on worker B
result3 = worker_a.handle_request(shared_db, "views", 1)  # => request 3 lands back on worker A

print(result1, result2, result3)  # => Output: 1 2 3
print(worker_a.local_count("views"), worker_b.local_count("views"))  # => Output: 2 1

# => co-05: each worker's LOCAL count only reflects requests IT happened to handle -- they diverge
assert worker_a.local_count("views") == 2 and worker_b.local_count("views") == 1
# => but the SHARED db is consistent regardless of which worker handled which request -- that's the point
assert shared_db["views"] == 3 == result3
print("kata-12 OK")
