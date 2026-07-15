# learning/code/ex-76-sbom-and-provenance/generate_sbom.py
"""Example 76: a real CycloneDX SBOM from requirements.txt, cross-checked against a real pip-audit run (co-21)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the SBOM/audit logic itself

import json  # => co-21: parses the REAL SBOM JSON cyclonedx-py actually generates
import subprocess  # => co-21: every cyclonedx-py/venv/pip/pip-audit invocation below is a REAL subprocess call
import sys  # => co-21: sys.executable -- runs `-m venv`/`-m pip` through the SAME interpreter this script uses
import tempfile  # => co-21: a genuinely fresh, throwaway install target for the real pip-audit cross-check
from pathlib import (
    Path,
)  # => co-21: real filesystem paths for the requirements file and generated SBOM

HERE = Path(__file__).parent  # => co-21: this example's own real directory
REQUIREMENTS_FILE = (
    HERE / "requirements.txt"
)  # => co-21: the REAL, pinned file this example generates an SBOM from
SBOM_OUTPUT = (
    HERE / "sbom.json"
)  # => co-21: the REAL, on-disk CycloneDX document this run actually writes


def run(
    args: list[str],
) -> subprocess.CompletedProcess[str]:  # => co-21: a shared, REAL subprocess runner
    return subprocess.run(
        args, capture_output=True, text=True
    )  # => co-21: check=False -- callers inspect returncode


def main() -> (
    None
):  # => co-21: generates a real SBOM, cross-checks it, then confirms a real clean pip-audit run
    print(
        f"requirements.txt:\n{REQUIREMENTS_FILE.read_text().strip()}\n"
    )  # => co-21: the real, pinned input file

    print(
        "=== generating a real CycloneDX SBOM via `cyclonedx-py requirements` ==="
    )  # => labels section
    # => co-21: `cyclonedx-py --help` (checked live before authoring this example) confirms the installed
    # => cyclonedx-bom 7.3.0 CLI supports BOTH `requirements` and `environment` sub-commands -- this example
    # => uses `requirements` since it targets a specific, pinned file rather than the whole active venv
    gen = run(
        [
            "cyclonedx-py",
            "requirements",
            str(REQUIREMENTS_FILE),
            "-o",
            str(SBOM_OUTPUT),
            "--of",
            "JSON",
        ]
    )
    assert gen.returncode == 0, (
        gen.stderr
    )  # => co-21: proves the REAL SBOM generation command actually succeeded
    sbom = json.loads(
        SBOM_OUTPUT.read_text()
    )  # => co-21: the REAL, generated CycloneDX document, parsed from disk
    print(
        f"bomFormat={sbom['bomFormat']} specVersion={sbom['specVersion']}"
    )  # => co-21: real, top-level SBOM metadata
    sbom_names = {
        component["name"] for component in sbom["components"]
    }  # => co-21: every REAL component name listed
    print(
        f"components in SBOM: {sorted(sbom_names)}"
    )  # => co-21: the real, generated component list

    print(
        "\n=== cross-checking every requirements.txt package appears in the SBOM ==="
    )  # => labels section
    declared_names = {  # => co-21: every REAL package name this project's requirements.txt actually declares
        line.split("==")[0].strip()
        for line in REQUIREMENTS_FILE.read_text().splitlines()
        if line.strip() and not line.strip().startswith("#")
    }
    print(
        f"declared in requirements.txt: {sorted(declared_names)}"
    )  # => co-21: real, parsed declared names
    for (
        name
    ) in declared_names:  # => co-21: every REAL declared package, checked individually
        assert name in sbom_names, (
            f"{name} declared but missing from the generated SBOM"
        )  # => co-21: real, per-package
    print(
        "verified: every declared package appears in the real, generated SBOM"
    )  # => co-21: real conclusion

    print(
        "\n=== real pip-audit cross-check against a clean install of the SAME requirements.txt ==="
    )  # => labels
    venv_dir = Path(
        tempfile.mkdtemp(prefix="ex76-venv-")
    )  # => co-21: a REAL, fresh, throwaway venv for this audit
    run(
        [sys.executable, "-m", "venv", str(venv_dir)]
    )  # => co-21: real venv creation, CLI form (see ex-55's honest note)
    venv_python = (
        venv_dir / "bin" / "python3"
    )  # => co-21: the real interpreter living inside this fresh venv
    run(
        [str(venv_python), "-m", "pip", "install", "--quiet", "--upgrade", "pip"]
    )  # => co-21: a real, current pip first
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
    site_packages = (
        next((venv_dir / "lib").glob("python3.*")) / "site-packages"
    )  # => co-21: the REAL, on-disk install dir
    audit = run(
        ["pip-audit", "--path", str(site_packages)]
    )  # => co-21: a REAL pip-audit CLI call, real advisory data
    audit_output = (
        audit.stdout + audit.stderr
    )  # => co-21: pip-audit writes its clean-result line to stderr (see ex-55)
    print(
        audit_output.strip()
    )  # => co-21: the REAL audit result -- straight from pip-audit's own output
    assert (
        "No known vulnerabilities found" in audit_output
    )  # => co-21: proves the SAME package set is CVE-clean too


if (
    __name__ == "__main__"
):  # => co-21: only runs when launched directly, e.g. `python3 generate_sbom.py`
    main()  # => co-21: generates a real SBOM, cross-checks its component list, then confirms a real clean audit
