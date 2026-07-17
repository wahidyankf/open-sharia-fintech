"""Example 4: Mutable Variable Box."""

x: int = 10  # => x names a box holding 10
print(x)  # => reads the box
# => Output: 10
x = 20  # => reassignment REBINDS the name x to a new value -- the imperative core (co-04)
print(x)  # => the SAME name now reads a different value -- rebinding, not mutation of "10"
# => Output: 20

original: list[int] = [1, 2, 3]  # => a genuinely mutable object: a list
alias: list[int] = original  # => alias is NOT a copy -- both names point at the same box
alias.append(4)  # => this mutates the shared list object in place
print(original)  # => original "sees" the change too, because they share one underlying box
# => Output: [1, 2, 3, 4]
print(original is alias)  # => confirms both names are bound to the identical object
# => Output: True
