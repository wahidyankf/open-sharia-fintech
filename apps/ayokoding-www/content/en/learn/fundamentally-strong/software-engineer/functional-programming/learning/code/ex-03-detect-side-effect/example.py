"""Example 3: Classify Pure vs. Impure Functions."""

log: list[str] = []  # => module-level list -- a target for one function's side effect


def loud_double(x: int) -> int:  # => impure: prints, an observable side effect
    print(
        f"doubling {x}"
    )  # => I/O is a side effect -- output visible OUTSIDE the return value
    return (
        x * 2
    )  # => the return value itself is fine; the PRINT above is the side effect


def mutate_double(items: list[int]) -> None:  # => impure: mutates the CALLER's own list
    items.append(
        items[-1] * 2
    )  # => appends in place -- the caller's list object changes
    # => returns None on purpose: the "result" is the mutation itself, not a return value


def pure_double(x: int) -> int:  # => pure: only reads x, only returns a new value
    return x * 2  # => no print, no mutation of any argument, no global touched


def is_pure(
    fn_name: str,
) -> bool:  # => a tiny classifier keyed by name for this example
    return fn_name == "pure_double"  # => only pure_double is flagged pure by this check


nums = [1, 2]  # => a list the impure mutate_double will mutate below
mutate_double(nums)  # => side effect: nums is mutated to [1, 2, 4]
classifications = {  # => a dict recording each function's purity classification
    "loud_double": is_pure("loud_double"),  # => False -- prints, so it is impure
    "mutate_double": is_pure("mutate_double"),  # => False -- mutates its argument
    "pure_double": is_pure("pure_double"),  # => True -- the only one flagged pure
}  # => three functions, three independent purity verdicts
print(classifications["pure_double"])  # => Output: True
print(  # => reads both remaining classifications out of the same dict
    classifications["loud_double"], classifications["mutate_double"]
)
# => Output: False False
