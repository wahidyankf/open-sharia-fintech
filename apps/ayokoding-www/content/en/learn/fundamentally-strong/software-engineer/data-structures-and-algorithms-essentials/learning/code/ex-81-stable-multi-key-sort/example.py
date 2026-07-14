"""Example 81: Stable Multi-Key Sort with a Tuple Key."""

# key=lambda returning a TUPLE sorts by the first field, breaking ties with the
# second -- Timsort's STABILITY means equal-key elements keep their relative
# input order, which is what makes this technique reliable (co-15).
records: list[tuple[str, int]] = [
    ("bob", 85),  # => a mid score
    ("alice", 90),  # => a top score
    ("carol", 85),  # => ties bob's score
    ("dave", 90),  # => ties alice's score
]  # => (name, score) pairs -- several scores tie

by_score_then_name = sorted(records, key=lambda r: (-r[1], r[0]))
# => -r[1] sorts score DESCENDING (highest first); r[0] breaks ties alphabetically
print(
    by_score_then_name
)  # => Output: [('alice', 90), ('dave', 90), ('bob', 85), ('carol', 85)]

assert by_score_then_name == [
    ("alice", 90),  # => highest score, alphabetically first among the 90s
    ("dave", 90),  # => ties alice's 90 -- kept AFTER alice by the name tiebreak
    ("bob", 85),  # => next score tier, alphabetically first among the 85s
    ("carol", 85),  # => ties bob's 85 -- kept AFTER bob by the name tiebreak
]  # => confirms primary key (score desc) then secondary key (name asc) both hold
print("ex-81 OK")  # => Output: ex-81 OK
