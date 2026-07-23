"""Example 46: the real Zeller ddmin algorithm (n-way splitting, not plain halving).

ex-24 used one-shot halving, which only works when the failing fragment is cleanly
isolated by a single split. Real inputs are rarely that convenient: this example
seeds TWO separate trigger characters ('#' and '@') far apart in a 300-char string,
so a parser only crashes when *both* are present. Plain halving would delete one of
them on the first split and falsely conclude the crash is gone. The full ddmin
algorithm -- start at granularity 2, remove one of n chunks, and only grow n back to
len(current) when a whole pass finds no reducible chunk -- correctly narrows in on
the 2-character minimal reproducer.
"""

from __future__ import annotations


def parse(s: str) -> None:
    # co-14: crash requires BOTH markers present -- a stand-in for two interacting
    # tokens (e.g. an unescaped quote *and* a trailing comma) that only crash a
    # parser together, never alone.
    if "#" in s and "@" in s:
        raise ValueError("parser choked on both '#' and '@' present")


def still_fails(s: str) -> bool:
    try:
        parse(s)
    except ValueError:
        return True
    return False


def ddmin(s: str) -> str:
    n = 2  # =>  granularity: split `s` into `n` roughly-equal chunks
    current = s
    while len(current) >= 2:
        chunk_size = max(1, len(current) // n)
        chunks = [
            current[i : i + chunk_size] for i in range(0, len(current), chunk_size)
        ]
        reduced = False
        for i in range(len(chunks)):
            candidate = "".join(c for j, c in enumerate(chunks) if j != i)
            if candidate and still_fails(candidate):
                current = candidate  # =>  removing chunk i kept the crash -- accept the smaller string
                n = max(n - 1, 2)  # =>  reset granularity, we made progress
                reduced = True
                break
        if not reduced:
            if n >= len(current):
                break  # =>  granularity can't go finer than one char per chunk -- done
            n = min(
                n * 2, len(current)
            )  # =>  no chunk was removable -- split finer and retry
    return current


def main() -> None:
    prefix = "x" * 140
    middle = "y" * 20
    suffix = "z" * 140
    original = prefix + "#" + middle + "@" + suffix  # =>  302 chars, markers 21 apart
    assert still_fails(original)
    minimal = ddmin(original)
    print(f"original length: {len(original)}")
    print(f"minimal length:  {len(minimal)}")
    print(f"minimal string:  {minimal!r}")
    assert still_fails(minimal)
    assert sorted(minimal) == sorted("#@"), (
        "expected the minimal repro to be exactly the two markers"
    )
    print(
        "confirmed: ddmin correctly kept BOTH markers despite plain halving being "
        "unable to isolate both markers simultaneously"
    )

    # co-11: 1-minimal means NO single remaining char can be deleted without the
    # bug disappearing -- verify that directly, character by character.
    for i in range(len(minimal)):
        one_shorter = minimal[:i] + minimal[i + 1 :]
        assert not still_fails(one_shorter), (
            f"expected removing char {i!r} ({minimal[i]!r}) to CLEAR the bug, but it still failed"
        )
        print(
            f"  removing {minimal[i]!r} at index {i} -> {one_shorter!r} -- bug cleared, as expected"
        )
    print(
        "confirmed: the 2-char result is 1-minimal (every further single-char removal clears the bug)"
    )


if __name__ == "__main__":
    main()
