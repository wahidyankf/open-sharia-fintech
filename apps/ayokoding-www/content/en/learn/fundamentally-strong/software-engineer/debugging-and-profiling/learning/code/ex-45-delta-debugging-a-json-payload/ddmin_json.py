"""Example 45: delta-debug a 500-key crashing JSON payload down to a tiny reproducer.

A request handler crashes on some payloads because one particular key/value pair
triggers a bug, buried among 500 unrelated keys a fuzzer generated. Rather than
stare at all 500, we shrink by deleting one top-level key at a time and
re-testing -- classic ddmin, applied to structured (dict) data instead of a flat
string. co-11: the search is the same shape as ex-24's halving, just keyed on
dict keys instead of string offsets.
"""

from __future__ import annotations

import json
from typing import Any


def handle_payload(payload: dict[str, Any]) -> int:
    # co-14/co-15: the real bug -- "retries" as a *string* "0" is falsy-but-truthy
    # in a way that trips an int() conversion deeper in a real handler; here we
    # simulate that exact crash directly so the repro is self-contained.
    if "retries" in payload and payload["retries"] == "0":
        raise ValueError("retries must be an int, got the string '0'")
    return len(payload)


def still_fails(payload: dict[str, Any]) -> bool:
    try:
        handle_payload(payload)
    except ValueError:
        return True  # =>  same crash still reproduces on this shrunk payload
    return False  # =>  crash gone -- this shrink step went too far


def ddmin_dict(payload: dict[str, Any]) -> dict[str, Any]:
    current = dict(payload)
    changed = True
    while changed and len(current) > 1:
        changed = False
        for key in list(current.keys()):
            candidate = {k: v for k, v in current.items() if k != key}
            if still_fails(candidate):
                current = candidate  # =>  dropping this key kept the bug -- keep the smaller dict
                changed = True
                break  # =>  restart the scan over the new, smaller dict
    return current


def make_fuzzed_payload(n_noise_keys: int) -> dict[str, Any]:
    # co-11: 500 unrelated noise keys plus the one real trigger key, "retries".
    payload: dict[str, Any] = {
        f"noise_{i:04d}": i * 7 % 997 for i in range(n_noise_keys)
    }
    payload["retries"] = "0"  # =>  the one key that actually matters
    return payload


def main() -> None:
    original = make_fuzzed_payload(
        n_noise_keys=499
    )  # =>  499 noise + 1 real = 500 keys total
    assert len(original) == 500, "sanity check: fixture must have exactly 500 keys"
    assert still_fails(original), "sanity check: original payload must fail first"

    minimal = ddmin_dict(original)
    print(f"original key count: {len(original)}")
    print(f"minimal key count:  {len(minimal)}")
    print(f"minimal payload: {json.dumps(minimal, sort_keys=True)}")

    assert still_fails(minimal), "sanity check: minimized payload must still fail"
    assert len(minimal) < 5, f"expected under 5 keys, got {len(minimal)}"
    assert minimal == {"retries": "0"}, (
        "expected the minimal repro to be exactly {'retries': '0'}"
    )
    print(
        f"confirmed: minimal payload ({len(minimal)} key) still reproduces the crash, well under the 5-key bound"
    )


if __name__ == "__main__":
    main()
