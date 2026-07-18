# learning/code/ex-40-feature-flag-release-toggle/feature_flags.py
"""ex-40: a release toggle -- ships incomplete code to trunk, DISABLED (co-22, co-01)."""  # => co-22: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic


class ReleaseFlags:  # => co-22: a tiny, in-memory release-toggle registry -- stands in for a real flag service
    """A minimal release-toggle registry: incomplete features stay OFF until explicitly flipped."""  # => co-22: documents ReleaseFlags's contract -- no runtime output, just sets its __doc__

    def __init__(self) -> None:  # => co-22: every flag starts OFF -- the safe, trunk-based default
        self._flags: dict[str, bool] = {  # => co-22: co-01: this is what LETS trunk-based dev work --
            "multi_currency_redemption": False,  # =>    incomplete code merges to trunk disabled,
        }  # =>    instead of living on a long-lived branch until "ready"

    def is_enabled(self, name: str) -> bool:  # => co-22: the ONE call site every caller uses to check a flag
        """Return whether the named release flag is currently enabled."""  # => co-22: documents is_enabled's contract -- no runtime output, just sets its __doc__
        return self._flags.get(name, False)  # => co-22: an UNKNOWN flag name defaults to False -- fail closed, not open

    def enable(self, name: str) -> None:  # => co-22: flips a flag ON -- the "release" half of deploy/release decoupling
        """Enable the named release flag."""  # => co-22: documents enable's contract -- no runtime output, just sets its __doc__
        self._flags[name] = True  # => co-22: mutates the registry in place


def redeem(amount: float, currency: str, flags: ReleaseFlags) -> str:  # => co-22: the caller this whole flag protects
    """Redeem `amount` in `currency`, gated by the multi_currency_redemption release flag."""  # => co-22: documents redeem's contract -- no runtime output, just sets its __doc__
    if currency != "USD" and not flags.is_enabled("multi_currency_redemption"):  # => co-22: the GATE itself
        raise NotImplementedError("multi-currency redemption is not yet enabled")  # => co-22: flag OFF -- old behavior preserved exactly
    return f"redeemed {amount} {currency}"  # => co-22: flag ON (or currency==USD) -- the new/existing path runs


if __name__ == "__main__":  # => co-22: entry point -- this block runs only when the file executes directly, not on import
    flags = ReleaseFlags()  # => co-22: a fresh registry, flag OFF by default (the just-merged-to-trunk state)

    usd_result = redeem(10.0, "USD", flags)  # => co-22: USD always works -- the flag only gates NEW currencies
    print(f"USD redemption with flag OFF: {usd_result}")  # => co-22: prints the unaffected, pre-existing path

    try:  # => co-22: the incomplete feature, merged to trunk, still DISABLED
        redeem(10.0, "EUR", flags)  # => co-22: this is the trunk-build-stays-green claim under test
    except NotImplementedError as exc:  # => co-22: expected -- the gate is doing its job
        print(f"EUR redemption with flag OFF: blocked ({exc})")  # => co-22: prints the blocked-path confirmation
    assert not flags.is_enabled("multi_currency_redemption"), "flag must still be OFF here"  # => co-22: the trunk-stays-green check

    flags.enable("multi_currency_redemption")  # => co-22: the RELEASE step -- deploy already happened; this is separate
    eur_result = redeem(10.0, "EUR", flags)  # => co-22: same code, same deploy, now unlocked
    print(f"EUR redemption with flag ON: {eur_result}")  # => co-22: prints the newly-unlocked path
    assert eur_result == "redeemed 10.0 EUR", "flag ON must unlock the new currency path"  # => co-22: the release-works check
    print("Trunk build stayed green with the flag off, and flag-on unlocks the new path: True")  # => co-22: reached only if both asserts passed
