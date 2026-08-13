# Flutter LCOV path verification

## Command

```sh
npm exec nx run beavernest-app:test:coverage
```

## Result

The target passes `apps/beavernest-app/coverage/lcov.info` to `rhino-cli` as a
repository-relative path. Although the target runs from `apps/beavernest-app`,
`rhino-cli` resolves its coverage argument from the workspace root.

The initial P1 source-inspection test produced no executable Dart coverage.
The application-facing readiness adapter is now regression-tested, so the
current LCOV file records `SF:lib/platform/web/readiness_client.dart` plus
generated schema paths. The verified target reports `87.76% (43 covered, 0
partial, 6 missed, 49 total)`, above its 80% threshold.

The configured exclusion is `lib/generated/*/*.dart`. It matches only the
current generated schema-model files beneath `lib/generated/schema/`; it does
not match handwritten platform code or the generated top-level client. The
glob uses one path segment because the coverage validator deliberately follows
Go `filepath.Match` semantics, where `**` is not recursive. Future tests that
execute generated models must recheck the `SF:` entries before changing this
exclusion.
