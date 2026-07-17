"""Example 62: pytest verification for Reactive Graph Diamond."""

from example import Computed, Signal


def _build_diamond() -> tuple[Signal, Computed, Computed, Computed]:  # => same wiring as the module demo
    a = Signal(0)
    b = Computed(lambda: a.get() + 1, depth=1)
    c = Computed(lambda: a.get() + 2, depth=1)
    d = Computed(lambda: b.value + c.value, depth=2)
    a.dependents.extend([b, c])
    b.dependents.append(d)
    c.dependents.append(d)
    return a, b, c, d


def test_d_recomputes_exactly_once_per_a_update() -> None:
    a, _b, _c, d = _build_diamond()  # => fresh diamond, isolated from the module-level demo
    a.write(5)  # => one write at the top
    assert d.recompute_count == 1  # => the crux of this example: NOT 2, despite d having two incoming edges


def test_d_value_reflects_both_branches_after_update() -> None:
    a, _b, _c, d = _build_diamond()  # => fresh diamond
    a.write(5)  # => b becomes 6, c becomes 7
    assert d.value == 13  # => 6 + 7


# => Run: pytest -- Output: 2 passed
