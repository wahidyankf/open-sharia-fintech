"""Example 3: Structured Three Constructs."""


def classify_flagged(n: int) -> str:  # => the BEFORE version: a boolean "goto flag" hack
    result = ""  # => mutable accumulator that later code branches decide whether to touch
    done = False  # => the "goto flag" -- a boolean standing in for a jump target
    if n < 0 and not done:  # => every later check must also test `not done` to fake a jump
        result = "negative"  # => sets the outcome
        done = True  # => "jump past the rest" by flipping the flag
    if n == 0 and not done:  # => repeats the same flag-guard boilerplate
        result = "zero"  # => sets the outcome
        done = True  # => flips the flag again
    if n > 0 and not done:  # => and again -- the flag is checked at every single branch
        result = "positive"  # => sets the outcome
        done = True  # => flips the flag one more time, though nothing reads it after this
    return result  # => the flag pattern adds bookkeeping with no structural payoff


def classify_structured(n: int) -> str:  # => the AFTER version: sequence + selection only
    if n < 0:  # => plain selection -- one of structured programming's three constructs, no flag needed
        return "negative"  # => sequence: return is the only "next step" needed
    elif n == 0:  # => selection's next branch, mutually exclusive with the first
        return "zero"  # => sequence
    else:  # => selection's final branch
        return "positive"  # => sequence
    # => no boolean flag anywhere -- each branch's `return` IS the control transfer


for n in (-3, 0, 5):  # => iteration: the third of the three structured constructs
    before = classify_flagged(n)  # => run the flag-based version
    after = classify_structured(n)  # => run the structured version
    print(before == after, after)  # => confirms both versions agree, for every case
# => Output: True negative
# => Output: True zero
# => Output: True positive
