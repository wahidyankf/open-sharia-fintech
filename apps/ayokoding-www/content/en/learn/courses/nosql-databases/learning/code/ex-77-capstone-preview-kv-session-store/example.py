"""Example 77: Capstone Preview - KV Session Store."""  # => co-20,co-24,co-21: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import time  # => co-24: a real sleep past the TTL window -- the same discipline Examples 7-8 established

import redis  # => co-20: redis-py, the official typed Python client -- the capstone's own kv.py will build on exactly this


def create_session(client: redis.Redis, session_id: str, user_id: str, ttl_seconds: int) -> None:  # => co-20,co-24: the capstone's core session-store primitive
    """Create a session as a Redis hash, with a TTL-based expiry -- the capstone's kv.py shape, previewed."""  # => documents the contract
    key = f"session:{session_id}"  # => co-20: a namespaced key -- the capstone will follow this same "type:id" convention
    client.hset(key, mapping={"user_id": user_id, "created_at": str(int(time.time()))})  # => co-20: a hash, not a plain string -- room for more session fields
    client.expire(key, ttl_seconds)  # => co-24: the session self-expires -- no scheduled cleanup job required


def get_session(client: redis.Redis, session_id: str) -> dict[str, str] | None:  # => co-20: reads a session back, or None if expired/never existed
    """Read a session hash back, returning None if it has expired or never existed."""  # => documents the contract
    key = f"session:{session_id}"  # => the SAME namespaced key create_session used
    data = client.hgetall(key)  # => co-20: HGETALL -- an empty dict means the key does not exist (expired or never created)
    if not data:  # => co-20: Redis returns an EMPTY hash for a missing key, not an error -- this IS the "not found" signal
        return None  # => co-24: correctly reports "gone" for an expired or never-existent session

    def as_str(raw: str | bytes) -> str:  # => co-20: redis-py's own return type is a union -- decode ONLY if the driver returned raw bytes
        return raw.decode() if isinstance(raw, bytes) else raw  # => the same isinstance-narrowing discipline the capstone's own kv.py must use

    return {as_str(k): as_str(v) for k, v in data.items()}  # => co-20: decodes the raw bytes redis-py returns by default


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = redis.Redis(host="localhost", port=6379, db=0)  # => connects to a local Valkey/Redis instance
    client.delete("session:sess-1")  # => resets state -- this example is fully self-contained

    create_session(client, "sess-1", "user-42", ttl_seconds=3)  # => co-20,co-24: a session with a SHORT TTL, for a fast round trip
    active_session = get_session(client, "sess-1")  # => reads it back immediately
    assert active_session is not None and active_session["user_id"] == "user-42"  # => co-20: the session round-tripped correctly, right after creation
    print(f"Immediately after creation: {active_session}")  # => Output line -- includes a created_at timestamp, machine-dependent

    time.sleep(4)  # => co-24: waits PAST the 3-second TTL -- a genuine elapsed expiry
    expired_session = get_session(client, "sess-1")  # => reads AGAIN, after the TTL elapsed
    assert expired_session is None  # => co-24: the session auto-expired, exactly as co-21's "TTL-based cache" pattern promises
    print(f"After the 3-second TTL elapses: {expired_session}")  # => Output: After the 3-second TTL elapses: None
    print("This session round-trip and auto-expire is EXACTLY the shape the capstone's kv.py will build on")  # => Output line
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
