"""Example 27: Bloom Filter Membership Test."""

import hashlib  # => stdlib module supplying the independent hash functions this filter needs

# A Bloom filter answers "definitely absent" or "maybe present" using a fixed
# bit array and several independent hash functions (co-15) -- adding a key
# sets K bits; querying checks the SAME K bits, so every added key is always
# reported present (no false negatives -- proven in Example 28).
BIT_COUNT: int = 64  # => size of the underlying bit array
HASH_COUNT: int = 3  # => number of independent hash functions per key


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


bits = bytearray(BIT_COUNT)  # => one byte per bit for simplicity -- 0 or 1


def add(key: str) -> None:  # => marks a key as a member by setting its K bits
    for pos in bit_positions(key):
        bits[pos] = 1  # => set every one of this key's K bits


def might_contain(
    key: str,
) -> bool:  # => "maybe present" (True) or "definitely absent" (False)
    return all(
        bits[pos] == 1 for pos in bit_positions(key)
    )  # => ALL K bits must be set


add("alice")  # => sets alice's K bits
add("bob")  # => sets bob's K bits (may share some positions with alice -- that's fine)
print(might_contain("alice"))  # => Output: True
print(might_contain("bob"))  # => Output: True

assert might_contain("alice") is True  # => an added key always reports present
assert might_contain("bob") is True  # => same for every other added key
print("ex-27 OK")  # => Output: ex-27 OK
