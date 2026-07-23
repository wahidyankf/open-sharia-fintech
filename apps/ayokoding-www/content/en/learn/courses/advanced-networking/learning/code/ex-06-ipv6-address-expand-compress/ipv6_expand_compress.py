# learning/code/ex-06-ipv6-address-expand-compress/ipv6_expand_compress.py
"""Example 6: IPv6 Address Expand/Compress -- 2001:db8::1 Round-Trips."""  # => co-03: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import ipaddress  # => co-03: stdlib's own IPv6 parser -- used here ONLY to cross-check the hand-rolled expand/compress


def expand(address: str) -> str:  # => co-03: "2001:db8::1" -> its 8 full, zero-padded hextets -- BY HAND, no ipaddress calls
    """Expand a compressed IPv6 address to its 8 full 4-digit hextets, colon-separated."""  # => co-03: documents expand's contract -- no runtime output, just sets its __doc__
    if "::" in address:  # => co-03: "::" is IPv6's ONE-PER-ADDRESS run-of-zeros compression marker
        left, right = address.split("::", 1)  # => co-03: everything before/after the single "::" (either side may be empty)
        left_parts = left.split(":") if left else []  # => co-03: "" .split(":") would wrongly yield [""], so guard the empty case
        right_parts = right.split(":") if right else []  # => co-03: same empty-string guard for the trailing side
        missing = 8 - len(left_parts) - len(right_parts)  # => co-03: "::" stands in for exactly this many all-zero hextets
        hextets = left_parts + (["0"] * missing) + right_parts  # => co-03: splice the implied zero hextets into the gap
    else:  # => co-03: no "::" present -- already 8 explicit hextets, nothing to expand
        hextets = address.split(":")  # => co-03: split on the ordinary hextet separator
    return ":".join(part.zfill(4) for part in hextets)  # => co-03: zero-PAD each hextet to 4 hex digits (zfill, not truncate)


def compress(expanded: str) -> str:  # => co-03: the EXACT inverse -- 8 full hextets -> the shortest legal "::" form
    """Compress a fully-expanded IPv6 address by collapsing its LONGEST run of all-zero hextets."""  # => co-03: documents compress's contract -- no runtime output, just sets its __doc__
    hextets = expanded.split(":")  # => co-03: 8 zero-padded hextets, one element per group
    trimmed = [part.lstrip("0") or "0" for part in hextets]  # => co-03: drop leading zeros per hextet ("0001" -> "1"), keep a lone "0"
    best_start, best_len, run_start, run_len = -1, 0, -1, 0  # => co-03: tracks the LONGEST zero-run seen so far (RFC 5952 §4.2.2 rule)
    for i, part in enumerate(trimmed):  # => co-03: scan every hextet position looking for runs of exactly "0"
        if part == "0":  # => co-03: this hextet is zero -- either continue or start a new run
            run_start = i if run_len == 0 else run_start  # => co-03: mark this position as the run's start if one just began
            run_len += 1  # => co-03: extend the current run by one hextet
            if run_len > best_len:  # => co-03: a strictly LONGER run replaces the previous best (ties keep the FIRST, per RFC 5952)
                best_start, best_len = run_start, run_len  # => co-03: records this run as the new best-so-far
        else:  # => co-03: a nonzero hextet -- any in-progress run ends here
            run_len = 0  # => co-03: reset -- the next zero hextet (if any) starts a brand-new run
    if best_len < 2:  # => co-03: RFC 5952 only compresses a run of 2+ zero hextets -- a single "0" is never worth a "::"
        return ":".join(trimmed)  # => co-03: no compression applies -- print the trimmed hextets as-is
    before = trimmed[:best_start]  # => co-03: every hextet strictly before the compressed run
    after = trimmed[best_start + best_len :]  # => co-03: every hextet strictly after the compressed run
    return ":".join(before) + "::" + ":".join(after)  # => co-03: splice "::" exactly where the longest zero-run was


if __name__ == "__main__":  # => co-03: entry point -- this block runs only when the file executes directly, not on import
    compressed = "2001:db8::1"  # => co-03: the syllabus's fixed test address
    full = expand(compressed)  # => co-03: hand-rolled expansion to 8 full hextets
    print(f"{compressed} expanded = {full}")  # => co-03: expect all 8 groups, zero-padded to 4 hex digits each
    assert full == "2001:0db8:0000:0000:0000:0000:0000:0001", "must expand to exactly 8 zero-padded hextets"  # => co-03
    recompressed = compress(full)  # => co-03: hand-rolled recompression -- must find the SAME "::" position
    print(f"{full} recompressed = {recompressed}")  # => co-03: expect the round trip back to the original compressed form
    assert recompressed == compressed, "recompression must recover the original compressed form"  # => co-03: the round-trip claim
    stdlib_check = ipaddress.IPv6Address(compressed)  # => co-03: an INDEPENDENT parser, never touched by expand()/compress() above
    assert str(stdlib_check.exploded) == full, "hand-rolled expand must match ipaddress.exploded"  # => co-03: cross-checks expand()
    assert str(stdlib_check.compressed) == recompressed, "hand-rolled compress must match ipaddress.compressed"  # => co-03
    print("Both forms round-trip and match ipaddress's own parser: True")  # => co-03: reached only if every assert above passed
    # => co-03: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
