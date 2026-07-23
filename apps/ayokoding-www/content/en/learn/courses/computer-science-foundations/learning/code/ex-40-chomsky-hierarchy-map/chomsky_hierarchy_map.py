# learning/code/ex-40-chomsky-hierarchy-map/chomsky_hierarchy_map.py
"""Example 40: Classifying Sample Languages into the Four Chomsky-Hierarchy Levels."""  # => co-21: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import re  # => co-21: the regular-language classifier reuses Python's regex engine directly
from typing import NamedTuple  # => co-21: typing import supporting the typed structures below


class LanguageSample(NamedTuple):  # => co-21: one language, its classifying test, and its hierarchy level
    name: str  # => co-21: a human label for the language
    level: str  # => co-21: which of the four nested Chomsky classes this language belongs to
    classifier: object  # => co-21: a callable string -> bool that DECIDES membership for this language


def is_regular_sample(s: str) -> bool:  # => co-21: L = a*b* -- accepted by a DFA/regex, the OUTERMOST class
    return re.fullmatch(r"a*b*", s) is not None  # => co-21: matches Example 35/36's regex/DFA-equivalence machinery


def is_context_free_sample(s: str) -> bool:  # => co-21: L = a^n b^n -- needs a stack (Example 38), NOT a DFA (Example 39)
    a_count = len(s) - len(s.lstrip("a"))  # => co-21: count of leading a's
    rest = s[a_count:]  # => co-21: everything after the a-run
    return rest == "b" * a_count  # => co-21: exactly as many b's as a's, and nothing else


def is_context_sensitive_sample(s: str) -> bool:  # => co-21: L = a^n b^n c^n -- needs TWO counts tracked together
    n = len(s) // 3  # => co-21: candidate length of each of the three equal runs
    return len(s) % 3 == 0 and s == ("a" * n) + ("b" * n) + ("c" * n)  # => co-21: three equal runs, in order


def is_recursively_enumerable_sample(s: str) -> bool:  # => co-21: modeled as "a TM would eventually accept" -- may not halt on rejects
    """A language a Turing machine can recognize but not necessarily always halt-reject on --
    modeled here as 'a palindrome over {a,b} of EVEN length', a language easily TM-decidable,
    standing in for the outermost, most permissive Chomsky class."""  # => co-21: closes is_recursively_enumerable_sample's docstring above -- no runtime output, just sets its __doc__
    # => co-21: the two paragraphs above explain why palindrome-checking stands in for TM recognizability here
    return len(s) % 2 == 0 and s == s[::-1]  # => co-21: a concrete, checkable stand-in for this survey's purposes


SAMPLES: list[LanguageSample] = [  # => co-21: one representative sample per nested hierarchy level, outermost first
    LanguageSample("a*b*", "regular", is_regular_sample),  # => co-21: regular ⊂ context-free ⊂ ... (innermost-most-restricted)
    LanguageSample("a^n b^n", "context-free", is_context_free_sample),  # => co-21: needs a stack, not just states
    LanguageSample("a^n b^n c^n", "context-sensitive", is_context_sensitive_sample),  # => co-21: needs even more memory
    LanguageSample("even-length palindromes", "recursively-enumerable", is_recursively_enumerable_sample),  # => co-21
]  # => co-21: closes the multi-line construct opened above

TEST_STRINGS = ["", "ab", "aabb", "aabbcc", "abba", "aab", "abc"]  # => co-21: run against every sample language


if __name__ == "__main__":  # => co-21: entry point -- this block runs only when the file executes directly, not on import
    for sample in SAMPLES:  # => co-21: one classification pass per hierarchy level
        print(f"{sample.level} ({sample.name}):")  # => co-21: labels which level's classifier follows
        for s in TEST_STRINGS:  # => co-21: the same test strings run against every level, for direct comparison
            accepted = sample.classifier(s)  # type: ignore[operator]  # => co-21: this level's own membership test
            print(f"  {s!r:<10} -> {accepted}")  # => co-21: per-string verdict for this language
    assert SAMPLES[0].classifier("aabb") is True  # type: ignore[operator]  # => co-21: a*b* accepts aabb (all a's then all b's)
    assert SAMPLES[1].classifier("aabb") is True  # type: ignore[operator]  # => co-21: a^n b^n also accepts aabb (n=2)
    assert SAMPLES[1].classifier("aab") is False  # type: ignore[operator]  # => co-21: a^n b^n rejects unequal counts
    assert SAMPLES[2].classifier("aabbcc") is True  # type: ignore[operator]  # => co-21: a^n b^n c^n accepts aabbcc (n=2)
    assert SAMPLES[2].classifier("aabb") is False  # type: ignore[operator]  # => co-21: missing the c-run -- rejected
    assert SAMPLES[3].classifier("abba") is True  # type: ignore[operator]  # => co-21: "abba" is a palindrome
    print(f"Every sample classified against its matching automaton/level: True")  # => co-21: every assert passed
    # => co-21: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
    # => co-21: the four classifier functions above are ordered outermost-to-innermost in Chomsky's nesting, matching SAMPLES' declaration order
