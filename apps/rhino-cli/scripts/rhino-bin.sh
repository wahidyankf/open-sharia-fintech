#!/usr/bin/env bash
# Resolver shim for the rhino-cli binary — invoked by every generated gate
# command instead of `dotnet run --project apps/rhino-cli/src/RhinoCli.Program
# -- <command>` so gate invocations skip dotnet's per-run startup overhead
# once a binary is already available.
#
# Single resolution path (rewrite-rhino-cli-to-fsharp Phase 9c collapsed the
# former Rust/F# dual-tier dispatch to this, once the Rust crate was retired
# and every namespace ran on F#):
#   1. RHINO_CLI_FSHARP_BIN env var — if set and points to an executable
#      file, use it directly (no build, no discovery). Lets CI/local callers
#      pin an already-built binary explicitly.
#   2. apps/rhino-cli/src/dist/rhino-cli-fsharp — the published
#      self-contained binary (the `build` Nx target's output; also what CI's
#      `build-rhino` job uploads and every consumer job downloads).
#   3. Otherwise, `dotnet run` against RhinoCli.Program as a last resort —
#      needs the .NET SDK, unlike tiers 1-2, so CI always sets
#      RHINO_CLI_FSHARP_BIN instead of relying on this tier.
#
# In every case, all arguments are passed through unchanged and the script
# exits with the resolved binary's exit code (via `exec`, so no code is
# swallowed or remapped).
#
# Usage:   rhino-bin.sh <args-to-rhino-cli>
# Example: rhino-bin.sh md mermaid validate --exclude "apps/example/content"

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
FSHARP_DIST_BIN="${REPO_ROOT}/apps/rhino-cli/src/dist/rhino-cli-fsharp"
FSHARP_PROJECT="${REPO_ROOT}/apps/rhino-cli/src/RhinoCli.Program/RhinoCli.Program.fsproj"

if [[ -n "${RHINO_CLI_FSHARP_BIN:-}" && -f "${RHINO_CLI_FSHARP_BIN}" && -x "${RHINO_CLI_FSHARP_BIN}" ]]; then
	# Tier 1: explicit override via RHINO_CLI_FSHARP_BIN.
	exec "${RHINO_CLI_FSHARP_BIN}" "$@"
elif [[ -x "${FSHARP_DIST_BIN}" ]]; then
	# Tier 2: reuse the published self-contained binary.
	exec "${FSHARP_DIST_BIN}" "$@"
else
	# Tier 3: last resort, needs the .NET SDK.
	exec dotnet run --project "${FSHARP_PROJECT}" -- "$@"
fi
