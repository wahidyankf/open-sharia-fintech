# learning/code/ex-07-cidr-prefix-to-netmask/cidr_to_netmask.py
"""Example 7: CIDR Prefix to Netmask -- /24, /26, /30 by Hand."""  # => co-04: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import ipaddress  # => co-04: stdlib's own CIDR parser -- used here ONLY to cross-check the hand-rolled prefix->mask table


def prefix_to_netmask(prefix_len: int) -> str:  # => co-04: /N -> its dotted-decimal netmask, BY HAND -- no ipaddress calls
    """Convert a CIDR prefix length (0-32) to its dotted-decimal netmask."""  # => co-04: documents prefix_to_netmask's contract -- no runtime output, just sets its __doc__
    if not 0 <= prefix_len <= 32:  # => co-04: an IPv4 prefix length is always between /0 (nothing) and /32 (one host)
        raise ValueError(f"/{prefix_len} is not a valid IPv4 prefix length (0-32)")  # => co-04: guards the prefix-length invariant
    mask_bits = ("1" * prefix_len).ljust(32, "0")  # => co-04: N leading 1-bits (the NETWORK portion), padded with 0-bits (HOST portion)
    octets = [mask_bits[i : i + 8] for i in range(0, 32, 8)]  # => co-04: slice the 32-bit string into 4 groups of 8 bits each
    return ".".join(str(int(octet, 2)) for octet in octets)  # => co-04: each 8-bit group parsed back to its decimal octet value


if __name__ == "__main__":  # => co-04: entry point -- this block runs only when the file executes directly, not on import
    reference_table = {24: "255.255.255.0", 26: "255.255.255.192", 30: "255.255.255.252"}  # => co-04: the syllabus's fixed prefix->mask reference table
    print("prefix -> netmask (hand-computed vs. reference table):")  # => co-04: labels the following per-prefix comparison
    for prefix_len, expected in reference_table.items():  # => co-04: one row per prefix this example is required to verify
        computed = prefix_to_netmask(prefix_len)  # => co-04: hand-rolled bit-string-slicing conversion
        print(f"  /{prefix_len} -> {computed}  (reference: {expected})")  # => co-04: shows the computed value next to the known-correct one
        assert computed == expected, f"/{prefix_len} must convert to {expected}, got {computed}"  # => co-04: the exact-match check
        stdlib_mask = str(ipaddress.IPv4Network(f"0.0.0.0/{prefix_len}").netmask)  # => co-04: an INDEPENDENT parser, never touched by prefix_to_netmask() above
        assert computed == stdlib_mask, f"hand-rolled mask must match ipaddress's own netmask for /{prefix_len}"  # => co-04
    print("All three prefixes match both the reference table and ipaddress's own parser: True")  # => co-04: every assert passed
    # => co-04: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
