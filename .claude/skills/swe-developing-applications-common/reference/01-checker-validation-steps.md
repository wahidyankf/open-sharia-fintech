# swe-code-checker Validation Steps 1-6

Detailed rule set for `swe-code-checker`'s core infrastructure and language-standard validation.

## Step 1: Discover Projects

List all `apps/`/`libs/` projects; read each `project.json` for tags (`type`, `platform`, `lang`,
`domain`), available targets, and language; group by language for language-specific validation.

## Step 2: Nx Target Infrastructure (All Languages)

Reference: `repo-governance/development/infra/nx-targets.md`.

- **Mandatory targets**: apps need `build`, `lint`, `test:quick`; libs need `lint`, `test:quick`
  — check each exists in `project.json` with a non-empty command.
- **Tag convention**: all 4 dimensions present (`type:app|lib`, `platform:*`, `lang:*`,
  `domain:*`) with values following convention.
- **CGO_ENABLED=0 (Go)**: every Go target (`build`, `test:quick`, `test:unit`,
  `test:integration`, `lint`) must prefix its command with `CGO_ENABLED=0` — HIGH if missing
  (build reproducibility).
- **Cache configuration**: `build`/`lint`/`test:quick` need `cache: true` (`build` needs proper
  `outputs`); `test:integration` only if it uses in-process mocking; `dev` needs `cache: false` or
  absent.
- **Coverage enforcement**: Go `test:quick` must include
  `rhino-cli test-coverage validate <path>/cover.out 95`; TypeScript must include
  `rhino-cli test-coverage validate <path>/lcov.info 95`; Rust must enforce ≥90% via
  `cargo-llvm-cov`/`rhino-cli test-coverage validate`.

## Step 3: Go-Specific Standards

Reference: AyoKoding Go educational content (`ose-public` has no Go projects of its own today; these
checks apply the moment one is added).

- **go.mod version**: must specify the current platform standard (Go 1.26) — MEDIUM if outdated.
- **Single-line main()**: `func main() { cmd.Execute() }` or equivalent; multi-line indicates
  uncovered paths — MEDIUM.
- **os.Exit dependency injection**: `var osExit = os.Exit` pattern in `cmd/root.go`, mocked in
  tests for error-path coverage — MEDIUM.
- **Cobra CLI patterns** (CLI apps): `RunE` not `Run`; root sets `SilenceErrors: true`;
  domain-prefixed subcommand naming (`{app} {domain} {action}`) — HIGH.
- **Integration tests**: Godog BDD tests in `test/integration/` or `internal/*/test/`, `.feature`
  files, `integration` build tag — MEDIUM.
- **Test patterns**: table-driven preferred, raw `testing.T` (no testify in unit tests),
  `*_test.go` naming — LOW.
- **Output functions**: `outputFuncs` pattern (text/json/markdown formatters), consistent across
  commands — LOW.

## Step 4: TypeScript-Specific Standards

Reference: `docs/explanation/software-engineering/programming-languages/typescript/`.

- **Vitest coverage**: `vitest.config.ts` configures thresholds, v8 provider preferred — HIGH.
- **Test structure**: unit as `*.test.ts`/`*.spec.ts`; MSW-based integration in a separate
  `test:integration` target; no unit/integration duplication — MEDIUM.
- **ESLint**: lint target present, no per-project overrides that weaken rules — MEDIUM.

## Step 5: Rust-Specific Standards

Reference: `docs/explanation/software-engineering/programming-languages/rust/README.md`.

- **Coverage**: `cargo-llvm-cov` line coverage ≥90% via `rhino-cli test-coverage validate` — HIGH.
- **Error handling**: `Result<T, E>` for fallible ops, no `.unwrap()` in production paths, typed
  enums (not `anyhow::Error`) at domain boundaries — HIGH.
- **Axum patterns** (if applicable): handlers return `impl IntoResponse` with no panics; state via
  `Extension<Arc<T>>`/`State<T>` not globals; integration tests call service functions directly,
  not through HTTP — MEDIUM.

## Step 6: Cross-Project Consistency

- **Go version alignment**: all Go projects share one `go.mod` version — HIGH if mismatched.
- **Coverage uniformity**: all projects enforce ≥95% line coverage — HIGH if any project is below.
- **Shared library usage**: Go projects import `golang-commons`; TypeScript projects use workspace
  libs; flag duplicated utility code — MEDIUM.
