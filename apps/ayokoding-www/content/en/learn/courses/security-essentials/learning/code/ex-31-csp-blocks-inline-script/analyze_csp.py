"""Example 31: fetches the live app.py page, then applies CSP's OWN nonce rule (co-19, co-06). See this
example's Brief Explanation in the markdown for the full honest sandbox-limitation statement."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the CSP classification logic

import re  # => co-19: extracts the real nonce value straight out of the real response header

import requests  # => co-19: real HTTP client -- every request below hits the live app.py process

BASE_URL = (
    "http://127.0.0.1:5031"  # => co-19: matches app.py's app.run(port=5031) exactly
)


def fetch_page() -> tuple[
    str, str
]:  # => co-19: returns (csp_header_value, html_body) from a REAL request
    response = requests.get(
        f"{BASE_URL}/page", timeout=5
    )  # => co-19: a real HTTP GET against the live server
    csp_header = response.headers[
        "Content-Security-Policy"
    ]  # => co-19: the REAL header the server actually sent
    return (
        csp_header,
        response.text,
    )  # => co-19: both come from the SAME real HTTP response


def allowed_nonces(
    csp_header: str,
) -> set[str]:  # => co-19: parses script-src 'nonce-X' out of the real header
    return set(
        re.findall(r"'nonce-([^']+)'", csp_header)
    )  # => co-19: CSP's own documented nonce-source syntax
    # => co-19: a set, not a single value -- CSP allows multiple 'nonce-X' sources in one script-src list


def classify_scripts(
    csp_header: str, html_body: str
) -> list[tuple[str, bool]]:  # => co-19: (tag, would-run) pairs
    permitted = allowed_nonces(
        csp_header
    )  # => co-19: the ONE nonce value THIS response's policy actually allows
    results: list[
        tuple[str, bool]
    ] = []  # => co-19: accumulates each real <script ...> tag found in html_body
    for tag_match in re.finditer(
        r"<script[^>]*>", html_body
    ):  # => co-19: every real opening <script> tag, in order
        tag = tag_match.group(
            0
        )  # => co-19: the exact tag text, e.g. '<script nonce="abc123">'
        nonce_match = re.search(
            r'nonce="([^"]+)"', tag
        )  # => co-19: does THIS tag carry a nonce attribute at all?
        tag_nonce = (
            nonce_match.group(1) if nonce_match else None
        )  # => co-19: the tag's own nonce, or None if absent
        would_run = (
            tag_nonce in permitted
        )  # => co-19: CSP's rule -- exact match against the header's nonce, nothing else
        results.append(
            (tag, would_run)
        )  # => co-19: records the real classification for this real tag
    return results  # => co-19: one (tag, would_run) entry per real <script> tag the server actually sent


def main() -> (
    None
):  # => co-19: fetches once, then classifies every real script tag in that SAME response
    csp_header, html_body = (
        fetch_page()
    )  # => co-19: ONE real HTTP GET -- header and body from the same response
    print(
        f"Content-Security-Policy: {csp_header}"
    )  # => co-19: the real header value, straight off the wire
    classified = classify_scripts(
        csp_header, html_body
    )  # => co-19: applies the CSP nonce rule to each real tag
    for (
        tag,
        would_run,
    ) in classified:  # => co-19: iterates the real (tag, verdict) pairs just computed
        verdict = (
            "ALLOWED (nonce matches)" if would_run else "BLOCKED (no matching nonce)"
        )  # => co-19: per spec
        print(
            f"  {tag} -> {verdict}"
        )  # => co-19: real tag text next to its real, spec-derived verdict
    verdicts = [
        would_run for _, would_run in classified
    ]  # => co-19: extracts just the True/False verdicts
    assert verdicts == [
        True,
        False,
    ]  # => co-19: nonced script allowed, bare script blocked -- exactly one of each


if (
    __name__ == "__main__"
):  # => co-19: only runs when launched directly, e.g. `python3 analyze_csp.py`
    main()  # => co-19: fetches the live page once, then prints the real per-tag CSP verdicts
