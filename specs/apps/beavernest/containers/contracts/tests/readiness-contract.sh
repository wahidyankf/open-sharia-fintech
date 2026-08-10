#!/usr/bin/env bash
# Assertion-only guard for the public readiness OpenAPI contract.
set -euo pipefail

repository_root="$(git rev-parse --show-toplevel)"
contract="$repository_root/specs/apps/beavernest/containers/contracts/openapi.yaml"

assert_contains() {
	local expected="$1"

	if ! grep -Fq -- "$expected" "$contract"; then
		printf 'Expected OpenAPI contract to contain: %s\n' "$expected" >&2
		exit 1
	fi
}

assert_text_contains() {
	local text="$1"
	local expected="$2"

	if ! grep -Fq -- "$expected" <<<"$text"; then
		printf 'Expected OpenAPI contract section to contain: %s\n' "$expected" >&2
		exit 1
	fi
}

schema_block() {
	local schema_name="$1"

	awk -v header="    ${schema_name}:" '
    $0 == header { capture = 1; next }
    capture && /^    [A-Za-z][A-Za-z0-9]*:$/ { exit }
    capture { print }
  ' "$contract"
}

readiness_path="$({
	awk '
    /^  \/api\/v1\/readiness:$/ { capture = 1; next }
    capture && /^  \/api\/v1\// { exit }
    capture { print }
  ' "$contract"
})"

assert_text_contains "$readiness_path" '      operationId: getReadiness'
assert_text_contains "$readiness_path" '        "200":'
assert_text_contains "$readiness_path" '        "503":'
assert_text_contains "$readiness_path" '              $ref: "#/components/schemas/ReadinessReady"'
assert_text_contains "$readiness_path" '              $ref: "#/components/schemas/ReadinessUnavailable"'

if [ "$(grep -Fxc '            Cache-Control:' <<<"$readiness_path")" -ne 2 ] || [ "$(grep -Fxc '                const: no-store' <<<"$readiness_path")" -ne 2 ]; then
	printf 'Each readiness response must require Cache-Control: no-store\n' >&2
	exit 1
fi

ready_schema="$(schema_block ReadinessReady)"
assert_text_contains "$ready_schema" '      additionalProperties: false'
assert_text_contains "$ready_schema" '          const: ready'
assert_text_contains "$ready_schema" '              const: ready'
assert_text_contains "$ready_schema" '              const: current'

unavailable_schema="$(schema_block ReadinessUnavailable)"
assert_text_contains "$unavailable_schema" '      additionalProperties: false'
assert_text_contains "$unavailable_schema" '          const: not-ready'
assert_text_contains "$unavailable_schema" '              const: unavailable'
assert_text_contains "$unavailable_schema" '              const: unknown'

if grep -Eq 'getHello|^[[:space:]]+Greeting:' "$contract"; then
	printf 'Retired greeting operation or schema must not remain in the OpenAPI contract\n' >&2
	exit 1
fi

if grep -Eq '(^|[^[:alnum:]])(ETag|Last-Modified)([^[:alnum:]]|$)' "$contract"; then
	printf 'Readiness contract must not declare a response validator header\n' >&2
	exit 1
fi
