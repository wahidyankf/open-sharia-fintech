# learning/code/ex-41-feature-flag-kill-switch/kill_switch.py
"""ex-41: an ops toggle -- disables a misbehaving feature with NO redeploy (co-22)."""  # => co-22: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic


class OpsFlags:  # => co-22: an OPS toggle -- short-lived, operator-flipped, unlike a release flag's longer life
    """A minimal ops-toggle registry: a live process reads it on every call, not just at startup."""  # => co-22: documents OpsFlags's contract -- no runtime output, just sets its __doc__

    def __init__(self) -> None:  # => co-22: every ops toggle starts ON -- the feature is healthy until proven otherwise
        self._enabled: dict[str, bool] = {"gift_card_redemption": True}  # => co-22: the ONE feature this example toggles

    def is_enabled(self, name: str) -> bool:  # => co-22: read on EVERY call -- no process restart needed to see a flip
        """Return whether the named feature is currently enabled."""  # => co-22: documents is_enabled's contract -- no runtime output, just sets its __doc__
        return self._enabled.get(name, True)  # => co-22: unknown names default ON -- this registry only tracks known kill switches

    def disable(self, name: str) -> None:  # => co-22: the OPERATOR action -- no code deploy, no process restart
        """Flip the named feature off -- the kill-switch action itself."""  # => co-22: documents disable's contract -- no runtime output, just sets its __doc__
        self._enabled[name] = False  # => co-22: mutates the LIVE registry -- the next call already sees the new value


def process_request(kind: str, flags: OpsFlags) -> str:  # => co-22: stands in for a live request handler
    """Route one incoming request, honoring the gift-card kill switch if it is flipped."""  # => co-22: documents process_request's contract -- no runtime output, just sets its __doc__
    if kind == "gift_card_redemption" and not flags.is_enabled("gift_card_redemption"):  # => co-22: the GATE itself
        return "503: gift-card redemption temporarily disabled"  # => co-22: the ONE feature stops -- a clean, explicit response
    return f"200: {kind} processed normally"  # => co-22: every OTHER request kind is entirely unaffected


if __name__ == "__main__":  # => co-22: entry point -- this block runs only when the file executes directly, not on import
    flags = OpsFlags()  # => co-22: a fresh registry -- simulates ONE long-running server process, no restart between calls
    request_kinds = ["checkout", "gift_card_redemption", "profile_update"]  # => co-22: three DIFFERENT request kinds

    print("--- before the kill switch is flipped ---")  # => co-22: labels the first batch below
    for kind in request_kinds:  # => co-22: every kind processes normally -- the system is fully healthy
        print(process_request(kind, flags))  # => co-22: prints this request's own response

    flags.disable("gift_card_redemption")  # => co-22: the OPERATOR action -- SAME process, no redeploy, no restart

    print("\n--- after the kill switch is flipped (SAME process, no redeploy) ---")  # => co-22: labels the second batch
    results = [process_request(kind, flags) for kind in request_kinds]  # => co-22: the SAME three kinds, SAME live process
    for kind, result in zip(request_kinds, results):  # => co-22: pairs each kind with its own result for the printout
        print(result)  # => co-22: prints this request's own response

    assert results[1] == "503: gift-card redemption temporarily disabled", "the flagged feature must be OFF"  # => co-22
    assert results[0].startswith("200") and results[2].startswith("200"), "unrelated features must stay UP"  # => co-22
    print("\nOne feature turned off; the rest of the system stayed up, no redeploy: True")  # => co-22: reached only if both asserts passed
