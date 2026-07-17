"""Example 4: pytest verification for Extend Behavior via a Plugin Registry."""

from example import HANDLERS, dispatch, register


def test_new_handler_needs_zero_edits_to_dispatch() -> None:
    # => registers a THIRD handler here, in the test, after the module already loaded
    @register("whisper")
    def handle_whisper(payload: str) -> str:  # => a brand-new handler, defined locally
        return payload.lower() + "..."  # => the whisper-specific behavior

    assert "whisper" in HANDLERS  # => the decorator alone added it to the registry
    assert dispatch("whisper", "REX") == "rex..."  # => dispatch() needed no changes


def test_existing_handlers_still_work() -> None:
    assert dispatch("greet", "Rex") == "Hello, Rex!"
    assert dispatch("shout", "woof") == "WOOF!!!"


# => Run: pytest -- Output: 2 passed
