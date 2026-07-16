# learning/code/ex-21-gitignore-and-env-example/gitignore_demo.py
"""Example 21: .gitignore and .env.example."""  # => co-17: module docstring

from __future__ import (
    annotations,
)  # => co-17: DD-39 hygiene, unrelated to the git sandbox itself

import subprocess  # => co-17: drives real `git` commands against a throwaway sandbox repo
import tempfile  # => co-17: the sandbox repo lives in a temp dir -- self-contained, cleaned up on exit
from pathlib import (
    Path,
)  # => co-17: typed, ergonomic file writes for the sandbox's own files


def run_git(
    args: list[str], cwd: Path
) -> str:  # => co-17: a small wrapper -- every git call in this example goes through it
    """Run a git subcommand in cwd and return its captured stdout."""  # => co-17: doc
    result = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=True
    )  # => co-17: shell=False, argv list
    return result.stdout  # => co-17: the real, captured stdout -- never fabricated


if (
    __name__ == "__main__"
):  # => co-17: entry point -- init a REAL repo, seed 3 files, then inspect git status
    with (
        tempfile.TemporaryDirectory() as tmp
    ):  # => co-17: throwaway sandbox, cleaned up automatically on exit
        repo = Path(
            tmp
        )  # => co-17: the temp dir this whole example's git repo lives in
        print(
            f"=== git init (throwaway sandbox at {repo.name}) ==="
        )  # => co-17: names the sandbox, not the real repo
        print(
            run_git(["init", "-q"], cwd=repo).strip()
            or "(no output -- git init -q is quiet)"
        )  # => co-17: real init

        (repo / ".gitignore").write_text(
            ".env\n__pycache__/\n*.pyc\n"
        )  # => co-17: .env is the ONE line that matters here
        (repo / ".env.example").write_text(
            "API_KEY=replace-with-your-own-key\nDB_PASSWORD=replace-me\n"
        )  # => co-17: placeholders ONLY
        (repo / ".env").write_text(
            "API_KEY=sk-live-51HxT9mQ2vL7pRz3nK8wY0aB\nDB_PASSWORD=Summer2026!\n"
        )  # => co-17: the REAL secret file

        print(
            "\n=== git status --porcelain (real output) ==="
        )  # => co-17: the actual verification this example proves
        status = run_git(
            ["status", "--porcelain"], cwd=repo
        )  # => co-17: a real, captured git status, not a fabricated one
        print(
            status.rstrip() or "(empty)"
        )  # => co-17: prints exactly what git reports, nothing more

        env_example_listed = (
            ".env.example" in status
        )  # => co-17: confirms the placeholder-only file IS tracked-as-new
        real_env_listed = any(  # => co-17: checks EACH status line individually -- avoids the ".env" substring trap
            line.strip().endswith(".env")
            for line in status.splitlines()  # => co-17: an exact filename match, not substring
        )  # => co-17: end of the per-line check
        print(
            f"\n.env.example appears in git status: {env_example_listed}"
        )  # => co-17: True -- untracked, ready to commit
        print(
            f".env (exact filename) appears in git status: {real_env_listed}"
        )  # => co-17: False -- .gitignore hides it
