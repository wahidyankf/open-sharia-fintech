#!/usr/bin/env bash
# Differential runner proving byte-identity between the Rust and F# rhino-cli
# binaries for one or more namespaces, per
# plans/in-progress/rewrite-rhino-cli-to-fsharp/tech-docs.md §Byte-identity
# harness. Every wave's flip PR runs this against its own namespaces before
# the flip, and the Phase 2 Gate runs it with both sides pointed at the same
# Rust binary to prove the harness itself is sound before it is trusted.
#
# For each requested namespace, this script walks the CLI's own subcommand
# tree — discovered from clap's "requires a subcommand" error, not
# hand-maintained — down to every leaf command, then invokes each leaf
# through both binaries in its bare form, its `--help` form, and each of the
# three `-o`/`--output` formats (text, json, markdown), comparing stdout,
# stderr, and exit code every time. Leaf commands are invoked without their
# own positional/required arguments deliberately: at this phase the harness
# proves the two binaries agree on *dispatch and validation-error shape*,
# not on every fixture-backed success path — later waves' own scenario
# tests cover those.
#
# Usage:   shadow-diff.sh <namespace> [<namespace> ...]
# Example: shadow-diff.sh convention parity
#
# Binary resolution (override either independently):
#   SHADOW_DIFF_RUST_BIN   — defaults to apps/rhino-cli/target/gate/rhino-cli
#   SHADOW_DIFF_FSHARP_BIN — defaults to apps/rhino-cli/src/dist/rhino-cli-fsharp
#
# Exits 0 and prints "shadow-diff: N invocation(s) compared, 0 difference(s)"
# when every compared invocation matches; exits 1 and prints every mismatch
# otherwise.

set -euo pipefail

