"""Example 60: pytest verification for Mini Logic Engine (Rules + Queries)."""

from example import LogicEngine


def test_transitive_closure_query_resolves() -> None:
    engine = LogicEngine()  # => fresh engine, isolated from the module-level demo
    engine.assert_fact("edge", "x", "y")
    engine.assert_fact("edge", "y", "z")
    closure = sorted(set(engine.query_path("x")))
    assert closure == ["y", "z"]  # => x reaches y directly, and z transitively via y


def test_cyclic_facts_do_not_cause_infinite_recursion() -> None:
    engine = LogicEngine()  # => fresh engine with a self-referencing cycle
    engine.assert_fact("edge", "p", "q")
    engine.assert_fact("edge", "q", "p")  # => p -> q -> p, a two-node cycle
    closure = sorted(set(engine.query_path("p")))  # => must terminate, not hang
    # => the guard stops q->p once "p" is already in `seen` -- proves the cycle was cut, not looped forever
    assert closure == ["q"]


# => Run: pytest -- Output: 2 passed
