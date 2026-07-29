# pyright: strict
"""Example 32: Refresh-token rotation. (co-18)

Short-lived access tokens limit a stolen token's lifetime; a long-lived
refresh token lets a client get a NEW access token without re-authenticating.
ROTATION issues a NEW refresh token on every use, so each refresh token is
single-use. NOTE: RFC 9700 Sec 2.2.2 requires public-client refresh tokens to
be "sender-constrained OR use rotation" -- one of two mitigations, not an
unconditional mandate.
"""

from dataclasses import dataclass  # => a small typed record for the issued pair


@dataclass(frozen=True)  # => co-18: the pair a refresh issues: a new access token + a NEW rotated refresh
class TokenPair:
    access_token: str  # => short-lived bearer token
    refresh_token: str  # => the NEW refresh token (the old one is now invalid)


# The store of CURRENTLY-valid refresh tokens. Rotation removes the used one and adds the new one.
VALID_REFRESH: set[str] = {"refresh-0"}  # => the initial refresh token issued at sign-in
ISSUE_COUNTER = [1]  # => a counter to mint distinct new tokens deterministically


def rotate(presented_refresh: str) -> TokenPair | None:  # => co-18: exchange a refresh for a new pair
    if presented_refresh not in VALID_REFRESH:  # => the presented refresh is not (or no longer) valid
        return None  # => rejected
    VALID_REFRESH.remove(presented_refresh)  # => co-18: rotation -- the used refresh is now INVALID
    new_refresh = f"refresh-{ISSUE_COUNTER[0]}"  # => mint a NEW single-use refresh token
    ISSUE_COUNTER[0] += 1  # => advance the counter
    VALID_REFRESH.add(new_refresh)  # => the new refresh is now the only valid one
    return TokenPair(access_token=f"access-{ISSUE_COUNTER[0]}", refresh_token=new_refresh)  # => the new pair


first = rotate("refresh-0")  # => co-18: the initial refresh -> a new access + rotated refresh
assert first is not None  # => type-narrow for pyright
print(f"first rotation:  access={first.access_token}, refresh={first.refresh_token}")  # => Output: new pair

second = rotate(first.refresh_token)  # => co-18: the rotated refresh -> ANOTHER new pair
assert second is not None  # => type-narrow
print(f"second rotation: access={second.access_token}, refresh={second.refresh_token}")  # => Output: another new pair

reused = rotate(first.refresh_token)  # => co-18: the OLD (already-rotated) refresh -> REJECTED
print(f"reused old refresh: {reused}")  # => Output: None -- single-use, rotation invalidated it

assert second.refresh_token != first.refresh_token  # => co-18: each rotation mints a distinct refresh
assert reused is None  # => co-18: an already-used refresh is no longer valid
