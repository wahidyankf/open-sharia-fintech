"""Example 58: Refactor Inheritance to Composition.

co-33 (refactor to pattern): a 4-level inheritance hierarchy, each level bolting on
one orthogonal capability (logging, retry, throttling), is refactored to a single
depth-1 class composed with small behavior objects -- co-09 (grasp-low-coupling):
the composed version needs zero new subclasses to add a capability, only a new
wrapper object. test_example.py locks both versions' observable behavior so the
refactor is verifiably safe.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# ============================================================
# BEFORE: a 4-level inheritance hierarchy, one capability per level
# ============================================================


class Notifier:  # => level 1 (base): just sends -- no capabilities yet
    def send(self, message: str) -> str:  # => returns what was "sent", stubbed as a string for this example
        return f"SEND:{message}"  # => the delivery itself


class LoggingNotifier(Notifier):  # => level 2: bolts on logging via override
    def __init__(self) -> None:  # => LoggingNotifier's constructor takes no new parameters beyond self
        self.log: list[str] = []  # => records every message this notifier has sent

    def send(self, message: str) -> str:  # => override adds ONE capability: logging
        self.log.append(message)  # => side effect before delegating up
        return super().send(message)  # => delegates to level 1's real send


# => level 3 repeats level 2's override-and-delegate shape one layer deeper, adding retry state
class RetryingLoggingNotifier(LoggingNotifier):  # => level 3: bolts on retry, on top of logging
    def __init__(self, attempts: int) -> None:  # => adds one new constructor parameter for this level's capability
        super().__init__()  # => must still wire up level 2's state
        self.attempts = attempts  # => how many times to retry

    def send(self, message: str) -> str:  # => override adds a SECOND capability: retry
        last_result = ""  # => tracks the most recent attempt's result
        for _ in range(self.attempts):  # => retry loop wraps the logging+base chain
            last_result = super().send(message)  # => delegates up two levels each iteration
        return last_result  # => the final attempt's result


# => level 4 keeps stacking: every new capability means one more override plus one more __init__ chain link
class ThrottledRetryingLoggingNotifier(RetryingLoggingNotifier):  # => level 4: bolts on throttling
    def __init__(self, attempts: int, max_calls: int) -> None:  # => now carries state for capabilities from two different levels
        super().__init__(attempts)  # => must wire up levels 3 AND 2's __init__ chain
        self.max_calls = max_calls  # => a THIRD, independent capability: a call budget
        self.calls_made = 0  # => how many sends have happened so far

    def send(self, message: str) -> str:  # => override adds a THIRD capability: throttling
        if self.calls_made >= self.max_calls:  # => guard: budget exhausted
            return "THROTTLED"  # => refuse to send once the budget is spent
        self.calls_made += 1  # => consume one unit of budget
        return super().send(message)  # => delegates up the whole three-level chain
        # => one send() call now cascades through 4 stacked overrides: throttle -> retry -> logging -> base


# ============================================================
# AFTER: one depth-1 class, capabilities composed as small standalone objects
# ============================================================


@dataclass  # => auto-generates __init__ from the single field below
class LoggingBehavior:  # => composed equivalent of LoggingNotifier -- one small standalone class
    log: list[str] = field(default_factory=list)  # => same responsibility, now owned independently


# => this single class replaces all 4 inheritance levels above, using composed collaborators instead of subclassing
class ComposedNotifier:  # => depth 1: no subclass at all -- capabilities are composed, not inherited
    def __init__(self, logging: LoggingBehavior | None = None) -> None:  # => takes an OPTIONAL composed capability instead of a hardcoded subclass chain
        self.logging = logging  # => an OPTIONAL logging capability, composed in per instance

    def raw_send(self, message: str) -> str:  # => the equivalent of Notifier.send() in the old hierarchy
        if self.logging is not None:  # => only log if a LoggingBehavior was composed in
            self.logging.log.append(message)  # => same log side effect, now opt-in rather than baked into a subclass
        return f"SEND:{message}"  # => identical delivery stub to the inheritance version


@dataclass  # => auto-generates __init__ for the retry capability's single field
class RetryBehavior:  # => composed equivalent of the retry capability -- reusable on its own
    attempts: int  # => how many times to retry


@dataclass  # => auto-generates __init__ for the throttle capability's two fields
class ThrottleBehavior:  # => composed equivalent of the throttle capability -- reusable on its own
    max_calls: int  # => the call budget
    calls_made: int = 0  # => mutable counter, local to this one small class


# => a free function stands in for a 4th subclass level, since retry/throttle here are simple per-call parameters
def send_with_capabilities(  # => a free function stands in for what would have been a 4th subclass level
    notifier: ComposedNotifier,  # => the base object, already composed with logging
    message: str,  # => the message to send
    retry: RetryBehavior,  # => the retry capability, composed in as a parameter
    throttle: ThrottleBehavior,  # => the throttle capability, composed in as a parameter
) -> str:  # => closes the multi-line signature; the function still returns a plain string like the old send()
    if throttle.calls_made >= throttle.max_calls:  # => throttle checked first, matching the old outermost override
        return "THROTTLED"  # => matches ThrottledRetryingLoggingNotifier's early return
    throttle.calls_made += 1  # => consumes budget exactly once per call, matching the old behavior
    last_result = ""  # => tracks the final attempt across retries
    for _ in range(retry.attempts):  # => same retry loop as before, now composed rather than inherited
        last_result = notifier.raw_send(message)  # => delegates to the composed base (which itself logs)
    return last_result  # => the final attempt's result


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    old_notifier = ThrottledRetryingLoggingNotifier(attempts=2, max_calls=5)  # => 4-level inheritance version
    print(old_notifier.send("hello"))  # => exercises the full inherited chain
    # => Output: SEND:hello
    logging_behavior = LoggingBehavior()  # => the composed logging unit
    new_notifier = ComposedNotifier(logging=logging_behavior)  # => depth-1 composed version
    result = send_with_capabilities(new_notifier, "hello", RetryBehavior(attempts=2), ThrottleBehavior(max_calls=5))  # => exercises the composed equivalent
    print(result)  # => identical output to the inheritance version
    # => Output: SEND:hello
    print(len(ThrottledRetryingLoggingNotifier.__mro__))  # => old hierarchy: 4 custom classes + object
    # => Output: 5
    print(ComposedNotifier.__mro__ == (ComposedNotifier, object))  # => new version: depth 1, no intermediate bases
    # => Output: True
