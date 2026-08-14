def complete(_: str) -> str:
    return "offline mock"  # => mock replaces paid provider


assert complete("hello") == "offline mock"  # => test requires no key or network
print("PASS: no-key-required-mock")  # => offline acceptance result
