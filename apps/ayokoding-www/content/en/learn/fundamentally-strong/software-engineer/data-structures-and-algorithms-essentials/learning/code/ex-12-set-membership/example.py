"""Example 12: Set Membership Testing."""

# set gives average-O(1) "is this in here?" via the same hashing as dict (co-09).
vip_ids: set[int] = {101, 202, 303}  # => a hash set literal, unordered

is_vip = 202 in vip_ids  # => hashes 202 and checks its bucket -- O(1) average
is_not_vip = 404 in vip_ids  # => hashes 404 -- bucket empty, no scan needed
print(is_vip)  # => Output: True
print(is_not_vip)  # => Output: False

assert is_vip is True  # => confirms a present element reports True
assert is_not_vip is False  # => confirms an absent element reports False
assert 101 in vip_ids and 303 in vip_ids  # => confirms both other members are present
print("ex-12 OK")  # => Output: ex-12 OK
