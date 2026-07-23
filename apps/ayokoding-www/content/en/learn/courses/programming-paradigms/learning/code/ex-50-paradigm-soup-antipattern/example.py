"""Example 50: Paradigm Soup Anti-Pattern."""


class MutableBucket:  # => an OO object with mutable state, threaded through a nominally "functional" pipeline
    def __init__(self, items: list[int]) -> None:
        self.items = items  # => a MUTABLE list, not a tuple -- this is the seed of the bug


def add_bonus_functional_looking(bucket: MutableBucket) -> MutableBucket:  # => LOOKS like a pure map step...
    bucket.items.append(999)  # => ...but secretly MUTATES the shared list in place -- paradigm soup
    return bucket  # => returning the SAME mutated object, not a new one, is the tell


def scale_functional_looking(bucket: MutableBucket) -> MutableBucket:  # => a second "map step"
    for i in range(len(bucket.items)):  # => also mutates in place, hidden behind a function-call facade
        bucket.items[i] *= 2  # => in-place scaling
    return bucket  # => same object identity as the input -- no new value was actually created


original = MutableBucket([1, 2, 3])  # => construct the shared mutable object once
step1 = add_bonus_functional_looking(original)  # => "looks like" pipe(original, add_bonus)
step2 = scale_functional_looking(step1)  # => "looks like" pipe(step1, scale) -- chained, functional style

print(step2.items)  # => the visible chained result
# => Output: [2, 4, 6, 1998]
print(original.items)  # => THE BUG: `original` was aliased and mutated by every "pipeline" step
# => Output: [2, 4, 6, 1998]
print(original is step1 is step2)  # => all three names point at the SAME object -- no new values anywhere
# => Output: True
