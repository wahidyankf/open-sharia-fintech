# learning/code/ex-07-path-traversal-file-read/download_file.py
"""Example 7: Path Traversal -- File Read."""  # => co-05: module docstring

from __future__ import (
    annotations,
)  # => co-05: DD-39 hygiene, unrelated to the exploit itself

import os  # => co-05: os.path.join/realpath below are the whole mechanism this example turns on
import tempfile  # => co-05: builds a throwaway sandbox directory, self-contained per-run
from pathlib import Path  # => co-05: typed, ergonomic file writes for the sandbox setup


def build_sandbox(
    root: Path,
) -> tuple[
    Path, Path
]:  # => co-05: returns (public download dir, secret file OUTSIDE it)
    """Create a downloads/ dir with a public file, plus a secret file one level ABOVE it."""  # => co-05: doc
    downloads = (
        root / "downloads"
    )  # => co-05: the intended, sandboxed root every download SHOULD stay inside
    downloads.mkdir()  # => co-05: creates the public-facing directory
    (downloads / "report.txt").write_text(
        "Q3 sales report -- public\n"
    )  # => co-05: a legitimate, in-bounds file
    secret = (
        root / "secret_config.txt"
    )  # => co-01: lives OUTSIDE downloads/ -- never meant to be served
    secret.write_text(
        "DB_PASSWORD=super-secret-value\n"
    )  # => co-01: the out-of-root file this exploit targets
    return (
        downloads,
        secret,
    )  # => co-05: (sandboxed dir, off-limits file) -- used by both handlers below


def naive_download(
    base_dir: Path, filename: str
) -> str:  # => co-05: the vulnerable handler -- filename is tainted
    """Read a file under base_dir by naive path joining -- VULNERABLE, do not copy."""  # => co-05: doc
    path = os.path.join(
        base_dir, filename
    )  # => co-01: '../' sequences in filename are NOT stripped here
    print(
        f"OPENING: {path}"
    )  # => co-05: prints the ACTUAL path opened -- shows the traversal landing outside base_dir
    return Path(
        path
    ).read_text()  # => co-05: reads WHATEVER path results, in or out of base_dir


def safe_download(
    base_dir: Path, filename: str
) -> str:  # => co-05: the FIXED handler -- same tainted filename
    """Read a file under base_dir, canonicalizing and enforcing a root prefix -- FIXED."""  # => co-05: doc
    candidate = os.path.realpath(
        os.path.join(base_dir, filename)
    )  # => co-05: resolves ALL '..' and symlinks first
    allowed_root = os.path.realpath(
        base_dir
    )  # => co-05: the canonical form of the ONE directory downloads may serve
    print(
        f"CANDIDATE: {candidate}"
    )  # => co-05: prints the fully-resolved path -- shows where '..' actually points
    if not candidate.startswith(
        allowed_root + os.sep
    ):  # => co-05: prefix check AFTER resolution, not before
        raise PermissionError(
            f"{filename!r} resolves outside the allowed root"
        )  # => co-05: rejects the escape
    return (
        Path(candidate).read_text()
    )  # => co-05: only reached if candidate is genuinely inside allowed_root


if (
    __name__ == "__main__"
):  # => co-05: entry point -- legit read, traversal exploit, then the fix
    with (
        tempfile.TemporaryDirectory() as tmp
    ):  # => co-05: throwaway sandbox, cleaned up automatically on exit
        root = Path(
            tmp
        )  # => co-05: the temp dir standing in for a real app's storage root
        downloads, secret = build_sandbox(
            root
        )  # => co-05: sets up downloads/report.txt and ../secret_config.txt

        print(
            "=== VULNERABLE: legitimate download ==="
        )  # => co-05: sanity check -- the naive handler works normally
        print(
            naive_download(downloads, "report.txt")
        )  # => co-05: reads the intended, in-bounds file

        print("=== VULNERABLE: path-traversal exploit ===")  # => co-05: the attack
        payload = "../secret_config.txt"  # => co-01: '..' walks UP one level, straight to the secret file
        leaked = naive_download(
            downloads, payload
        )  # => co-05: the out-of-root read this example proves
        print(
            f"LEAKED CONTENT: {leaked!r}"
        )  # => co-05: the secret file's contents, read successfully

        print(
            "=== FIXED: same payload against realpath + prefix check ==="
        )  # => co-05: re-run against the fix
        try:  # => co-05: safe_download raises instead of returning attacker-reachable content
            safe_download(
                downloads, payload
            )  # => co-01: the SAME payload string, now rejected
        except PermissionError as exc:  # => co-05: the exact exception the fix raises for an out-of-root path
            print(
                f"BLOCKED: {exc}"
            )  # => co-05: proves the traversal is refused, no content is ever read
