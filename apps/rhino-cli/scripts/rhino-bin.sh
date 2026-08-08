#!/usr/bin/env bash
# Resolver shim for the rhino-cli binary — invoked by every generated gate
# command instead of `cargo run --release --quiet --manifest-path
# apps/rhino-cli/Cargo.toml -- <command>` so gate invocations skip cargo's
# per-run overhead once a binary is already available.
#
# Resolution order:
#   1. RHINO_CLI_BIN env var — if set and points to an executable file, use
#      it directly (no build, no discovery). Lets CI/local callers pin an
#      already-built binary explicitly.
#   2. <target-dir>/release/rhino-cli — the `--release` build output — if it
#      exists and is newer than every file under apps/rhino-cli/src/, use it
#      directly (no rebuild). <target-dir> is CARGO_TARGET_DIR if that env
#      var is set (matching plain `cargo build`'s own precedence), otherwise
#      apps/rhino-cli/target.
#   3. Otherwise, build it with `cargo build --release` and then use
#      the resulting binary. `cargo build` honors CARGO_TARGET_DIR itself, so
#      no extra flag is needed here to keep step 2 and step 3 in sync.
#
# NOTE: this targets `--release`/`target/release/` for now, not the faster
# `--profile gate`/`target/gate/` pair — `[profile.gate]` does not exist in
# Cargo.toml until a later phase adds it. That phase's own step repoints
# this script (and the `cargo build --release` call and `release/` path
# segment below) at the gate profile once it exists; see
# plans/in-progress/optimize-cis/delivery.md.
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
TARGET_DIR="${CARGO_TARGET_DIR:-${REPO_ROOT}/apps/rhino-cli/target}"
GATE_BIN="${TARGET_DIR}/release/rhino-cli"

# Resolve which binary to run, trying each tier in order, then execute it
# once at the bottom — the single `exec` call keeps argument passthrough
# ("$@") and exit-code propagation defined in exactly one place.
if [[ -n "${RHINO_CLI_BIN:-}" && -f "${RHINO_CLI_BIN}" && -x "${RHINO_CLI_BIN}" ]]; then
	# Tier 1: explicit override via RHINO_CLI_BIN.
	RESOLVED_BIN="${RHINO_CLI_BIN}"
elif [[ -x "${GATE_BIN}" ]] && [[ -z "$(find "${SRC_DIR}" -type f -newer "${GATE_BIN}" -print -quit)" ]]; then
	# Tier 2: reuse the prebuilt `--release` binary if it is at least as
	# fresh as every source file (i.e. nothing under src/ is newer than it).
	RESOLVED_BIN="${GATE_BIN}"
else
	# Tier 3: (re)build the release binary, then use it.
	cargo build --release --manifest-path "${MANIFEST}" --quiet
	RESOLVED_BIN="${GATE_BIN}"
fi

exec "${RESOLVED_BIN}" "$@"
