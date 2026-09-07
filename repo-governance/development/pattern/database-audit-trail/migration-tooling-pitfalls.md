---
description: "Lessons learned from adding migration tooling across eight language ecosystems, covering schema fidelity, coverage tooling, embedded filesystems, locale, and Docker environment differences."
when_to_use: "Use when adding or debugging migration tooling for a new language ecosystem and want to avoid known pitfalls."
---

# Migration Tooling Pitfalls

Lessons from adding migration tooling across 8 language ecosystems (2026-03-27). These apply to any
project replacing programmatic DDL (`AutoMigrate`, `create_all`, `EnsureCreated`, `SchemaUtils.create`)
with dedicated migration tools.

## Match the original schema exactly

Migration SQL must produce the **identical schema** that the previous programmatic DDL created — same
column types, same precision, same constraints. Common mismatches that break E2E tests:

- **DECIMAL precision**: `DECIMAL(19,4)` forces trailing zeros (`10.5000` vs `10.50`). If the
  original DDL used `DECIMAL` (arbitrary precision), keep it.
- **FK constraints**: ORMs like EF Core `EnsureCreated()` and Exposed `SchemaUtils.create()` often
  do NOT create FK constraints unless navigation properties are explicitly defined. Adding FKs in
  migration SQL breaks code that inserts with empty/placeholder foreign keys (e.g., `Guid.Empty`).
- **Type mismatches**: `UUID` vs `TEXT`, `TIMESTAMPTZ` vs `timestamp without time zone`. Check what
  the ORM driver actually generates.

**Rule**: Before writing migration SQL, inspect the original DDL source (the programmatic code being
replaced) and replicate its types exactly.

## Coverage tool configuration

When adding new Cargo crates (SQLx migrate), Go modules (goose), or Python packages (Alembic):

- **cargo-llvm-cov (Rust)**: Migration SQL files do not inflate coverage. Ensure `migrations/`
  is listed in Nx `inputs` so cache invalidates when migration files change.
- **Nx inputs**: For Go apps using `embed.FS`, add the migrations directory to `inputs` in
  `project.json` so Nx cache invalidates when migration files change.

## Embedded filesystem paths

Go's `embed.FS` creates a filesystem rooted at the package directory. When using
`goose.NewProvider(dialect, db, embedFS)`, goose expects migration files at the FS root. If the
embed directive is `//go:embed migrations/*.sql`, files live under `migrations/` — use
`fs.Sub(embedFS, "migrations")` to give goose the correct root.

## JVM locale affects test parsing

Cucumber JVM's `{double}` parameter type uses the JVM default locale. On locales where `.` is the
thousands separator (e.g., `id_ID`), `50.5` parses as `505.0`. Fix by adding
`-Duser.language=en -Duser.country=US` to JVM opts in test runner configuration.

## Docker environment differences

Networked database E2E tests (including any legacy image still named `Dockerfile.integration`) and
process E2E tests (`cargo run` / `uv run` with volume mount) may behave differently. The filename
does not change the boundary: PostgreSQL reached over TCP is E2E, not Integration.

- **Rust migrations**: SQLx `sqlx::migrate!` embeds migration SQL at compile time. When using
  volume mounts, ensure `migrations/` is present in the container build context.
- **Go version**: Keep `Dockerfile`, `Dockerfile.integration`, AND `Dockerfile.be.dev` in sync with
  `go.mod`'s Go version requirement.
- **Python Alembic**: The database-E2E image needs explicit `COPY alembic/ alembic/` and
  `COPY alembic.ini alembic.ini` — the standard `COPY . .` may not include them if `.dockerignore`
  is aggressive.
