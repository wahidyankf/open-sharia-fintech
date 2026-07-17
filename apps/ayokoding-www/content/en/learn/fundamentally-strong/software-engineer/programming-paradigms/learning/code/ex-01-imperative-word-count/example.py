"""Example 1: Imperative Word Count."""

text: str = "the cat sat on the mat the cat ran"  # => sample sentence, "the" and "cat" repeat
counts: dict[str, int] = {}  # => mutable box we will update step by step -- the imperative core
for word in text.split():  # => explicit loop: step through every word one at a time
    if word in counts:  # => explicit selection: has this word been seen before?
        counts[word] = counts[word] + 1  # => explicit statement: mutate the box in place
    else:  # => selection's other branch
        counts[word] = 1  # => explicit statement: first sighting, start the box at 1
    # => nothing here is a value being computed and returned -- every step mutates `counts`

print(counts["the"])  # => reads the mutated box after the loop finished
# => Output: 3
print(counts["cat"])  # => reads a second entry from the same mutated box
# => Output: 2
print(len(counts))  # => five distinct words were tallied: the, cat, sat, on, mat, ran = 6
# => Output: 6
