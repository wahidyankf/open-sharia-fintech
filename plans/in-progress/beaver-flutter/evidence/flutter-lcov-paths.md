# Flutter LCOV path verification

## Command

```sh
npm exec nx run beavernest-app:test:coverage
```

## Result

The target passes `apps/beavernest-app/coverage/lcov.info` to `rhino-cli` as a
repository-relative path. Although the target runs from `apps/beavernest-app`,
`rhino-cli` resolves its coverage argument from the workspace root.

The P1 test reads generated contract source as text and does not execute a Dart
source unit. The resulting LCOV file therefore currently contains no `SF:`
entries and the 80% gate reports `100.00% (0 covered, 0 partial, 0 missed, 0
total)`.

The configured exclusion is `lib/generated/*/*.dart`. It matches only the
current generated schema-model files beneath `lib/generated/schema/`; it does
not match handwritten sources or the generated top-level client. The glob uses
one path segment because the coverage validator deliberately follows Go
`filepath.Match` semantics, where `**` is not recursive. Future tests that
execute generated models must recheck the `SF:` entries before changing this
exclusion.
