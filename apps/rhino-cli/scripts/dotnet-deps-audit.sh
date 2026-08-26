#!/usr/bin/env bash
# Wrapper turning `dotnet list package --vulnerable` into a real gate.
#
# `dotnet list <project> package --vulnerable --include-transitive` is a
# REPORTING command: it prints a vulnerable-package table (as a build
# warning, NU1903/NU1902) but always exits 0, even when it finds one — see
# plans/in-progress/rewrite-rhino-cli-to-fsharp/learnings.md's `deps:audit`
# scratch-project proof, where a deliberately pinned vulnerable
# `Newtonsoft.Json 12.0.1` reference was reported and the command still
# exited 0. Every rhino-cli-fsharp `deps:audit` target invocation goes
# through this wrapper instead of the bare `dotnet list` command so a
# finding actually turns the target (and therefore the CI job invoking it)
# red, per tech-docs.md DD-8.
#
# Usage: dotnet-deps-audit.sh <path-to-.fsproj-or-.csproj>

set -euo pipefail

if [[ $# -ne 1 ]]; then
	echo "usage: dotnet-deps-audit.sh <path-to-project-file>" >&2
	exit 2
fi

PROJECT="$1"

REPORT_JSON="$(dotnet list "${PROJECT}" package --vulnerable --include-transitive --format json)"

# A finding is any non-empty `vulnerabilities` array under either
# top-level or transitive packages, across every framework and project in
# the report — jq's `any(...)` short-circuits on the first match.
if echo "${REPORT_JSON}" | jq -e '
    any(
      .projects[]?.frameworks[]?;
      (.topLevelPackages[]?.vulnerabilities? // [] | length > 0)
      or (.transitivePackages[]?.vulnerabilities? // [] | length > 0)
    )
  ' >/dev/null; then
	echo "deps:audit: vulnerable package(s) found — failing the gate" >&2
	# Re-run in the default human-readable format so the offending
	# package/version/advisory is visible in CI logs, not only in the JSON
	# this wrapper parsed.
	dotnet list "${PROJECT}" package --vulnerable --include-transitive >&2 || true
	exit 1
fi

echo "deps:audit: no vulnerable packages found"
