#!/usr/bin/env bash
# Resolver shim for the rhino-cli binary — invoked by every generated gate
# command instead of `cargo run --release --quiet --manifest-path
# apps/rhino-cli/Cargo.toml -- <command>` so gate invocations skip cargo's
# per-run overhead once a binary is already available.
#
# Namespace routing (rewrite-rhino-cli-to-fsharp, Phase 2 onward): before any
# Rust resolution runs, the first argument is checked against
# FSHARP_NAMESPACES. A namespace listed there resolves against the F# binary
# instead, through its own three tiers below. FSHARP_NAMESPACES ships empty
# here and gains one namespace per wave's flip PR — reverting a wave is a
# one-line removal from this array. See
# plans/in-progress/rewrite-rhino-cli-to-fsharp/tech-docs.md
# §Dispatch shim during migration.
#
# Rust resolution order (unchanged, still the default for every
# not-yet-flipped namespace):
#   1. RHINO_CLI_BIN env var — if set and points to an executable file, use
#      it directly (no build, no discovery). Lets CI/local callers pin an
#      already-built binary explicitly.
#   2. <target-dir>/gate/rhino-cli — the `--profile gate` build output — if it
#      exists and is newer than every file under apps/rhino-cli/src/ and its
#      Cargo.toml/Cargo.lock, use it directly (no rebuild). <target-dir> is
#      CARGO_TARGET_DIR if that env var is set (matching plain `cargo build`'s
#      own precedence), otherwise apps/rhino-cli/target.
#   3. Otherwise, build it with `cargo build --profile gate` and then use
#      the resulting binary. `cargo build` honors CARGO_TARGET_DIR itself, so
#      no extra flag is needed here to keep step 2 and step 3 in sync.
#
# This targets `--profile gate`/`target/gate/` — a fast-compiling profile
# (no LTO, higher codegen-unit parallelism, lower opt-level) that inherits
# from `[profile.release]` in Cargo.toml, trading a little runtime speed for
# much faster local rebuilds. The `build` Nx target and CI release artifacts
# still use `--release`/`target/release/`, unchanged; see
# plans/done/2026-08-09__optimize-cis/delivery.md.
#
# F# resolution order (mirrors the Rust tiers above), used only for a
# namespace listed in FSHARP_NAMESPACES:
#   1. RHINO_CLI_FSHARP_BIN env var — explicit override, same contract as
#      RHINO_CLI_BIN.
#   2. apps/rhino-cli/src-fsharp/dist/rhino-cli-fsharp — the published
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
MANIFEST="${REPO_ROOT}/apps/rhino-cli/Cargo.toml"
SRC_DIR="${REPO_ROOT}/apps/rhino-cli/src"
LOCKFILE="${REPO_ROOT}/apps/rhino-cli/Cargo.lock"
TARGET_DIR="${CARGO_TARGET_DIR:-${REPO_ROOT}/apps/rhino-cli/target}"
GATE_BIN="${TARGET_DIR}/gate/rhino-cli"

# Namespaces already flipped to the F# binary. Empty at Phase 2 — every wave
# from Wave A (Phase 3) onward adds exactly its own namespaces here in that
# wave's flip PR, per tech-docs.md DD-4's wave ordering.
FSHARP_NAMESPACES=("convention" "parity" "repo-config" "env" "doctor" "test-coverage" "md" "governance" "git" "harness" "specs" "repo-governance" "gate")

if [[ $# -gt 0 ]]; then
	for FSHARP_NAMESPACE in "${FSHARP_NAMESPACES[@]+"${FSHARP_NAMESPACES[@]}"}"; do
		if [[ "${FSHARP_NAMESPACE}" == "$1" ]]; then
			FSHARP_DIST_BIN="${REPO_ROOT}/apps/rhino-cli/src-fsharp/dist/rhino-cli-fsharp"
			FSHARP_PROJECT="${REPO_ROOT}/apps/rhino-cli/src-fsharp/RhinoCli.Program/RhinoCli.Program.fsproj"
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
		fi
	done
fi

# Resolve which Rust binary to run, trying each tier in order, then execute
# it once at the bottom — the single `exec` call keeps argument passthrough
# ("$@") and exit-code propagation defined in exactly one place.
if [[ -n "${RHINO_CLI_BIN:-}" && -f "${RHINO_CLI_BIN}" && -x "${RHINO_CLI_BIN}" ]]; then
	# Tier 1: explicit override via RHINO_CLI_BIN.
	RESOLVED_BIN="${RHINO_CLI_BIN}"
elif [[ -x "${GATE_BIN}" ]] && [[ -z "$(find "${SRC_DIR}" "${MANIFEST}" "${LOCKFILE}" -type f -newer "${GATE_BIN}" -print -quit)" ]]; then
	# Tier 2: reuse the prebuilt `--profile gate` binary if it is at least as
	# fresh as every source file, Cargo.toml, and Cargo.lock (i.e. nothing
	# that affects the build is newer than it).
	RESOLVED_BIN="${GATE_BIN}"
else
	# Tier 3: (re)build the gate-profile binary, then use it.
	cargo build --profile gate --manifest-path "${MANIFEST}" --quiet
	RESOLVED_BIN="${GATE_BIN}"
fi

exec "${RESOLVED_BIN}" "$@"
