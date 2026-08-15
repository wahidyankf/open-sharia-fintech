# => Initialize or update deterministic state used by this demonstration.
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


# => Isolate the operation so its observable behavior can be checked.
def base62(number: int) -> str:
    # Zero has a real one-character encoding instead of an empty string.
    # => Choose the branch that models this design condition.
    if number == 0:
        # => Return the observable result of this modeled operation.
        return ALPHABET[0]
    # Repeated division emits the least-significant base62 digit first.
    # => Initialize or update deterministic state used by this demonstration.
    digits: list[str] = []
    # => Repeat the deterministic step over the current input.
    while number:
        # => Initialize or update deterministic state used by this demonstration.
        number, remainder = divmod(number, len(ALPHABET))
        # => Initialize or update deterministic state used by this demonstration.
        digits.append(ALPHABET[remainder])
    # => Return the observable result of this modeled operation.
    return "".join(reversed(digits))


# => Initialize or update deterministic state used by this demonstration.
codes = {base62(identifier) for identifier in range(10_000)}
# Unique numeric IDs yield unique compact codes; storage still enforces uniqueness.
# => Check the promised observable behavior of the demonstration.
assert len(codes) == 10_000 and base62(62) == "10"
# => Emit the final observable state for a direct run.
print(base62(12_345))
