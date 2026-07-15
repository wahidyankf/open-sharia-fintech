# learning/code/ex-22-shared-conftest-fixture/test_example.py
"""Example 22: A Shared Fixture in conftest.py."""


# ex-22a: this file uses shared_greeting WITHOUT ever importing it (co-09, co-05)
def test_first_file_sees_the_shared_fixture(shared_greeting: str) -> None:
    # => "shared_greeting" resolves purely by matching this PARAMETER NAME against
    # => conftest.py's fixture of the same name -- pytest wires this up automatically
    assert shared_greeting == "hello from conftest"  # => confirms the injected value is real  # fmt: skip
