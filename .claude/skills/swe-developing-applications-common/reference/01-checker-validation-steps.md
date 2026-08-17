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
- **Cache configuration**: `build`/`lint`/`test:quick` need `cache: true` (`build` needs proper
  `outputs`); `test:integration` only if it uses in-process mocking; `dev` needs `cache: false` or
  absent.
- **Coverage enforcement**: TypeScript `test:quick` must include
  `rhino-cli test-coverage validate <path>/lcov.info 95`; Rust must enforce ≥90% via
  `cargo-llvm-cov`/`rhino-cli test-coverage validate`; F# must pass a `/p:Threshold` line
  threshold to `dotnet test --collect:"XPlat Code Coverage"`.

## Step 3: F#-Specific Standards

Reference: `docs/explanation/software-engineering/programming-languages/f-sharp/README.md`.

- **Coverage**: `dotnet test --collect:"XPlat Code Coverage"` with an explicit
  `/p:Threshold` + `/p:ThresholdType=line` — HIGH if the threshold is absent.
- **Railway-oriented error handling**: fallible operations return `Result<_, _>`; no bare
  `failwith` on a domain path — HIGH.
- **Type safety**: domain values wrapped in single-case DUs rather than raw primitives;
  exhaustive `match` with no catch-all silently swallowing cases — HIGH.
- **Giraffe/API patterns** (if applicable): handlers compose `HttpHandler` functions; wiring lives
  in the composition root, not in domain modules — MEDIUM.
- **Test patterns**: unit suites under `tests/unit/*.fsproj`, scenario-named tests that auto-bind
  to the Gherkin scenario titles the spec-coverage gate reads — MEDIUM.

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

- **Toolchain version alignment**: all projects in one ecosystem share a single pinned version
  (`.tool-versions`, `global.json`, `rust-toolchain.toml`) — HIGH if mismatched.
- **Coverage uniformity**: all projects enforce the language's declared line-coverage floor — HIGH
  if any project is below it.
- **Shared library usage**: TypeScript projects use workspace libs rather than copied helpers;
  flag duplicated utility code — MEDIUM.
