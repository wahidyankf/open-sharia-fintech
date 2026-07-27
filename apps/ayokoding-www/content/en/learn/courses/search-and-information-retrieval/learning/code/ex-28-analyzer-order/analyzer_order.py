# pyright: strict
"""Example 28: Analyzer Order (co-06, co-07, co-08, co-09)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def _cv_string(
    word: str,
) -> str:  # => classify every letter of word as 'c' (consonant) or 'v' (vowel) per
    """Classify every letter of word as 'c' (consonant) or 'v' (vowel) per
    Porter's definition, where 'y' is a vowel only when preceded by a
    consonant (or is a consonant at word-start)."""
    result: list[str] = []  # => starts empty, populated by the loop below
    for i, ch in enumerate(word):  # => iterates one item at a time
        if ch in "aeiou":  # => true when ch in "aeiou"
            result.append("v")  # => records this item, in order
        elif ch == "y":  # => otherwise, true when ch == "y"
            result.append(
                "c" if i == 0 or result[i - 1] == "v" else "v"
            )  # => records this item, in order
        else:  # => the fallback branch, when no prior condition matched
            result.append("c")  # => records this item, in order
    return "".join(result)  # => returns "".join(result)


def _measure(
    stem: str,
) -> int:  # => porter's m: the count of VC repetitions in [C](VC)^m[V]
    """Porter's m: the count of VC repetitions in [C](VC)^m[V]."""
    cv = _cv_string(stem)  # => cv = _cv_string(stem)
    collapsed: list[str] = []  # => starts empty, populated by the loop below
    for ch in cv:  # => collapses runs of the same letter type into one marker
        if (
            not collapsed or collapsed[-1] != ch
        ):  # => true when not collapsed or collapsed[-1] != ch
            collapsed.append(ch)  # => records this item, in order
    pattern = "".join(collapsed)  # => pattern = "".join(collapsed)
    if pattern.startswith("c"):  # => true when pattern.startswith("c")
        pattern = pattern[1:]  # => strips the optional leading consonant run
    if pattern.endswith("v"):  # => true when pattern.endswith("v")
        pattern = pattern[:-1]  # => strips the optional trailing vowel run
    return (
        len(pattern) // 2
    )  # => what remains is (vc)^m -- each pair is one unit of measure


def _contains_vowel(stem: str) -> bool:  # => defines  contains vowel
    return "v" in _cv_string(stem)  # => the *v* condition Porter's ED/ING rules require


def _ends_double_consonant(stem: str) -> bool:  # => defines  ends double consonant
    if len(stem) < 2:  # => true when len(stem) < 2
        return False  # => returns False
    cv = _cv_string(stem)  # => cv = _cv_string(stem)
    return cv[-1] == "c" and cv[-2] == "c" and stem[-1] == stem[-2]  # => e.g. "hopp"


def _ends_cvc(stem: str) -> bool:  # => defines  ends cvc
    if len(stem) < 3:  # => true when len(stem) < 3
        return False  # => returns False
    cv = _cv_string(stem)  # => cv = _cv_string(stem)
    return cv[-3:] == "cvc" and stem[-1] not in "wxy"  # => Porter's *o condition


def _step1a(word: str) -> str:  # => defines  step1a
    if word.endswith("sses"):  # => true when word.endswith("sses")
        return word[:-2]  # => caresses -> caress
    if word.endswith("ies"):  # => true when word.endswith("ies")
        return word[:-2]  # => ponies -> poni
    if word.endswith("ss"):  # => true when word.endswith("ss")
        return word  # => caress -> caress (unchanged)
    if word.endswith("s"):  # => true when word.endswith("s")
        return word[:-1]  # => cats -> cat
    return word  # => returns word


def _step1b_cleanup(stem: str) -> str:  # => defines  step1b cleanup
    if stem.endswith(
        ("at", "bl", "iz")
    ):  # => true when stem.endswith(("at", "bl", "iz"))
        return stem + "e"  # => conflat(ed) -> conflate
    if _ends_double_consonant(stem) and not stem.endswith(
        ("l", "s", "z")
    ):  # => true when _ends_double_consonant(stem) and not stem.endswith((...
        return stem[:-1]  # => hopp(ing) -> hop
    if _measure(stem) == 1 and _ends_cvc(
        stem
    ):  # => true when _measure(stem) == 1 and _ends_cvc(stem)
        return stem + "e"  # => fil(ing) -> file
    return stem  # => returns stem


