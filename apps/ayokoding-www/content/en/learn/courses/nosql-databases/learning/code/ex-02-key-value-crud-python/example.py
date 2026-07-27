"""Example 2: Key-Value CRUD in Python."""  # => co-20: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import redis  # => co-20: redis-py, the official typed Python client for Valkey/Redis


def crud_roundtrip(client: redis.Redis) -> None:  # => performs and verifies one full create/read/update/delete cycle
    """Set, read, overwrite, delete, and confirm-gone on one key."""  # => documents the contract, no runtime output
    client.set("user:1:name", "Ada")  # => co-20: SET creates user:1:name with value "Ada"
    assert client.get("user:1:name") == b"Ada"  # => co-20: GET returns bytes by default, not str
    # => the b"..." prefix is not a typo -- redis-py's default decode_responses=False
    client.set("user:1:name", "Ada Lovelace")  # => co-20: SET on an existing key overwrites it in place
    assert client.get("user:1:name") == b"Ada Lovelace"  # => confirms the overwrite actually took
    deleted_count = client.delete("user:1:name")  # => co-20: DELETE returns the count of keys it removed
    assert deleted_count == 1  # => exactly one key existed under this name and was removed
    assert client.get("user:1:name") is None  # => co-20: GET on a missing key returns None, never raises
    # => this is the same nil the CLI showed in Example 1, surfaced as Python None


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = redis.Redis(host="localhost", port=6379, db=0)  # => connects to a local Valkey/Redis instance
    crud_roundtrip(client)  # => runs the full verified round trip above
    print("CRUD round trip verified: set, get, overwrite, delete, confirm-gone")  # => Output: CRUD round trip verified: set, get, overwrite, delete, confirm-gone
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
