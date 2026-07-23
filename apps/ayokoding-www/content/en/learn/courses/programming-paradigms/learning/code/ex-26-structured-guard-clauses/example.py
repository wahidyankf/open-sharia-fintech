"""Example 26: Structured Guard Clauses."""


def discount_nested(is_member: bool, cart_total: int, has_coupon: bool) -> int:  # => BEFORE: a nested pyramid
    if is_member:  # => level 1
        if cart_total > 100:  # => level 2, indented inside level 1
            if has_coupon:  # => level 3, indented inside level 2
                return cart_total - 30  # => three levels deep before reaching the real logic
            else:  # => the has_coupon-False branch, still three levels deep
                return cart_total - 20  # => still three levels deep
        else:  # => the cart_total<=100 branch, back out to two levels deep
            return cart_total - 10  # => two levels deep
    else:  # => the not-a-member branch, back out to one level deep
        return cart_total  # => back at level 1 -- the "no discount" case is buried at the bottom


def discount_guarded(is_member: bool, cart_total: int, has_coupon: bool) -> int:  # => AFTER: early returns
    if not is_member:  # => guard #1: handle the simplest case first and exit immediately
        return cart_total  # => zero nesting for the "no discount" case
    if cart_total <= 100:  # => guard #2: handle the next simplest case, still zero extra nesting
        return cart_total - 10  # => guard #2's result: same value as the nested version's level-2 branch
    if has_coupon:  # => guard #3: only the remaining, most-specific case reaches here
        return cart_total - 30  # => guard #3's result: same value as the nested version's level-3 branch
    return cart_total - 20  # => the final fallthrough case, at the SAME nesting level as every guard


for is_member, total, has_coupon in (  # => exercise every branch of both versions
    (False, 50, False),  # => not a member: both versions must return 50 unchanged
    (True, 50, False),  # => member, cart <= 100: both versions apply the 10-off tier
    (True, 150, False),  # => member, cart > 100, no coupon: both versions apply the 20-off tier
    (True, 150, True),  # => member, cart > 100, with coupon: both versions apply the 30-off tier
):  # => closes the tuple of cases driving both functions through every branch
    nested = discount_nested(is_member, total, has_coupon)  # => run the BEFORE version
    guarded = discount_guarded(is_member, total, has_coupon)  # => run the AFTER version
    print(nested == guarded, guarded)  # => both must agree, for every combination
# => Output: True 50
# => Output: True 40
# => Output: True 130
# => Output: True 120