def _step1b(word: str) -> str:  # => defines  step1b
    if word.endswith("eed"):  # => true when word.endswith("eed")
        stem = word[:-3]  # => stem = word[:-3]
        return stem + "ee" if _measure(stem) > 0 else word  # => agreed -> agree
    if word.endswith("ed"):  # => true when word.endswith("ed")
        stem = word[:-2]  # => stem = word[:-2]
        return (
            _step1b_cleanup(stem) if _contains_vowel(stem) else word
        )  # => returns _step1b_cleanup(stem) if _contains_vowel(stem) else word
    if word.endswith("ing"):  # => true when word.endswith("ing")
        stem = word[:-3]  # => stem = word[:-3]
        return (
            _step1b_cleanup(stem) if _contains_vowel(stem) else word
        )  # => returns _step1b_cleanup(stem) if _contains_vowel(stem) else word
    return word  # => returns word


def _step1c(word: str) -> str:  # => defines  step1c
    if word.endswith("y") and _contains_vowel(
        word[:-1]
    ):  # => true when word.endswith("y") and _contains_vowel(word[:-1])
        return word[:-1] + "i"  # => happy -> happi
    return word  # => returns word


_STEP2 = [  # =>  STEP2 = [
    ("ational", "ate"),
    ("tional", "tion"),
    ("enci", "ence"),
    (
        "anci",
        "ance",
    ),  # => part of this step's computation, continued from the line above
    ("izer", "ize"),
    ("abli", "able"),
    ("alli", "al"),
    (
        "entli",
        "ent",
    ),  # => part of this step's computation, continued from the line above
    ("eli", "e"),
    ("ousli", "ous"),
    ("ization", "ize"),
    (
        "ation",
        "ate",
    ),  # => part of this step's computation, continued from the line above
    ("ator", "ate"),
    ("alism", "al"),
    ("iveness", "ive"),
    (
        "fulness",
        "ful",
    ),  # => part of this step's computation, continued from the line above
    ("ousness", "ous"),
    ("aliti", "al"),
    ("iviti", "ive"),
    (
        "biliti",
        "ble",
    ),  # => part of this step's computation, continued from the line above
]  # => sorted longest-suffix-first below, so "ization" wins over "ation"


def _step2(word: str) -> str:  # => defines  step2
    for suf, repl in sorted(
        _STEP2, key=lambda p: len(p[0]), reverse=True
    ):  # => iterates one item at a time
        if word.endswith(suf):  # => true when word.endswith(suf)
            stem = word[: -len(suf)]  # => stem = word[: -len(suf)]
            return (
                stem + repl if _measure(stem) > 0 else word
            )  # => relational -> relate
    return word  # => returns word


_STEP3 = [
    ("icate", "ic"),
    ("ative", ""),
    ("alize", "al"),
    ("iciti", "ic"),
    ("ical", "ic"),
    ("ful", ""),
    ("ness", ""),
]  # =>  STEP3 = [("icate", "ic"), ("ative", ""), ("alize", "al"...


def _step3(word: str) -> str:  # => defines  step3
    for suf, repl in sorted(
        _STEP3, key=lambda p: len(p[0]), reverse=True
    ):  # => iterates one item at a time
        if word.endswith(suf):  # => true when word.endswith(suf)
            stem = word[: -len(suf)]  # => stem = word[: -len(suf)]
            return stem + repl if _measure(stem) > 0 else word  # => hopeful -> hope
    return word  # => returns word


_STEP4 = [
    "al",
    "ance",
    "ence",
    "er",
    "ic",
    "able",
    "ible",
    "ant",
    "ement",
    "ment",
    "ent",
    "ou",
    "ism",
    "ate",
    "iti",
    "ous",
    "ive",
    "ize",
]  # =>  STEP4 = ["al", "ance", "ence", "er", "ic", "able", "ibl...


def _step4(word: str) -> str:  # => defines  step4
    if word.endswith("ion"):  # => true when word.endswith("ion")
        stem = word[:-3]  # => stem = word[:-3]
        if _measure(stem) > 1 and stem.endswith(
            ("s", "t")
        ):  # => true when _measure(stem) > 1 and stem.endswith(("s", "t"))
            return stem  # => adoption -> adopt (only after s/t, and only if m>1)
    for suf in sorted(_STEP4, key=len, reverse=True):  # => iterates one item at a time
        if word.endswith(suf):  # => true when word.endswith(suf)
            stem = word[: -len(suf)]  # => stem = word[: -len(suf)]
            return (
                stem if _measure(stem) > 1 else word
            )  # => airliner -> airlin (m>1 required)
    return word  # => returns word


