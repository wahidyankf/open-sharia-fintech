# learning/code/ex-13-fixture-scope/test_example.py
"""Example 13: Fixture Scope -- Module."""

import pytest  # => same @pytest.fixture decorator, this time with an explicit scope= (co-05)

# => module-level state is the ONLY way to observe how many times a fixture body ran
build_count = 0  # => module-level counter -- proves HOW MANY TIMES the fixture body ran  # fmt: skip


@pytest.fixture(scope="module")  # => scope="module": built ONCE, shared across this whole file  # fmt: skip
def shared_connection() -> dict[str, int]:  # => the fixture body -- WHEN it reruns is the decorator's job  # fmt: skip
    global build_count  # => needed to mutate the module-level counter from inside the fixture
    build_count += (
        1  # => increments EXACTLY once per module, not once per test, if scope works
    )
    return {"connection_id": build_count}  # => the same dict object every test in this file receives  # fmt: skip


def test_first_test_sees_connection_id_one(shared_connection: dict[str, int]) -> None:  # => pytest resolves the param via the fixture above  # fmt: skip
    assert shared_connection["connection_id"] == 1  # => first use -- fixture just built it  # fmt: skip
    assert build_count == 1  # => confirms the fixture body has run exactly once so far


def test_second_test_reuses_the_same_instance(shared_connection: dict[str, int]) -> None:  # => same param name -- pytest injects the ALREADY-BUILT instance  # fmt: skip
    assert shared_connection["connection_id"] == 1  # => SAME id as the first test -- not rebuilt  # fmt: skip
    assert build_count == 1  # => STILL 1 -- proves scope="module" built it only once for the file  # fmt: skip
