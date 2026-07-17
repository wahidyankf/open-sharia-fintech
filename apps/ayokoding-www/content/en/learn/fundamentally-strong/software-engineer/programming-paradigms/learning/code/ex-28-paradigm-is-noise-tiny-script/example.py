"""Example 28: Paradigm Is Noise (Tiny Script).

This is a 15-line one-off: convert a small CSV-ish string to a total. For a script this
short, choosing "the imperative way" versus "the functional way" is genuinely noise -- neither
choice changes readability, testability, or risk in any way that matters at this size. Written
here the fastest way that came to mind: one plain function, no ceremony, no class, no pipeline
of higher-order combinators. See co-23/co-24: paradigm choice earns its weight only once a
system is big enough to have a dominant axis of change -- this script does not qualify.
"""


def total_from_csv(rows: str) -> int:  # => the fastest-to-write shape for a 15-line script
    # => a functional rewrite (sum() + a generator expression) would be exactly as readable here
    total = 0  # => plain accumulator, no ceremony needed at this size
    # => a fold/reduce would compute the identical value, at the cost of one more concept to know
    for line in rows.strip().splitlines():  # => plain loop -- a comprehension would be equally fine here
        # => .strip() drops leading/trailing blank lines; .splitlines() yields one row string per line
        total += int(line.split(",")[1])  # => grab the second column and add it
        # => split(",") turns "apple,3" into ["apple", "3"]; index [1] is the numeric column
    return total  # => done
    # => the loop has already fully drained `rows` before this line ever runs
    # => nothing about this function's shape would change if the CSV had a thousand rows instead of three


sample = "apple,3\nbanana,5\ncherry,2"  # => tiny inline sample data
# => three rows, columns 3 + 5 + 2 -- small enough that no paradigm choice changes anything that matters
print(total_from_csv(sample))  # => 3 + 5 + 2
# => Output: 10
# => at this size, the "how" (loop vs comprehension vs fold) is genuinely noise -- co-23/co-24
