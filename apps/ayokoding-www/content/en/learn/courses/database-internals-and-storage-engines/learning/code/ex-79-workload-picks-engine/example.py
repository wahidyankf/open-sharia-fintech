"""Example 79: A Workload Chooser Selects LSM Then B-Tree."""
# The engine choice (co-14) is a function of the workload's write fraction -- no universal winner.


def choose_engine(
    write_fraction: float,
) -> str:  # => a simplified, threshold-based recommendation
    if (
        write_fraction >= 0.5
    ):  # => write-heavy or write-balanced -- LSM's buffered writes win here
        return "LSM"  # => write-optimized: buffer in memory, flush sequentially
    return "B-tree"  # => read-heavy -- the B-tree's bounded-height point reads win here


write_heavy_workload = 0.9  # => 90% writes, 10% reads -- an ingest-style pipeline
read_heavy_workload = 0.1  # => 10% writes, 90% reads -- a lookup-style service

write_heavy_choice = choose_engine(
    write_heavy_workload
)  # => run the chooser on the write-heavy case
read_heavy_choice = choose_engine(read_heavy_workload)  # => and on the read-heavy case
print(write_heavy_choice)  # => Output: LSM
print(read_heavy_choice)  # => Output: B-tree

assert write_heavy_choice == "LSM"  # => the write-heavy workload correctly selects LSM
assert (
    read_heavy_choice == "B-tree"
)  # => the read-heavy workload correctly selects B-tree
print("ex-79 OK")  # => Output: ex-79 OK
