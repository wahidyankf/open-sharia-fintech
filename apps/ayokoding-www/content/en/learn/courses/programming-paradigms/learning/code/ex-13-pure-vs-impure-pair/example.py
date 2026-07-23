"""Example 13: Pure vs Impure Pair."""

log: list[str] = []  # => a module-level "side channel" the impure function writes to


def normalize(text: str) -> str:  # => PURE: output depends only on the input, no visible side effect
    return text.strip().lower()  # => reads only its argument, writes to nothing outside itself


def normalize_and_log(text: str) -> str:  # => IMPURE: same math, plus a side effect
    result = text.strip().lower()  # => identical computation to the pure version
    log.append(f"normalized {text!r} -> {result!r}")  # => SIDE EFFECT: mutates state outside this function
    return result  # => same return value as the pure version


sample = "  Hello WORLD  "  # => shared input for both functions
first_call = normalize(sample)  # => call #1 of the pure function
second_call = normalize(sample)  # => call #2, same argument
print(first_call == second_call)  # => referential transparency: same input, same output, every time
# => Output: True
print(log)  # => the pure function never touched `log` -- it is still empty
# => Output: []

normalize_and_log(sample)  # => call the impure twin once
print(len(log))  # => exactly one entry was appended by the ONE impure call
# => Output: 1
