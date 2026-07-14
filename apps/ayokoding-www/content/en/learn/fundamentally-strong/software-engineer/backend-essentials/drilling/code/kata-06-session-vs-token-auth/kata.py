def check_session(  # => co-17: server-side session -- the STORE, not the cookie, is the source of truth
    session_id: str | None, sessions: dict[str, str]
) -> str | None:
    if session_id is None:  # => no cookie sent at all
        return None
    return sessions.get(session_id)  # => O(1) lookup: cookie is only an opaque KEY into server-side state


def check_bearer_token(  # => co-18: a stateless bearer token -- the token itself carries the identity
    authorization: str | None, valid_tokens: dict[str, str]
) -> tuple[int, str | None]:  # => returns (status, caller) -- no session store consulted at all
    if authorization is None or not authorization.startswith("Bearer "):  # => co-18: missing/malformed
        return 401, None  # => reject BEFORE ever touching valid_tokens
    token = authorization.removeprefix("Bearer ")  # => strip the scheme, keep the opaque token value
    caller = valid_tokens.get(token)  # => co-18: reads Authorization, validates it against known tokens
    if caller is None:  # => the token doesn't match any known-valid entry
        return 401, None
    return 200, caller  # => a good token identifies the caller with no server-side session lookup


sessions: dict[str, str] = {"sess-abc123": "alice"}  # => co-17: session store -- state lives on the SERVER
tokens: dict[str, str] = {"tok-xyz789": "bob"}  # => co-17/co-18: token store -- state lives IN the token

session_hit = check_session("sess-abc123", sessions)  # => cookie resolves via the server-side store
session_miss = check_session("sess-nope", sessions)  # => an unknown/expired session id
print(session_hit, session_miss)  # => Output: alice None

status_ok, caller_ok = check_bearer_token("Bearer tok-xyz789", tokens)  # => a valid bearer token
status_missing, caller_missing = check_bearer_token(None, tokens)  # => co-18: no Authorization header at all
status_bad, caller_bad = check_bearer_token("Bearer tok-wrong", tokens)  # => co-18: a malformed/unknown token
print(status_ok, caller_ok)  # => Output: 200 bob
print(status_missing, caller_missing)  # => Output: 401 None
print(status_bad, caller_bad)  # => Output: 401 None

assert session_hit == "alice" and session_miss is None  # => the cookie alone means nothing without the store
assert (status_ok, caller_ok) == (200, "bob")  # => the token alone is enough -- no store lookup needed
assert status_missing == 401 and status_bad == 401  # => co-18: both reject with 401, not a crash
print("kata-06 OK")