if [[ $# -lt 1 ]]; then
	echo "usage: shadow-diff.sh <namespace> [<namespace> ...]" >&2
	exit 2
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RUST_BIN="${SHADOW_DIFF_RUST_BIN:-${REPO_ROOT}/apps/rhino-cli/target/gate/rhino-cli}"
FSHARP_BIN="${SHADOW_DIFF_FSHARP_BIN:-${REPO_ROOT}/apps/rhino-cli/src/dist/rhino-cli-fsharp}"

if [[ ! -x "${RUST_BIN}" ]]; then
	echo "shadow-diff: Rust binary not found or not executable: ${RUST_BIN}" >&2
	echo "shadow-diff: build it first, e.g. cargo build --profile gate --manifest-path ${REPO_ROOT}/apps/rhino-cli/Cargo.toml" >&2
	exit 2
fi
if [[ ! -x "${FSHARP_BIN}" ]]; then
	echo "shadow-diff: F# binary not found or not executable: ${FSHARP_BIN}" >&2
	echo "shadow-diff: build it first, e.g. npx nx run rhino-cli:build" >&2
	exit 2
fi

COMPARED=0
DIFFERENCES=0

# Strips fields whose value is expected to vary between two otherwise-identical
# invocations — wall-clock timestamps and elapsed-time measurements — so
# `compare_invocation` proves dispatch/output-shape identity rather than
# accidental timing identity. Field shapes are pinned to the emitting Rust
# source, not guessed:
#   - `ran_at=...`      : repo_governance/audit_orchestrator.rs (text/markdown)
#   - `"ran_at": "..."` : same struct, JSON
#   - `"timestamp": "..."` and `**Generated**: ...` : doctor/reporter.rs
#   - `Duration: ...`, `- **Duration**: ...`, and `"duration_ms": N` : every
#     `harness` leaf (agents/reporter.rs)
# Edited in place; each stream is a private mktemp file already, so no backup
# file is left behind.
mask_volatile_fields() {
	local f="$1"
	sed -i.bak \
		-e 's/ran_at=[^,)"]*/ran_at=<MASKED>/g' \
		-e 's/"ran_at": *"[^"]*"/"ran_at": "<MASKED>"/g' \
		-e 's/"timestamp": *"[^"]*"/"timestamp": "<MASKED>"/g' \
		-e 's/\*\*Generated\*\*: .*/**Generated**: <MASKED>/' \
		-e 's/^Generated: .*/Generated: <MASKED>/' \
		-e 's/^Duration: .*/Duration: <MASKED>/' \
		-e 's/\*\*Duration\*\*: .*/**Duration**: <MASKED>/' \
		-e 's/"duration_ms": *[0-9][0-9]*/"duration_ms": <MASKED>/g' \
		"${f}"
	rm -f "${f}.bak"
}

# Runs one argument vector through both binaries and compares stdout,
# stderr, and exit code. Never lets a nonzero leaf exit code trip `set -e`.
compare_invocation() {
	local -a args=("$@")
	local rust_stdout rust_stderr rust_exit
	local fsharp_stdout fsharp_stderr fsharp_exit

	rust_stdout="$(mktemp)"
	rust_stderr="$(mktemp)"
	fsharp_stdout="$(mktemp)"
	fsharp_stderr="$(mktemp)"

	set +e
	"${RUST_BIN}" "${args[@]}" >"${rust_stdout}" 2>"${rust_stderr}"
	rust_exit=$?
	"${FSHARP_BIN}" "${args[@]}" >"${fsharp_stdout}" 2>"${fsharp_stderr}"
	fsharp_exit=$?
	set -e

	mask_volatile_fields "${rust_stdout}"
	mask_volatile_fields "${rust_stderr}"
	mask_volatile_fields "${fsharp_stdout}"
	mask_volatile_fields "${fsharp_stderr}"

	COMPARED=$((COMPARED + 1))

	local mismatch=0
	if [[ "${rust_exit}" -ne "${fsharp_exit}" ]]; then
		mismatch=1
	fi
	if ! diff -q "${rust_stdout}" "${fsharp_stdout}" >/dev/null 2>&1; then
		mismatch=1
	fi
	if ! diff -q "${rust_stderr}" "${fsharp_stderr}" >/dev/null 2>&1; then
		mismatch=1
	fi

	if [[ "${mismatch}" -eq 1 ]]; then
		DIFFERENCES=$((DIFFERENCES + 1))
		echo "shadow-diff: MISMATCH for: ${args[*]}" >&2
		echo "  exit codes: rust=${rust_exit} fsharp=${fsharp_exit}" >&2
		echo "  stdout diff:" >&2
		diff "${rust_stdout}" "${fsharp_stdout}" >&2 || true
		echo "  stderr diff:" >&2
		diff "${rust_stderr}" "${fsharp_stderr}" >&2 || true
	fi

	rm -f "${rust_stdout}" "${rust_stderr}" "${fsharp_stdout}" "${fsharp_stderr}"
}

# Recursively walks the clap-derived subcommand tree under `path`, comparing
# every leaf found. A parent whose bare (no-args) invocation requires a
# subcommand is not itself a leaf; its listed subcommands (everything but
# `help`) are visited instead. Bare invocation of a required-subcommand
# group prints a `Commands:` section (one `  name  description` line per
# subcommand) rather than clap's terser `[subcommands: a, b, c]` bracket
# form that an explicit `--help` produces on the same group — both are
# real, observed shapes of this CLI, but only the bare-invocation shape is
# relevant here since recursion always calls bare.
walk_namespace() {
	local -a path=("$@")
	local output_capture exit_code
	output_capture="$(mktemp)"

	set +e
	"${RUST_BIN}" "${path[@]}" >"${output_capture}" 2>&1
	exit_code=$?
	set -e

	# Lines strictly between "Commands:" and the next blank line, first
	# whitespace-delimited word on each — clap's per-subcommand list shape.
	local -a subcommands=()
	if [[ "${exit_code}" -eq 2 ]] && grep -q '^Commands:$' "${output_capture}"; then
		# A real subcommand line always has exactly two leading spaces before
		# its name (clap's fixed left-pad). A long `about` string that wraps
		# to a second line is indented further, to align under the
		# description column — filtering on `^  [^ ]` (exactly two spaces,
		# then a non-space) keeps the former and drops the latter, so a
		# wrapped continuation's first word (e.g. "entry" from
		# "rewrite-paths"'s two-line about text) is never mistaken for a
		# phantom subcommand.
		while IFS= read -r name; do
			[[ -n "${name}" ]] && subcommands+=("${name}")
		done < <(sed -n '/^Commands:$/,/^$/p' "${output_capture}" | tail -n +2 | sed '/^$/d' | grep -E '^  [^ ]' | awk '{print $1}')
	fi
	rm -f "${output_capture}"

	if [[ "${#subcommands[@]}" -gt 0 ]]; then
		# A group: recurse into every subcommand except the built-in `help`.
		local subcommand
		for subcommand in "${subcommands[@]}"; do
			if [[ "${subcommand}" != "help" ]]; then
				walk_namespace "${path[@]}" "${subcommand}"
			fi
		done
		return
	fi

	# A leaf: compare its bare form, its --help form, and each output format.
	compare_invocation "${path[@]}"
	compare_invocation "${path[@]}" --help
	compare_invocation "${path[@]}" -o text
	compare_invocation "${path[@]}" -o json
	compare_invocation "${path[@]}" -o markdown
}

for namespace in "$@"; do
	walk_namespace "${namespace}"
done

if [[ "${DIFFERENCES}" -gt 0 ]]; then
	echo "shadow-diff: ${COMPARED} invocation(s) compared, ${DIFFERENCES} difference(s)" >&2
	exit 1
fi

echo "shadow-diff: ${COMPARED} invocation(s) compared, 0 difference(s)"