def _step5a(word: str) -> str:  # => defines  step5a
    if word.endswith("e"):  # => true when word.endswith("e")
        stem = word[:-1]  # => stem = word[:-1]
        m = _measure(stem)  # => m = _measure(stem)
        if m > 1 or (
            m == 1 and not _ends_cvc(stem)
        ):  # => true when m > 1 or (m == 1 and not _ends_cvc(stem))
            return stem  # => probate -> probat, but cease stays cease (m==1 and *o)
    return word  # => returns word


def _step5b(word: str) -> str:  # => defines  step5b
    if (
        _measure(word) > 1 and _ends_double_consonant(word) and word.endswith("l")
    ):  # => true when _measure(word) > 1 and _ends_double_consonant(word) ...
        return word[:-1]  # => controll -> control
    return word  # => returns word


def porter_stem(
    word: str,
) -> str:  # => reduce word to its Porter (1980) stem by chaining Steps 1a through 5b
    """Reduce word to its Porter (1980) stem by chaining Steps 1a through 5b."""
    if len(word) <= 2:  # => true when len(word) <= 2
        return word  # => Porter's algorithm is a no-op below 3 letters
    w = word.lower()  # => w = word.lower()
    for step in (
        _step1a,
        _step1b,
        _step1c,
        _step2,
        _step3,
        _step4,
        _step5a,
        _step5b,
    ):  # => iterates one item at a time
        w = step(
            w
        )  # => each step's OUTPUT feeds the next step's INPUT, in this fixed order
    return w  # => returns w


STOP_WORDS: frozenset[str] = frozenset(
    {"the", "a", "an", "of", "in", "on", "and", "or", "to", "is", "are", "for"}
)  # => STOP WORDS = frozenset({"the", "a", "an", "of", "in", "on", ...


def analyze(
    text: str,
) -> list[
    str
]:  # => chain tokenize -> case-fold -> stop-word drop -> stem, in that fixed order
    """Chain tokenize -> case-fold -> stop-word drop -> stem, in that fixed order."""
    tokens: list[str] = text.split()  # => co-06: stage 1 -- whitespace tokenization
    folded: list[str] = [t.lower() for t in tokens]  # => co-07: stage 2 -- case folding
    filtered: list[str] = [
        t for t in folded if t not in STOP_WORDS
    ]  # => co-08: stage 3 -- stop-word removal
    stemmed: list[str] = [
        porter_stem(t) for t in filtered
    ]  # => co-09: stage 4 -- stemming, applied LAST
    return stemmed  # => returns stemmed


def main() -> None:  # => defines main
    text: str = "The Runners are running to the finish and jumping around happily"  # => mixed case, stop words, plural/ing/Y-suffix forms
    result: list[str] = analyze(
        text
    )  # => co-06,07,08,09: the full 4-stage pipeline in one call
    print(f"input:  {text!r}")  # => shows input
    print(f"output: {result}")  # => shows output

    # Hand-traced through all 4 stages: tokenize -> fold -> drop {the, are, to, and} -> stem.
    # "happily" ends in Y preceded by a vowel-containing stem ("happil"), so Porter's Step 1c
    # converts Y -> I, giving "happili" -- genuine algorithm behavior, not a typo.
    expected: list[str] = [
        "runner",
        "run",
        "finish",
        "jump",
        "around",
        "happili",
    ]  # => expected = ["runner", "run", "finish", "jump", "around", "...
    assert result == expected, (
        f"expected {expected}, got {result}"
    )  # => expected {expected}, got {result}
    assert "the" not in result, (
        "stage 3 must remove 'the' before stage 4 ever sees it"
    )  # => stage 3 must remove 'the' before stage 4 ever sees it
    assert "and" not in result, (
        "stage 3 must remove 'and' too"
    )  # => stage 3 must remove 'and' too
    print(
        f"MATCH: the 4-stage pipeline's output equals the hand-traced fixture {expected}"
    )  # => shows MATCH: the 4-stage pipeline's output equals the hand-traced fixture


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
