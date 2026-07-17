"""Example 2: Procedural Decompose."""

import inspect


def tokenize(text: str) -> list[str]:  # => named procedure #1: text -> list of words
    return text.split()  # => the ONLY thing this procedure does -- splitting


def tally(words: list[str]) -> dict[str, int]:  # => named procedure #2: words -> counts
    counts: dict[str, int] = {}  # => local mutable box, scoped to this procedure only
    for word in words:  # => explicit loop, same mechanics as example 1
        counts[word] = counts.get(word, 0) + 1  # => bump the count, default to 0 first time
    return counts  # => hand the finished box back to the caller


def main(text: str) -> dict[str, int]:  # => the orchestrator -- now tiny and readable
    words = tokenize(text)  # => step 1: delegate to tokenize
    return tally(words)  # => step 2: delegate to tally, nothing else happens here


result: dict[str, int] = main("the cat sat on the mat the cat ran")  # => same input as example 1
print(result["the"])  # => identical counts to the inline loop version
# => Output: 3
print(result["cat"])  # => same second count
# => Output: 2

main_body_lines: int = len(inspect.getsource(main).strip().splitlines())  # => count main()'s own lines
print(main_body_lines)  # => main() is 3 lines: def + two delegating calls, no loop logic inline
# => Output: 3
