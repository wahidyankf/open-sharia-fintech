# pyright: strict
"""Kata 3 (after): stripping the "W/" prefix before comparing restores weak validation."""

STORED_ETAG = '"abc123"'


def strip_weak_prefix(etag: str) -> str:
    # THE FIX: a weak validator's opaque tag is identical once "W/" is stripped --
    # weak comparison only needs the tag to match, not the full literal string.
    return etag[2:] if etag.startswith("W/") else etag


def check_not_modified(if_none_match: str) -> int:
    if strip_weak_prefix(if_none_match) == strip_weak_prefix(STORED_ETAG):
        return 304
    return 200


weak_client_etag = 'W/"abc123"'
status = check_not_modified(weak_client_etag)
print(f"status for weak ETag of the SAME representation: {status}")
