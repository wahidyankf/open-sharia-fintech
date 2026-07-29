# pyright: strict
"""Kata 3 (before): comparing a weak ETag against a stored strong ETag never matches."""

STORED_ETAG = '"abc123"'  # the server's own strong validator for the current representation


def check_not_modified(if_none_match: str) -> int:
    # THE BUG: a weak validator ("W/" prefix) is semantically equivalent for a
    # GET's freshness check, but this direct string comparison treats the
    # "W/" prefix as making the values genuinely different.
    if if_none_match == STORED_ETAG:
        return 304
    return 200


weak_client_etag = 'W/"abc123"'  # the SAME representation, tagged weak by an intermediary
status = check_not_modified(weak_client_etag)
print(f"status for weak ETag of the SAME representation: {status}")  # BUG: 200, should be 304
