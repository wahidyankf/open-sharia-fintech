"""Example 4: Extend Behavior via a Plugin Registry."""

from typing import Callable  # => Callable types the registry's stored handlers

HANDLERS: dict[str, Callable[[str], str]] = {}  # => starts empty; register() populates it as each handler module-level-loads  # => the ONE registry every handler plugs into


def register(
    name: str,
    # => name is the event key later dispatch() calls will look up
) -> Callable[
    [Callable[[str], str]], Callable[[str], str]  # => maps handler-in to handler-out
]:  # => a decorator FACTORY, returns the real decorator below
    def decorator(
        fn: Callable[[str], str],
        # => fn is the handler function being registered under `name`
    ) -> Callable[[str], str]:  # => the actual decorator, closes over `name`
        HANDLERS[name] = fn  # => the ONLY line that mutates HANDLERS
        return fn  # => returns fn unchanged so it stays directly callable too

    return decorator  # => returns this closure to be applied as @register("...")


@register("greet")  # => registers this function under the key "greet"
def handle_greet(payload: str) -> str:  # => defines the handle_greet() function
    return f"Hello, {payload}!"  # => the greet-specific behavior, isolated here
    # => this decorator call is the ONLY place "greet" is ever written down


@register("shout")  # => a SECOND handler, registered with zero edits to dispatch()
def handle_shout(payload: str) -> str:  # => defines the handle_shout() function
    return payload.upper() + "!!!"  # => the shout-specific behavior, isolated here


def dispatch(event_name: str, payload: str) -> str:  # => defines the dispatch() function
    handler: Callable[[str], str] = HANDLERS[
        event_name  # => the key chosen by whichever @register("...") call ran earlier
    ]  # => looks up the registered handler by name -- no if/elif anywhere
    return handler(payload)  # => calls whichever function was registered
    # => this function never mentions "greet" or "shout" by name, ever


print(dispatch("greet", "Rex"))  # => routes through the registry, not a branch
print(dispatch("shout", "woof"))  # => a totally different registered handler
# => a fifth handler could be added below with @register("...") and no other edit
# => Output: Hello, Rex!
# => WOOF!!!
# => `dispatch()` was written once and never touched again when `handle_shout` was added
