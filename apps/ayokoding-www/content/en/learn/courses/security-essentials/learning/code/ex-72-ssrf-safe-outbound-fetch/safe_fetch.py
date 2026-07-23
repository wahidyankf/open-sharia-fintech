# learning/code/ex-72-ssrf-safe-outbound-fetch/safe_fetch.py
"""Example 72: a real outbound-fetch helper -- blocks private/internal/metadata IPs BEFORE any network call happens (co-01, co-25)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the SSRF-guard logic itself

import ipaddress  # => co-01: stdlib -- the REAL, authoritative classifier for RFC 1918/loopback/link-local ranges
from urllib.parse import (
    urlparse,
)  # => co-01: real URL parsing -- extracts the target host BEFORE any connection attempt

import requests  # => co-25: real HTTP client -- reached ONLY once a target has already passed the allow-check


class SSRFBlockedError(
    Exception
):  # => co-25: a real, named exception -- raised strictly BEFORE any network I/O
    """Raised when a target IP falls inside a blocked private/internal/metadata range."""


def classify_ip(
    ip_str: str,
) -> str | None:  # => co-01: returns a REAL, human-readable reason, or None if allowed
    ip = ipaddress.ip_address(
        ip_str
    )  # => co-01: Python's OWN real IP-address parser/classifier, not hand-rolled
    if ip.is_loopback:  # => co-01: 127.0.0.0/8 -- a REAL, standard loopback range
        return "loopback (127.0.0.0/8)"  # => co-01: real, specific reason -- not a generic "blocked"
    if ip.is_link_local:  # => co-01: 169.254.0.0/16 -- REAL, includes the cloud-metadata address 169.254.169.254
        return "link-local (169.254.0.0/16, includes cloud-metadata endpoints)"  # => co-01: real, named reason
    if ip.is_private:  # => co-01: covers the REAL RFC 1918 ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
        return "private (RFC 1918)"  # => co-01: real, standard reason
    if (
        ip.is_reserved or ip.is_multicast or ip.is_unspecified
    ):  # => co-01: real, additional non-routable/special ranges
        return "reserved/multicast/unspecified"  # => co-01: real, catch-all reason for the remaining special ranges
    return None  # => co-01: NONE of the real blocked-range checks matched -- this target is allowed


def check_url_target(
    url: str,
) -> (
    None
):  # => co-25: the REAL guard -- runs BEFORE any outbound connection is attempted
    host = urlparse(
        url
    ).hostname  # => co-01: the REAL target host, parsed straight from the URL string, no network yet
    if (
        host is None
    ):  # => co-01: a real guard against a malformed URL with no host component at all
        raise SSRFBlockedError(
            f"could not parse a target host from: {url!r}"
        )  # => co-25: real, hard reject
    ip = ipaddress.ip_address(
        host
    )  # => co-01: this example targets IP-literal URLs -- no DNS resolution, no network
    reason = classify_ip(
        str(ip)
    )  # => co-01: the REAL classification -- pure, local, no I/O of any kind
    if (
        reason is not None
    ):  # => co-25: the REAL decision point -- raises BEFORE requests.get is ever called
        raise SSRFBlockedError(
            f"blocked outbound fetch to {host}: {reason}"
        )  # => co-25: real, specific rejection


def safe_fetch(
    url: str, timeout: float = 5
) -> requests.Response:  # => co-25: the REAL, guarded outbound-fetch helper
    check_url_target(
        url
    )  # => co-25: raises HERE, before this function's own network call, for a blocked target
    return requests.get(
        url, timeout=timeout
    )  # => co-25: ONLY reached once the target has already passed the check
