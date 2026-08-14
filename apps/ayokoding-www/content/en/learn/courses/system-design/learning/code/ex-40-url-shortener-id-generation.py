ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def base62(number: int) -> str:
    # Zero has a real one-character encoding instead of an empty string.
    if number == 0:
        return ALPHABET[0]
    # Repeated division emits the least-significant base62 digit first.
    digits: list[str] = []
    while number:
        number, remainder = divmod(number, len(ALPHABET))
        digits.append(ALPHABET[remainder])
    return "".join(reversed(digits))


codes = {base62(identifier) for identifier in range(10_000)}
# Unique numeric IDs yield unique compact codes; storage still enforces uniqueness.
assert len(codes) == 10_000 and base62(62) == "10"
print(base62(12_345))
