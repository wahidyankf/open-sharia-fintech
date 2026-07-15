# learning/code/ex-37-monkeypatch-env/test_example.py
"""Example 37: monkeypatch.setenv."""

import os  # => needed so get_environment_name can read a real environment variable


def get_environment_name() -> str:  # => the unit under test -- reads an ENV VAR, a form of hidden state (co-26)  # fmt: skip
    return os.environ.get("APP_ENV", "development")  # => "development" is the default if unset  # fmt: skip


def test_monkeypatch_setenv_controls_the_environment(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")  # => co-14: sets a REAL env var for this test's duration  # fmt: skip
    # => this genuinely mutates os.environ["APP_ENV"] -- get_environment_name has no idea
    # => it is being tested; it reads the SAME os.environ any real process would read
    assert get_environment_name() == "production"  # => act+assert: sees the PATCHED env var  # fmt: skip


def test_the_environment_variable_does_not_leak_between_tests() -> None:
    # => monkeypatch automatically UNSETS APP_ENV at the end of the PREVIOUS test --
    # => proving that env-var patching, like attribute patching (ex-36), is test-scoped
    assert get_environment_name() == "development"  # => back to the default -- no leftover "production"  # fmt: skip
