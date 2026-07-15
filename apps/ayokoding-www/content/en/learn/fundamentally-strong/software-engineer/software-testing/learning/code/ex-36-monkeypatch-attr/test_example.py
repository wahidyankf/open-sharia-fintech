# learning/code/ex-36-monkeypatch-attr/test_example.py
"""Example 36: monkeypatch.setattr."""


# ex-36: pytest's OWN patching fixture -- an alternative to mock.patch, auto-undone after the test (co-14)  # fmt: skip
def get_greeting_prefix() -> str:  # => the real dependency this example swaps out
    return "Hello"  # => the ordinary, unpatched behavior


def greet(name: str) -> str:  # => the unit under test -- depends on get_greeting_prefix via module lookup  # fmt: skip
    return f"{get_greeting_prefix()}, {name}!"  # => looks up get_greeting_prefix in THIS module  # fmt: skip


def test_monkeypatch_setattr_swaps_the_prefix_function(monkeypatch) -> None:
    # monkeypatch is a pytest-BUILTIN fixture, injected by name just like ex-11's custom fixture --
    # its setattr accepts a dotted "module.attr" string plus the replacement value (co-14)
    monkeypatch.setattr(f"{__name__}.get_greeting_prefix", lambda: "Yo")  # => swaps the function  # fmt: skip
    assert (
        greet("Ada") == "Yo, Ada!"
    )  # => act+assert: sees the PATCHED prefix, not "Hello"
    # => monkeypatch automatically UNDOES this swap at the end of the test -- no explicit
    # => "with" block or manual restore needed, unlike ex-35's mock.patch context manager
