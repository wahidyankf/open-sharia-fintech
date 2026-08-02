# Technical Approach — Database Internals Course Ruff Configuration

## Architecture

Ruff resolves configuration by walking from each formatted Python file toward its ancestors. A
`ruff.toml` at the course root therefore applies to the course's `learning/` and `drilling/` Python
subtrees without altering another course or a repository-level default.

## Decision

Use a course-scoped configuration rather than reformatting source or changing a shared policy. This
matches other annotation-heavy courses and keeps the blast radius to one course directory.

## File Impact

| Path | Change |
| --- | --- |
| `apps/ayokoding-www/content/en/learn/courses/database-internals-and-storage-engines/ruff.toml` | Add the measured, supported Ruff line-length setting with a concise rationale. |
| `plans/backlog/ayokoding-database-internals-ruff-config/` | Track requirements, delivery evidence, and Knowledge Capture. |

No file beneath `apps/ayokoding-www/src/features/course-paths/manifests/` is in scope.

## Mechanics

1. Confirm the target course has no existing root `ruff.toml`.
2. Measure the longest annotated Python line across `learning/` and `drilling/`.
3. Add a root `ruff.toml` whose `line-length` covers that baseline and is accepted by the installed
   Ruff version.
4. Run `ruff format --check` against all target Python files. Do not run an in-place formatter.

## Dependencies

- The repository's installed Ruff formatter.
- Existing course Python files and their test examples.

## Verification and Rollback

Verification uses a non-mutating Ruff check plus the affected-project quality gate. Roll back by
removing only the new course-root `ruff.toml`; no source migration or data change is involved.
