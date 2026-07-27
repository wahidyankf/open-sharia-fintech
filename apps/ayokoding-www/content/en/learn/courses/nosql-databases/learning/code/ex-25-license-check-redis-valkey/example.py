"""Example 25: License Check: Redis vs. Valkey."""  # => co-28: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

# co-28, deliberate exception: this is the ONLY example in this course that opens a live network
# socket. Every other example in this course runs against a LOCAL Docker service; a license check is
# inherently about reading an EXTERNAL, authoritative source, so a live fetch is the honest way to
# "verify the citation matches the official page" rather than embedding a frozen, unverifiable string.
import urllib.error  # => co-28: distinguishes "network unreachable" from "citation actually wrong"
import urllib.request  # => co-28: stdlib only -- no new pinned dependency added for one network call

from dataclasses import dataclass  # => co-28: a typed, citable record -- store, source, and expected text


@dataclass(frozen=True)  # => frozen -- a license citation is a stated, verifiable claim, not something mutated
class LicenseCheck:  # => co-28: one store's license claim, paired with WHERE to verify it and WHAT to expect
    store: str  # => which store this check is about
    license_url: str  # => vendor's OWN raw license file -- more stable than scraping a marketing legal page
    expected_identifier: str  # => the exact substring that must appear if the citation above is still current


CHECKS = [  # => co-28: exactly 2 checks -- Redis (tri-licensed) and Valkey, its permissive BSD-3-Clause fork
    LicenseCheck(  # => check 1 -- Redis's own repository LICENSE.txt, pinned to the Redis 8 release branch
        store="Redis",  # => the store this check verifies
        license_url="https://raw.githubusercontent.com/redis/redis/8.0/LICENSE.txt",  # => vendor's own file
        expected_identifier="AGPLv3",  # => Redis 8's re-added OSI-approved tri-license option, the citation's claim
    ),  # => closes check 1
    LicenseCheck(  # => check 2 -- Valkey's own repository COPYING file, pinned to the matching 8.0 branch
        store="Valkey",  # => the Linux Foundation fork this check verifies
        license_url="https://raw.githubusercontent.com/valkey-io/valkey/8.0/COPYING",  # => vendor's own file
        expected_identifier="BSD 3-Clause License",  # => the permissive license the citation claims, verbatim
    ),  # => closes check 2
]  # => closes CHECKS -- exactly 2 entries, one per store this example set out to verify


def fetch_license_text(url: str) -> str:  # => co-28: the ONE function in this course that opens a socket
    """Fetch a vendor's raw license file text, timing out rather than hanging forever."""  # => documents contract
    with urllib.request.urlopen(url, timeout=10) as response:  # => co-28: 10s timeout -- fail fast, don't hang
        return response.read().decode("utf-8")  # => co-28: raw file bytes decoded to text for a substring check


def verify_license(check: LicenseCheck) -> bool:  # => co-28: fetches + asserts, returns whether the citation held
    """Fetch check.license_url and confirm check.expected_identifier appears in it."""  # => documents contract
    try:  # => co-28: a network failure is NOT the same thing as a wrong citation -- keep them distinct
        text = fetch_license_text(check.license_url)  # => co-28: the live fetch -- this IS the "verify" step
    except (urllib.error.URLError, TimeoutError) as exc:  # => co-28: "couldn't check" vs. "check failed"
        print(f"{check.store}: SKIPPED -- could not reach {check.license_url} ({exc})")  # => Output (network-dependent)
        return False  # => co-28: unverifiable right now is NOT the same as a confirmed license mismatch
    found = check.expected_identifier in text  # => co-28: the actual verification -- does the citation still hold?
    status = "CONFIRMED" if found else "MISMATCH"  # => co-28: names the outcome plainly, no ambiguity
    print(f"{check.store}: {status} -- '{check.expected_identifier}' found in {check.license_url}")  # => Output
    return found  # => co-28: caller decides what to do with a False (here: just tally it in main())


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    results = [verify_license(check) for check in CHECKS]  # => co-28: runs both checks, collects pass/fail/skip
    confirmed = sum(1 for r in results if r)  # => co-28: counts genuinely CONFIRMED checks (a SKIP counts as False)
    print(f"{confirmed}/{len(CHECKS)} license citations confirmed against the vendor's own repository")  # => Output


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
