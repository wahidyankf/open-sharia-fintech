"""Example 27: while Loop."""

# while loops require an explicit exit condition -- for loops handle known ranges instead.
n: int = 3  # => n is 3 (type: int) -- the loop counter
while n >= 0:  # => keeps looping as long as the condition stays True
    print(n)  # => Output: 3, then 2, then 1, then 0
    n -= 1  # => must shrink n each pass, or the loop never ends
