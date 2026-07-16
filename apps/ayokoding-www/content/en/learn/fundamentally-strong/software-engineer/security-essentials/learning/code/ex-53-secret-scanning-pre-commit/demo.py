# learning/code/ex-53-secret-scanning-pre-commit/demo.py
"""Example 53: a real throwaway git repo, a real detect-secrets scan, and a real pre-commit hook block (co-17, co-21)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the secret-scanning logic itself

import json  # => co-17: detect-secrets' own JSON output format -- parsed for real, not guessed at
import subprocess  # => co-17: every git/detect-secrets invocation below is a REAL subprocess call
import sys  # => co-17: sys.executable -- the exact interpreter this hook script must shell back out through
import tempfile  # => co-17: a genuinely throwaway sandbox directory -- never touches this repo's own git history
from pathlib import Path  # => co-17: real filesystem paths for the sandbox repo's files

# => co-17: AKIAIOSFODNN7EXAMPLE is AWS's OWN documented placeholder access key ID (matches the real
# => AKIA[0-9A-Z]{16} shape detect-secrets' AWSKeyDetector plugin looks for) -- never a live credential
FAKE_AWS_KEY_LINE = 'AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"\n'  # => co-17: the seeded, obviously-shaped secret

PRE_COMMIT_HOOK = f"""#!/usr/bin/env {sys.executable}
# Example 53's real pre-commit hook -- runs detect-secrets against every STAGED file (co-17, co-21)
import json
import subprocess
import sys

staged = subprocess.run(
    ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
    capture_output=True, text=True, check=True,
).stdout.split()
if not staged:
    sys.exit(0)
result = subprocess.run(
    ["detect-secrets", "scan", "--force-use-all-plugins", *staged],
    capture_output=True, text=True, check=True,
)
findings = json.loads(result.stdout)
if findings["results"]:
    print("COMMIT BLOCKED: detect-secrets found a likely secret:")
    for filename, hits in findings["results"].items():
        for hit in hits:
            print(f"  {{filename}}:{{hit['line_number']}} -- {{hit['type']}}")
    sys.exit(1)
sys.exit(0)
"""  # => co-17: a REAL executable script, written to .git/hooks/pre-commit below -- not a fabricated transcript


def run(
    args: list[str], cwd: Path, check: bool = True
) -> subprocess.CompletedProcess[str]:  # => co-17: shared runner
    return subprocess.run(
        args, cwd=cwd, capture_output=True, text=True, check=check
    )  # => co-17: every call REAL


def main() -> (
    None
):  # => co-17: builds a real sandbox git repo, scans it, wires the hook, then proves it blocks/allows
    sandbox = Path(
        tempfile.mkdtemp(prefix="ex53-secret-scan-")
    )  # => co-17: a REAL, isolated, throwaway directory
    print(
        f"sandbox repo: {sandbox}"
    )  # => co-17: real path, unique per run -- never collides with this project's git

    print("\n=== git init (real, throwaway repo) ===")  # => labels section
    run(
        ["git", "init", "-q"], cwd=sandbox
    )  # => co-17: a REAL git repository, isolated from this project's own history
    # => co-17: identity is intentionally NOT set here -- it inherits whatever author identity
    # => is already configured in the machine's own global ~/.gitconfig, exactly like any other local repo
    print(
        "initialized"
    )  # => co-17: real confirmation -- the sandbox repo now exists on disk

    print(
        "\n=== stage a file containing an obvious AWS-key-shaped secret ==="
    )  # => labels section
    config_file = (
        sandbox / "config.py"
    )  # => co-17: a real file this example's git repo will really track
    config_file.write_text(
        FAKE_AWS_KEY_LINE
    )  # => co-17: real bytes written to disk -- the seeded secret line
    run(
        ["git", "add", "config.py"], cwd=sandbox
    )  # => co-17: a REAL `git add` -- the file is now staged
    print(
        f"staged: {config_file.name}"
    )  # => co-17: real confirmation of what is now in the index

    print(
        "\n=== detect-secrets scan (real CLI call against the staged file) ==="
    )  # => labels section
    scan = run(
        ["detect-secrets", "scan", "--force-use-all-plugins", "config.py"], cwd=sandbox
    )  # => co-17: real CLI run
    findings = json.loads(
        scan.stdout
    )  # => co-17: real, parsed JSON output -- not a hand-written fixture
    for filename, hits in findings[
        "results"
    ].items():  # => co-17: every real finding detect-secrets actually reported
        for hit in hits:  # => co-17: one entry per real detected secret in this file
            print(
                f"  FOUND: {filename}:{hit['line_number']} -- {hit['type']}"
            )  # => co-17: real plugin name + line
    assert findings["results"], (
        "detect-secrets should have flagged the AWS-key-shaped line"
    )  # => co-17: proves it fired

    print(
        "\n=== wire the SAME check as a real pre-commit hook ==="
    )  # => labels section
    hooks_dir = (
        sandbox / ".git" / "hooks"
    )  # => co-17: git's real, standard hook directory for this sandbox repo
    hook_path = (
        hooks_dir / "pre-commit"
    )  # => co-17: the exact filename git invokes before every commit
    hook_path.write_text(
        PRE_COMMIT_HOOK
    )  # => co-17: real, executable Python source written to disk
    hook_path.chmod(
        0o755
    )  # => co-17: makes the hook script REALLY executable -- git will not run it otherwise
    print(
        f"installed: {hook_path}"
    )  # => co-17: real confirmation the hook file now exists and is executable

    print(
        "\n=== VULNERABLE moment: commit attempt WITH the secret still staged ==="
    )  # => labels section
    blocked = run(
        ["git", "commit", "-m", "add config"], cwd=sandbox, check=False
    )  # => co-17: a REAL commit attempt
    print(
        f"exit code: {blocked.returncode}"
    )  # => co-17: real process exit code -- 1 means the hook rejected the commit
    # => co-17: git relays a hook's own stdout through ITS stderr channel, not its stdout -- real git behavior
    print(
        blocked.stderr.strip()
    )  # => co-17: the REAL text the hook printed, straight from the subprocess
    assert (
        blocked.returncode != 0
    )  # => co-17: proves the commit really did NOT go through

    log_before = run(
        ["git", "log", "--oneline"], cwd=sandbox, check=False
    )  # => co-17: a real, empty log at this point
    print(
        f"git log after blocked attempt: {log_before.stdout.strip()!r}"
    )  # => co-17: real, empty string -- no commit exists

    print(
        "\n=== FIXED: remove the secret, re-stage, commit again ==="
    )  # => labels section
    config_file.write_text(
        "AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']  # loaded from env, not hardcoded\n"
    )
    run(
        ["git", "add", "config.py"], cwd=sandbox
    )  # => co-17: re-stages the NOW-secret-free version of the same file
    allowed = run(
        ["git", "commit", "-m", "add config"], cwd=sandbox, check=False
    )  # => co-17: the SAME commit command
    print(
        f"exit code: {allowed.returncode}"
    )  # => co-17: real exit code -- 0 means the hook let it through this time
    assert (
        allowed.returncode == 0
    )  # => co-17: proves the identical commit command now succeeds once the secret is gone

    log_after = run(
        ["git", "log", "--oneline"], cwd=sandbox, check=False
    )  # => co-17: a real, one-line log now
    print(
        f"git log after allowed commit: {log_after.stdout.strip()!r}"
    )  # => co-17: real commit hash + message, on disk


if (
    __name__ == "__main__"
):  # => co-17: only runs when launched directly, e.g. `python3 demo.py`
    main()  # => co-17: builds the sandbox, scans it, wires the hook, then proves BOTH the block and the allow
