# Dart-Native OpenAPI Generator Spike

**Recorded**: 2026-08-13

## Selected Generator

`openapi_spec` `0.15.0` is the selected native-Dart generator. Its published CLI reads the local
OpenAPI 3.1 bundle and emits a Dart HTTP client plus separate `ReadinessReady` and
`ReadinessUnavailable` model definitions. It was published on 2025-08-03 under BSD-3-Clause;
therefore it meets Path B's 2026-06-14 (2026-08-13 minus 60 days) cutoff.

The generated schema uses Freezed serialization. The direct pins are all exact and pre-cutoff:
`http` `1.6.0` (2025-11-10), `meta` `1.17.0` (SDK-compatible), `freezed_annotation` `3.1.0`
(2025-07-02), `json_annotation` `4.12.0` (2026-05-15), `build_runner` `2.15.0` (2026-04-30),
`freezed` `3.2.5` (2026-02-03), `json_serializable` `6.14.0` (2026-05-15), and `flutter_lints`
`6.0.0` (2025-05-27).

Commands proven from `apps/beavernest-app/`:

```bash
npm exec nx run beavernest-contracts:bundle
fvm dart run openapi_spec generate --path ../../specs/apps/beavernest/containers/contracts/generated/openapi-bundled.yaml --destination lib/generated --package_name beavernest_api --force
fvm dart run build_runner build --delete-conflicting-outputs
fvm flutter test test/generated_contract_test.dart
fvm dart analyze lib/generated test/generated_contract_test.dart
```

The last two commands pass. `lib/generated/` contains only generator output, including the
Freezed `schema.freezed.dart` and JSON `schema.g.dart` artifacts; no model is handwritten.

## Rejected Candidates

- `dart_openapi_generator` `0.2.0`: functionally generated the required named variants, but it was
  published six days before evaluation. It fails the mandatory 60-day non-LTS soak and is retained
  only under ignored `local-temp/rejected-dart-openapi-generator-output/` for auditability.
- `space_gen` `1.0.1`: it warned that contract `const` values were ignored and attempted an offline
  nested-package resolution requiring an unavailable formatter dependency. Its output is retained
  only under ignored `local-temp/rejected-space-gen-output/`.

## Security and Functional Review

On 2026-08-13, the OSV Pub batch query returned an empty result for each selected direct pin. The
NVD exact-name lookup returned zero results for `openapi_spec`; generic `http` keyword hits are not
attributable to the Pub package and were not treated as package vulnerabilities. GitHub Advisory
Database and Snyk package searches returned no advisory matching `openapi_spec`; the upstream
repository exposes no `SECURITY.md` policy. The CISA KEV feed has zero matching Dart, Flutter,
Taza, OpenAPI, Freezed, or `json_serializable` entries. No CVE was found, so no EPSS lookup or
waiver applies. Pub.dev reports the package as active; the generation, formatter, test, and
analyzer checks above found no primary-function defect. Clearance: **CLEAR**.
