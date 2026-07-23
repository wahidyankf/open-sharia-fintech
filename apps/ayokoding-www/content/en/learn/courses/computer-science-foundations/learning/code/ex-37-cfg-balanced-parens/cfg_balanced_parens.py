# learning/code/ex-37-cfg-balanced-parens/cfg_balanced_parens.py
"""Example 37: A CFG for Balanced Parentheses, Checked by a Recursive-Descent Parser."""  # => co-20: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

# ex-37: the CFG this parser implements, in BNF -- a genuinely CONTEXT-FREE grammar (co-20):
#   S -> "(" S ")" S | ε
# Every production's left-hand side is a SINGLE nonterminal (S), the defining trait of context-free.


def parse_balanced(s: str, pos: int = 0) -> int | None:  # => co-20: recursive-descent parser for the CFG above
    """Try to parse a balanced-parens prefix of s starting at pos; return the end index, or None if invalid."""  # => co-20: documents parse_balanced's contract -- no runtime output, just sets its __doc__
    while pos < len(s) and s[pos] == "(":  # => co-20: S -> "(" S ")" S -- consume opens, recursing per production
        inner_end = parse_balanced(s, pos + 1)  # => co-20: recursively parse the matching S inside this "("
        if inner_end is None or inner_end >= len(s) or s[inner_end] != ")":  # => co-20: the closing ")" MUST be there
            return None  # => co-20: malformed -- no matching close, or ran out of input
        pos = inner_end + 1  # => co-20: past the ")" -- continue parsing the OUTER S's own trailing S
    return pos  # => co-20: S -> ε -- nothing left to consume at this nesting level, return where parsing stopped


def is_balanced(s: str) -> bool:  # => co-20: accepted iff the WHOLE string is consumed by one S derivation
    """True iff s is entirely balanced parentheses, per the CFG S -> ( S ) S | ε."""  # => co-20: documents is_balanced's contract -- no runtime output, just sets its __doc__
    end = parse_balanced(s)  # => co-20: parse from position 0
    return end is not None and end == len(s)  # => co-20: must consume EVERY character, not just a prefix


if __name__ == "__main__":  # => co-20: entry point -- this block runs only when the file executes directly, not on import
    test_cases = {  # => co-20: string -> hand-verified balanced/unbalanced expectation
        "": True,  # => co-20: the empty string -- S -> ε, the base case
        "()": True,  # => co-20: one S -> "(" S ")" S step, both inner S's empty
        "(())": True,  # => co-20: nested pair, both levels a valid S
        "()()": True,  # => co-20: two sibling pairs, S's trailing S production
        "(()())": True,  # => co-20: valid derivations of S
        "(": False,  # => co-20: an open with no matching close -- no S derivation
        ")": False,  # => co-20: a close with no preceding open -- no S derivation
        "(()": False,  # => co-20: inner pair closes but the outer open never does
        "())": False,  # => co-20: a close with nothing left open to match
        ")(": False,  # => co-20: no valid S derivation
    }  # => co-20: closes the multi-line construct opened above
    for s, expected in test_cases.items():  # => co-20: run every case through the recursive-descent parser
        actual = is_balanced(s)  # => co-20: the CFG-derived parser's own verdict
        print(f"{s!r:<8} balanced={actual} expected={expected}")  # => co-20: per-case report
        assert actual == expected, f"balanced-parens verdict for {s!r} must be {expected}"  # => co-20
    print(f"All balanced and unbalanced strings classified correctly: True")  # => co-20: every assert passed
    # => co-20: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
