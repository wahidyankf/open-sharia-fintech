"""Example 5: Lint With Ruff -- deliberately has an unused import."""

# Never referenced below -- ruff's F401 rule flags exactly this.
import json  # => imports the json module but never uses it (deliberately unused)


def greet(name: str) -> str:  # => defines greet, takes name, returns a str
    return f"hello {name}"  # => builds and returns "hello Ada" when called below


print(greet("Ada"))  # => calls greet("Ada"), prints "hello Ada"
# => Output: hello Ada -- the SCRIPT runs fine; ruff still flags it
