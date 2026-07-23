# ADR-0002: SOLID + functional-core / imperative-shell refactor

**Status**: Accepted
**Date**: 2026-07-19

## Context

Pass 1's `app/repository.py` mixed data access with domain-object hydration; `app/main.py`'s
route handlers called `repo.*` functions directly. Nothing was formally WRONG with this for a
single-file capstone, but it does not demonstrate: (a) depending on an abstraction rather than
a concrete database module (Dependency Inversion Principle), (b) a business-rule layer
independently testable without a database (Single Responsibility Principle), or (c) a pure
computational core separated from the parts that touch state (functional core / imperative
shell, topics 22/23).

## Decision

- Introduce `app/ports.py`: a `HabitRepository` `Protocol` (structural typing, PEP 544) naming
  every operation the application layer needs from storage.
- Introduce `app/services.py`: `HabitService`, depending only on `HabitRepository`, owning the
  business rules (e.g., "a check-in needs an owned habit") that used to live inline in route
  handlers.
- `app/repository_sqlite.py`'s `SqliteHabitRepository` is the ONE concrete adapter that ships in
  production, satisfying `HabitRepository` by shape, never by inheritance.
- `app/domain.py` splits into pure functions (`current_streak`, `longest_streak_ever`,
  `longest_streak_ever_naive`) plus a thin `Habit` shell that delegates to them -- the
  computation itself needs no database, no HTTP server, and no `Habit` instance to be tested.

## Consequences

- **Positive (Open/Closed proof)**: `tests/test_services.py` adds `InMemoryHabitRepository` --
  a SECOND class satisfying `HabitRepository` -- with zero edits to `services.py`, `ports.py`,
  or `repository_sqlite.py`. `HabitService` accepts it exactly as it accepts the real adapter.
- **Positive**: the functional core (`domain.py`'s free functions) is independently
  benchmarkable (`bench/benchmark_algorithm.py`) without spinning up a database or server.
- **Trade-off**: one more file, one more layer of indirection (`main.py` -> `HabitService` ->
  `HabitRepository` -> `SqliteHabitRepository`) than Pass 1's flatter shape -- justified here
  because the syllabus spec requires a DEMONSTRATED OCP extension point, not just a claim of one.

## Verification

Behavior preservation: `tests/test_app.py`'s full integration suite (auth, CRUD, ownership,
injection-safety) passes unchanged in spirit against the refactored code (see this page's Step
2 transcript). OCP: `tests/test_services.py::TestHabitServiceWithInMemoryRepository` passes
against `InMemoryHabitRepository`, added without touching any shipped `app/` file.
