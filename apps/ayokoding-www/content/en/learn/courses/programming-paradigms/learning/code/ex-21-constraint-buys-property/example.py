"""Example 21: Constraint Buys Property."""


def uses_a_tuple(shared: tuple[int, ...]) -> tuple[int, ...]:  # => receives an IMMUTABLE sequence
    # shared.append(99)  # => would be a AttributeError: tuple has no append -- the constraint is enforced
    return shared + (99,)  # => "adding" returns a BRAND NEW tuple -- never touches the original
    # => this is the constraint: no in-place mutation exists on tuple at all


def uses_a_frozenset(shared: frozenset[int]) -> frozenset[int]:  # => receives an IMMUTABLE set
    # shared.add(99)  # => would be an AttributeError: frozenset has no add -- same constraint
    return shared | {99}  # => "adding" returns a BRAND NEW frozenset via union, original untouched
    # => the constraint (no mutation method exists) is what BUYS the property (safe to share freely)


shared_tuple: tuple[int, ...] = (1, 2, 3)  # => one immutable object
shared_frozenset: frozenset[int] = frozenset({1, 2, 3})  # => a second immutable object

result_a = uses_a_tuple(shared_tuple)  # => function A receives the SAME shared object
result_b = uses_a_tuple(shared_tuple)  # => function B (same fn, different call) also receives it
print(shared_tuple)  # => neither call could have mutated it -- no method exists to do so
# => Output: (1, 2, 3)
print(result_a == result_b)  # => both calls independently derived the identical new tuple
# => Output: True

frozen_result = uses_a_frozenset(shared_frozenset)  # => same story for frozenset
print(shared_frozenset, sorted(frozen_result))  # => the original is provably unchanged
# => Output: frozenset({1, 2, 3}) [1, 2, 3, 99]
