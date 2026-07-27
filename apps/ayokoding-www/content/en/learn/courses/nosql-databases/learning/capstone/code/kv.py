"""Capstone Step 1: kv.py -- session-store CRUD against Valkey/Redis (co-20, co-24, co-21).

Builds directly on Example 77's own preview shape: a namespaced "session:<id>" hash, with
a TTL-based expiry the store itself enforces -- no scheduled cleanup job needed. This module
adds the two operations Example 77 did not need: an explicit UPDATE (extend a session's TTL
after activity) and an explicit DELETE (an explicit logout), completing full CRUD.
"""

from __future__ import annotations

import time  # => a real sleep past the TTL window, the same discipline Example 77 established
from typing import cast  # => reconciles redis-py's own dict[bytes | str, bytes | str] stub with the guaranteed-str runtime shape below

import redis  # => redis-py, the official typed Python client for Valkey/Redis (BSD-3-Clause, co-28)

SESSION_KEY_PREFIX = "session:"  # => a namespaced key convention -- every session lives under this prefix


def _session_key(session_id: str) -> str:
    """Build the namespaced key for one session -- the single place this convention is spelled out."""
    return f"{SESSION_KEY_PREFIX}{session_id}"


def create_session(client: redis.Redis, session_id: str, user_id: str, ttl_seconds: int) -> None:
    """CREATE: a session as a Redis hash, with a TTL-based expiry (Example 77's own shape)."""
    key = _session_key(session_id)
    client.hset(key, mapping={"user_id": user_id, "created_at": str(int(time.time()))})  # => a hash, not a plain string
    client.expire(key, ttl_seconds)  # => self-expiring -- no scheduled cleanup job required


def get_session(client: redis.Redis, session_id: str) -> dict[str, str] | None:
    """READ: a session hash back, or None if it has expired or never existed."""
    key = _session_key(session_id)
    data = client.hgetall(key)  # => an EMPTY dict means the key does not exist (expired or never created)
    if not data:  # => this IS the "not found" signal -- Redis never raises for a missing key
        return None
    return cast(dict[str, str], data)  # => decode_responses=True (below) guarantees str keys/values at runtime; the cast narrows redis-py's broader dict[bytes | str, bytes | str] stub to match


def touch_session(client: redis.Redis, session_id: str, extra_ttl_seconds: int) -> bool:
    """UPDATE: extend a session's TTL after activity -- returns False if the session no longer exists."""
    key = _session_key(session_id)
    if not client.exists(key):  # => refuses to resurrect a session that has already expired
        return False
    client.expire(key, extra_ttl_seconds)  # => resets the TTL countdown -- the "keep me logged in" pattern
    return True


def delete_session(client: redis.Redis, session_id: str) -> None:
    """DELETE: an explicit logout -- removes the session immediately, without waiting on its TTL."""
    client.delete(_session_key(session_id))


def main() -> None:
    """Run a full CRUD + TTL round trip and print a CLI-verifiable report."""
    client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)  # => decode_responses=True: values come back as str, not bytes
    client.delete(_session_key("sess-cap-1"))  # => resets state -- this script is fully self-contained

    create_session(client, "sess-cap-1", "user-42", ttl_seconds=60)  # => CREATE
    created = get_session(client, "sess-cap-1")  # => READ, right after creation
    assert created is not None and created["user_id"] == "user-42"
    print(f"CREATE + READ:  {created}")

    touched = touch_session(client, "sess-cap-1", extra_ttl_seconds=120)  # => UPDATE: extends the TTL
    assert touched is True
    print(f"UPDATE (touch): extended={touched}")

    delete_session(client, "sess-cap-1")  # => DELETE: an explicit logout
    deleted = get_session(client, "sess-cap-1")  # => READ after DELETE -- must be gone immediately
    assert deleted is None
    print(f"DELETE + READ:  {deleted}")

    create_session(client, "sess-cap-2", "user-99", ttl_seconds=3)  # => a SECOND session, short TTL
    time.sleep(4)  # => waits PAST the 3-second TTL -- a genuine elapsed expiry, not a mocked clock
    expired = get_session(client, "sess-cap-2")
    assert expired is None
    print(f"TTL expiry:     {expired} (after the 3-second TTL elapsed on its own)")

    print("kv.py: full CREATE/READ/UPDATE/DELETE + TTL-expiry round trip PASSED")
    client.close()


if __name__ == "__main__":
    main()
