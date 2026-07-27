"""Example 28: Bloom Filter Never False-Negatives."""

import hashlib  # => stdlib module supplying the independent hash functions this filter needs

# A Bloom filter can report a false POSITIVE (an absent key looking present)
# but can NEVER report a false NEGATIVE for a key that was actually added
# (co-15) -- adding a key only ever SETS bits, never clears any, so every
# bit that key's query needs stays set forever.
BIT_COUNT: int = 256  # => a larger bit array -- this example scales up to 200 keys
HASH_COUNT: int = 4  # => number of independent hash functions per key


def bit_positions(
    key: str,
) -> list[int]:  # => derives HASH_COUNT distinct bit positions from one key
    positions: list[int] = []
    for seed in range(HASH_COUNT):  # => one distinct hash per seed value
        digest = hashlib.sha256(
            f"{seed}:{key}".encode()
        ).hexdigest()  # => one hash per seed
        positions.append(
            int(digest, 16) % BIT_COUNT
        )  # => fold the hash down into the bit array's range
    return positions


bits = bytearray(BIT_COUNT)  # => starts all-zero -- no key added yet
added_keys: list[str] = [
    f"key-{i}" for i in range(200)
]  # => 200 keys -- enough to fill the bit array up


def add(
    key: str,
) -> None:  # => marks a key as a member by setting its K bits -- NEVER clears any bit
    for pos in bit_positions(key):
        bits[pos] = 1


def might_contain(
    key: str,
) -> bool:  # => "maybe present" (True) or "definitely absent" (False)
    return all(bits[pos] == 1 for pos in bit_positions(key))


for key in added_keys:  # => add every one of the 200 keys, one at a time
    add(key)

false_negatives = [
    key for key in added_keys if not might_contain(key)
]  # => should stay EMPTY, always
print(len(false_negatives))  # => Output: 0
# => zero out of 200 -- the property holds at scale, not just for one or two toy keys

assert (
    false_negatives == []
)  # => not one of the 200 added keys was ever reported absent
# => this is the guarantee ex-53 relies on when it uses a bloom filter to skip SSTables
print("ex-28 OK")  # => Output: ex-28 OK
# => the tradeoff for this guarantee is space -- more bits and more hashes shrink the false-positive rate
