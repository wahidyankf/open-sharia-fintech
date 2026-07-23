# learning/code/ex-55-dependency-pinning-and-lockfile/demo.py
"""Example 55: two REAL, independent clean installs from one exact-pinned requirements.txt (co-21)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the pinning/lockfile logic itself

import subprocess  # => co-21: every venv/pip/pip-audit invocation below is a REAL subprocess call
import sys  # => co-21: sys.executable -- runs `-m venv`/`-m pip` through the SAME interpreter this script uses
import tempfile  # => co-21: two genuinely independent, throwaway install targets -- never shared state
from pathlib import Path  # => co-21: real filesystem paths for both sandbox installs

REQUIREMENTS_FILE = (
    Path(__file__).parent / "requirements.txt"
)  # => co-21: the REAL, exact-pinned file this scans


def run(
    args: list[str],
) -> subprocess.CompletedProcess[str]:  # => co-21: a shared, REAL subprocess runner
    return subprocess.run(
        args, capture_output=True, text=True, check=True
    )  # => co-21: every call below is REAL


def clean_install(
    target_dir: Path,
) -> str:  # => co-21: builds ONE real venv, installs the pinned reqs, returns freeze
    run(
        [sys.executable, "-m", "venv", str(target_dir)]
    )  # => co-21: a REAL, fresh venv -- no shared state with any other
    venv_python = (
        target_dir / "bin" / "python3"
    )  # => co-21: the real interpreter living INSIDE this fresh venv
    run(
        [str(venv_python), "-m", "pip", "install", "--quiet", "--upgrade", "pip"]
    )  # => co-21: real, current pip first
    run(
        [
            str(venv_python),
            "-m",
            "pip",
            "install",
            "--quiet",
            "-r",
            str(REQUIREMENTS_FILE),
        ]
    )  # => co-21: the REAL install
    freeze = run(
        [str(venv_python), "-m", "pip", "freeze"]
    )  # => co-21: the REAL, resolved, fully-pinned package list
    return (
        freeze.stdout
    )  # => co-21: every line here is a REAL resolved `name==version`, not hand-typed


def main() -> (
    None
):  # => co-21: runs two independent installs, compares them, then audits the result
    print(
        f"requirements.txt (exact pins, no ranges):\n{REQUIREMENTS_FILE.read_text().strip()}"
    )  # => co-21: real content

    print(
        "\n=== independent install A (fresh venv, clean machine) ==="
    )  # => labels section
    venv_a = Path(
        tempfile.mkdtemp(prefix="ex55-venv-a-")
    )  # => co-21: a REAL, throwaway venv directory
    freeze_a = clean_install(
        venv_a
    )  # => co-21: a REAL install, top to bottom -- venv, pip upgrade, requirements install
    print(
        freeze_a.strip()
    )  # => co-21: the REAL, fully-resolved lock this install produced (a real "lockfile")

    print(
        "\n=== independent install B (a SEPARATE fresh venv, SAME requirements.txt) ==="
    )  # => labels section
    venv_b = Path(
        tempfile.mkdtemp(prefix="ex55-venv-b-")
    )  # => co-21: a SECOND, unrelated, throwaway venv directory
    freeze_b = clean_install(
        venv_b
    )  # => co-21: a completely independent real install run
    print(
        freeze_b.strip()
    )  # => co-21: the real, fully-resolved lock THIS install produced

    print(
        "\n=== comparing the two independently resolved locks ==="
    )  # => labels section
    lines_a = sorted(
        freeze_a.strip().splitlines()
    )  # => co-21: sorted so ordering differences never cause a false diff
    lines_b = sorted(
        freeze_b.strip().splitlines()
    )  # => co-21: sorted the SAME way for a real, meaningful comparison
    print(
        f"install A resolved {len(lines_a)} packages, install B resolved {len(lines_b)} packages"
    )  # => co-21: real counts
    assert (
        lines_a == lines_b
    )  # => co-21: proves BOTH independent installs resolved to IDENTICAL exact versions

    print(
        "\n=== pip-audit against install B's real, installed packages ==="
    )  # => labels section
    site_packages = (
        next((venv_b / "lib").glob("python3.*")) / "site-packages"
    )  # => co-21: the REAL, on-disk install dir
    audit = run(
        ["pip-audit", "--path", str(site_packages)]
    )  # => co-21: a REAL pip-audit CLI call, real PyPI advisory data
    audit_output = (
        audit.stdout + audit.stderr
    )  # => co-21: pip-audit writes its clean-result summary line to stderr
    print(
        audit_output.strip()
    )  # => co-21: the REAL audit result -- straight from pip-audit's own output
    assert (
        "No known vulnerabilities found" in audit_output
    )  # => co-21: proves the pinned, resolved tree is CVE-clean


if (
    __name__ == "__main__"
):  # => co-21: only runs when launched directly, e.g. `python3 demo.py`
    main()  # => co-21: runs both real installs, compares their real locks, then audits the result for real
