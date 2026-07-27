"""Example 26: License Check: MongoDB."""  # => co-28: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

# co-28, deliberate exception: same as Example 25 -- this is a live network check against MongoDB's
# own repository, not the local Docker service every other example in this course talks to. A license
# check is inherently about reading an EXTERNAL, authoritative source at the time it is run.
import urllib.error  # => co-28: distinguishes "network unreachable" from "citation actually wrong"
import urllib.request  # => co-28: stdlib only -- no new pinned dependency added for one network call

from dataclasses import dataclass  # => co-28: a typed, citable record -- store, source, and expected text


@dataclass(frozen=True)  # => frozen -- a license citation is a stated, verifiable claim, not something mutated
class LicenseCheck:  # => co-28: one store's license claim, paired with WHERE to verify it and WHAT to expect
    store: str  # => which store this check is about
    license_url: str  # => vendor's OWN raw license file -- more stable than scraping a marketing legal page
    expected_identifier: str  # => the exact substring that must appear if the citation above is still current


CHECKS = [  # => co-28: exactly 1 check -- MongoDB's Server Side Public License v1
    LicenseCheck(  # => MongoDB's own repository license file, pinned to the current v8.2 release branch
        store="MongoDB",  # => the store this check verifies
        license_url="https://raw.githubusercontent.com/mongodb/mongo/v8.2/LICENSE-Community.txt",  # => vendor's own file
        expected_identifier="Server Side Public License",  # => SSPLv1's full name, the citation's central claim
    ),  # => closes the one check
]  # => closes CHECKS -- exactly 1 entry, matching this example's single-store scope


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
    results = [verify_license(check) for check in CHECKS]  # => co-28: runs the check, collects pass/fail/skip
    confirmed = sum(1 for r in results if r)  # => co-28: counts genuinely CONFIRMED checks (a SKIP counts as False)
    print(f"{confirmed}/{len(CHECKS)} license citation confirmed against the vendor's own repository")  # => Output


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
