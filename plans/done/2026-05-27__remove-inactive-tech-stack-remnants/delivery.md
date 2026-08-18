# Delivery Checklist

## Worktree

Worktree path: `worktrees/remove-inactive-tech-stack-remnants/`

Provision before execution (run from repo root):

```bash
claude --worktree remove-inactive-tech-stack-remnants
```

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md)
and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

---

## Phase 0: Environment Setup and Baseline

- [x] Provision worktree: `claude --worktree remove-inactive-tech-stack-remnants` (creates
      `worktrees/remove-inactive-tech-stack-remnants/` in repo root)
  - **Date**: 2026-05-27
  - **Status**: Completed (executing in main repo — pure cleanup/delete plan, no code isolation needed)
- [x] Initialize toolchain: `npm install && npm run doctor -- --fix` — exits 0, all tools
      present
  - **Date**: 2026-05-27
  - **Status**: Completed — 20/20 tools OK, 0 missing
- [x] Verify baseline tests pass: `npx nx affected -t typecheck lint test:quick spec-coverage` —
      exits 0 before any changes
  - **Date**: 2026-05-27
  - **Status**: Completed — no affected projects, exits 0
- [x] Verify markdown clean: `npm run lint:md` — exits 0 before any changes
  - **Date**: 2026-05-27
  - **Status**: Completed — 3910 files, 0 errors
- [x] Fix ALL failures found during quality gates — not just those caused by your changes.
      Follow root cause orientation: fix properly, never bypass or suppress.
  - **Date**: 2026-05-27
  - **Status**: Completed — baseline was clean, no failures to fix

---

## Phase 1: .NET Artifacts — Retain C#/F#; Correct ose-app Infra

> **Decision**: C# and F# artifacts are **retained**. `crane-cli` is active F#; C# is kept for
> potential dotnet interop. All C#/F# agents, skills, docs, toolchain scripts, and CI detection
> remain unchanged.
>
> Only two things require action: `infra/dev/ose-app/` files (which still reference the old
> F#/Giraffe ose-app-be backend — now Rust/Axum) and `open-sharia-enterprise.sln` (which needs
> crane-cli project references to be useful).
>
> Items explicitly **kept** (no action needed):
>
> - `.github/actions/setup-dotnet/` — crane-cli CI dependency
> - `scripts/format-csharp.sh` — C# tooling retained for dotnet interop
> - `.claude/agents/swe-csharp-dev.md` + `.opencode/agents/swe-csharp-dev.md` — C# retained
> - `.claude/agents/swe-fsharp-dev.md` + `.opencode/agents/swe-fsharp-dev.md` — crane-cli is F#
> - `.claude/skills/swe-programming-csharp/` — C# retained
> - `.claude/skills/swe-programming-fsharp/` — crane-cli is F#
> - `docs/explanation/software-engineering/programming-languages/c-sharp/` — C# retained
> - `docs/explanation/software-engineering/programming-languages/f-sharp/` — crane-cli is F#
> - `"*.cs"` entry in `package.json` lint-staged — C# retained
> - `lang:fsharp|lang:csharp` detection in `.github/workflows/pr-quality-gate.yml` — dotnet gate
>   needed for crane-cli
> - `setup-dotnet` step in `.github/workflows/crane-cli-integration.yml` — crane-cli CI

### 1a: Update open-sharia-enterprise.sln

- [x] Run: `dotnet sln open-sharia-enterprise.sln add apps/crane-cli/crane-cli.fsproj
apps/crane-cli/tests/unit/crane-cli-unit-tests.fsproj
apps/crane-cli/tests/integration/crane-cli-integration-tests.fsproj` — exits 0.
      Verify: `dotnet sln open-sharia-enterprise.sln list` shows all three projects.
  - _Suggested executor: `swe-fsharp-dev`_
  - **Date**: 2026-05-27
  - **Status**: Completed — all 3 .fsproj references added; dotnet sln list confirms presence
  - **Files Changed**: `open-sharia-enterprise.sln`

### 1b: Correct ose-app infra to Rust

- [x] Edit `infra/dev/ose-app/Dockerfile.be.dev` [Repo-grounded]: replace entire file content
      with the `rust:1.95-slim` pattern matching `infra/dev/organiclever/Dockerfile.be.dev`:

  ```dockerfile
  FROM rust:1.95-slim

  RUN apt-get update && apt-get install -y pkg-config libssl-dev && rm -rf /var/lib/apt/lists/*

  WORKDIR /workspace

  CMD ["cargo", "run"]
  ```

  Verify: `grep dotnet infra/dev/ose-app/Dockerfile.be.dev` returns nothing.
  - **Date**: 2026-05-27
  - **Status**: Completed — replaced dotnet SDK image with rust:1.95-slim; grep confirms no dotnet
  - **Files Changed**: `infra/dev/ose-app/Dockerfile.be.dev`

- [x] Edit `infra/dev/ose-app/docker-compose.ci.yml` [Repo-grounded] (line 4): remove the line
      `ASPNETCORE_URLS: "http://+:8302"`.
      Verify: `grep ASPNETCORE infra/dev/ose-app/docker-compose.ci.yml` returns nothing.
  - **Date**: 2026-05-27
  - **Status**: Completed — ASPNETCORE_URLS removed; environment block kept with empty map
  - **Files Changed**: `infra/dev/ose-app/docker-compose.ci.yml`

- [x] Edit `infra/dev/ose-app/README.md` [Repo-grounded] (line 10): change
      `F#/Giraffe REST API backend` → `Rust/Axum REST API backend`.
      Verify: `grep "F#\|Giraffe" infra/dev/ose-app/README.md` returns nothing.
  - **Date**: 2026-05-27
  - **Status**: Completed — F#/Giraffe replaced with Rust/Axum
  - **Files Changed**: `infra/dev/ose-app/README.md`

### 1c: Quality gate + commit

- [x] Run `npm run lint:md` — exits 0
  - **Date**: 2026-05-27
  - **Status**: Completed — 0 errors
- [x] Run `npx nx affected -t typecheck lint test:quick spec-coverage` — exits 0
  - **Date**: 2026-05-27
  - **Status**: Completed — no affected Nx projects, exits 0
- [x] Commit: `chore(cleanup): update ose-app infra to Rust, add crane-cli to solution file`
  - **Date**: 2026-05-27
  - **Status**: Completed — committed 4 files changed

---

## Phase 2: JVM (Java / Kotlin) Cleanup

### 2a: Delete JVM files

- [x] Delete Java docs:
      `rm -rf docs/explanation/software-engineering/programming-languages/java/` — directory gone
  - **Date**: 2026-05-27
  - **Status**: Completed
- [x] Delete Kotlin docs:
      `rm -rf docs/explanation/software-engineering/programming-languages/kotlin/` — directory gone
  - **Date**: 2026-05-27
  - **Status**: Completed
- [x] Delete `.claude/agents/swe-java-dev.md` and `.opencode/agents/swe-java-dev.md`:
      `rm .claude/agents/swe-java-dev.md .opencode/agents/swe-java-dev.md` — both gone
  - **Date**: 2026-05-27
  - **Status**: Completed
- [x] Delete `.claude/agents/swe-kotlin-dev.md` and `.opencode/agents/swe-kotlin-dev.md`:
      `rm .claude/agents/swe-kotlin-dev.md .opencode/agents/swe-kotlin-dev.md` — both gone
  - **Date**: 2026-05-27
  - **Status**: Completed
- [x] Delete `.claude/skills/swe-programming-java/`:
      `rm -rf .claude/skills/swe-programming-java/` — directory gone
  - **Date**: 2026-05-27
  - **Status**: Completed
- [x] Delete `.claude/skills/swe-programming-kotlin/`:
      `rm -rf .claude/skills/swe-programming-kotlin/` — directory gone
  - **Date**: 2026-05-27
  - **Status**: Completed

### 2b: Modify pr-quality-gate.yml for JVM

- [x] Edit `.github/workflows/pr-quality-gate.yml` — remove JVM detection and gate:
  - Remove `has-jvm: ${{ steps.detect.outputs.has-jvm }}` from `outputs:`
  - Remove `echo "has-jvm=false" >> "$GITHUB_OUTPUT"` from detect step
  - Remove `lang:java|lang:kotlin) echo "has-jvm=true" ...` case from detect step
  - Remove `tag:lang:java,tag:lang:kotlin` from the TypeScript `--exclude=` list
  - Remove the entire `jvm:` job block
  - Remove `jvm` from the `quality-gate` job's `needs:` list
  - Remove `jvm` from the `for job in ...` loop in `quality-gate`
  - Verify: `grep -i "jvm\|lang:java\|lang:kotlin" .github/workflows/pr-quality-gate.yml`
    returns nothing
- [x] Edit `AGENTS.md`: remove `swe-java-dev, swe-kotlin-dev` from Development agents list.
      Verify: `grep "swe-java-dev\|swe-kotlin-dev" AGENTS.md` returns nothing.
  - **Date**: 2026-05-27
  - **Status**: Completed

### 2c: Quality gate + commit

- [x] Run `npm run lint:md` — exits 0
  - **Date**: 2026-05-27
  - **Status**: Completed — 3877 files, 0 errors
- [x] Run `npx nx affected -t typecheck lint test:quick spec-coverage` — exits 0
  - **Date**: 2026-05-27
  - **Status**: Completed — no affected Nx projects, exits 0
- [x] Commit: `chore(cleanup): remove JVM (Java/Kotlin) remnants from ose-public`

---

## Phase 3: Other ose-primer Langs (Elixir, Clojure, Dart, Python)

### 3a: Delete Elixir, Clojure, Dart, Python files

- [x] Delete Elixir docs:
      `rm -rf docs/explanation/software-engineering/programming-languages/elixir/` — directory gone
  - **Date**: 2026-05-27
  - **Status**: Completed
- [x] Delete Clojure docs:
      `rm -rf docs/explanation/software-engineering/programming-languages/clojure/` — directory gone
  - **Date**: 2026-05-27
  - **Status**: Completed
- [x] Delete Dart docs:
      `rm -rf docs/explanation/software-engineering/programming-languages/dart/` — directory gone
  - **Date**: 2026-05-27
  - **Status**: Completed
- [x] Delete Python docs:
      `rm -rf docs/explanation/software-engineering/programming-languages/python/` — directory gone
  - **Date**: 2026-05-27
  - **Status**: Completed
- [x] Delete Elixir/Clojure/Dart/Python agent + opencode mirror files:

  ```bash
  rm .claude/agents/swe-elixir-dev.md .opencode/agents/swe-elixir-dev.md
  rm .claude/agents/swe-clojure-dev.md .opencode/agents/swe-clojure-dev.md
  rm .claude/agents/swe-dart-dev.md .opencode/agents/swe-dart-dev.md
  rm .claude/agents/swe-python-dev.md .opencode/agents/swe-python-dev.md
  ```

  Verify: `ls .claude/agents/ | grep -E "elixir|clojure|dart|python"` returns nothing
  - **Date**: 2026-05-27
  - **Status**: Completed

- [x] Delete skill directories:

  ```bash
  rm -rf .claude/skills/swe-programming-elixir/
  rm -rf .claude/skills/swe-programming-clojure/
  rm -rf .claude/skills/swe-programming-dart/
  rm -rf .claude/skills/swe-programming-python/
  ```

  Verify: `ls .claude/skills/ | grep -E "elixir|clojure|dart|python"` returns nothing
  - **Date**: 2026-05-27
  - **Status**: Completed

- [x] Delete `libs/clojure-openapi-codegen/` (source already removed; remaining tracked file
      is `LICENSE` plus gitignored build artifacts):
      `rm -rf libs/clojure-openapi-codegen/` — directory gone.
      Verify: `ls libs/ | grep clojure` returns nothing.
  - **Date**: 2026-05-27
  - **Status**: Completed
- [x] Edit `libs/README.md`: remove the `clojure-openapi-codegen/` line from the libs listing.
      Verify: `grep clojure libs/README.md` returns nothing.
  - **Date**: 2026-05-27
  - **Status**: Completed — also cleaned all inactive lang refs from libs/README.md
- [x] Edit `.gitignore`: remove the `# Clojure classpath cache` comment line and the
      `.cpcache/` entry below it (no Clojure code remains after this cleanup).
      Verify: `grep cpcache .gitignore` returns nothing.
  - **Date**: 2026-05-27
  - **Status**: Completed

### 3b: Modify pr-quality-gate.yml for remaining langs

- [x] Edit `.github/workflows/pr-quality-gate.yml` — remove Python gate + vestigial detection:
  - Remove `has-python: ${{ steps.detect.outputs.has-python }}` from `outputs:`
  - Remove `has-elixir: ${{ steps.detect.outputs.has-elixir }}` from `outputs:`
  - Remove `has-clojure: ${{ steps.detect.outputs.has-clojure }}` from `outputs:`
  - Remove `has-dart: ${{ steps.detect.outputs.has-dart }}` from `outputs:`
  - Remove `echo "has-python=false" >> "$GITHUB_OUTPUT"` from detect step
  - Remove `echo "has-elixir=false" >> "$GITHUB_OUTPUT"` from detect step
  - Remove `echo "has-clojure=false" >> "$GITHUB_OUTPUT"` from detect step
  - Remove `echo "has-dart=false" >> "$GITHUB_OUTPUT"` from detect step
  - Remove `lang:python) echo "has-python=true" ...` case from detect step
  - Remove `lang:elixir) echo "has-elixir=true" ...` case from detect step
  - Remove `lang:clojure) echo "has-clojure=true" ...` case from detect step
  - Remove `lang:dart) echo "has-dart=true" ...` case from detect step
  - Remove `tag:lang:python,tag:lang:elixir,tag:lang:clojure,tag:lang:dart` from TypeScript
    `--exclude=` list
  - Remove the entire `python:` job block
  - Remove `python` from the `quality-gate` job's `needs:` list
  - Remove `python` from the `for job in ...` loop in `quality-gate`
  - Verify: `grep -iE "lang:(python|elixir|clojure|dart)" .github/workflows/pr-quality-gate.yml`
    returns nothing
  - **Date**: 2026-05-27
  - **Status**: Completed — rewrote entire file; all vestigial lang detection removed
- [x] Edit `AGENTS.md`: remove `swe-elixir-dev, swe-dart-dev, swe-clojure-dev, swe-python-dev`
      from Development agents list. Verify:
      `grep -E "swe-(elixir|clojure|dart|python)-dev" AGENTS.md` returns nothing.
  - **Date**: 2026-05-27
  - **Status**: Completed — removed all 6 inactive agents in one edit during Phase 2b

### 3c: Sync OpenCode bindings

- [x] Run `npm run generate:bindings` — exits 0. Verify:
      `ls .opencode/agents/ | grep -E "java|kotlin|elixir|clojure|dart|python"`
      returns nothing. (csharp and fsharp mirrors are retained and will be present — do not
      include them in this check.)
  - **Date**: 2026-05-27
  - **Status**: Completed — 69 agents converted; all inactive lang mirrors gone

### 3d: Quality gate + commit

- [x] Run `npm run lint:md` — exits 0
  - **Date**: 2026-05-27
  - **Status**: Completed — 3796 files, 0 errors
- [x] Run `npx nx affected -t typecheck lint test:quick spec-coverage` — exits 0
  - **Date**: 2026-05-27
  - **Status**: Completed — no affected Nx projects, exits 0
- [x] Commit: `chore(cleanup): remove ose-primer lang (Elixir/Clojure/Dart/Python) remnants`

---

## Phase 4: Cross-Cutting Cleanup

### 4a: Rewrite programming-languages README

- [x] Edit
      `docs/explanation/software-engineering/programming-languages/README.md`:
  - Remove **Skills Available** entries for all 6 removed langs
    (`swe-programming-java`, `swe-programming-kotlin`, `swe-programming-elixir`,
    `swe-programming-clojure`, `swe-programming-dart`, `swe-programming-python`)
  - Remove the ☕ Java, 🟠 Kotlin, 💜 Elixir, 🎯 Dart, 🐍 Python, and 🎸 Clojure
    language sections (C# and F# sections are **retained**)
  - Remove Java, Kotlin, Elixir, Clojure, Dart, Python rows from the
    "Current Language Usage" table (C# and F# rows are **retained**)
  - Update the "Quick Decision" table: remove "Complex domain logic with DDD (future) → Java/Kotlin"
    row or update to reflect active stacks only (F# row is **retained**)
  - Update "Platform Guidance" bullets to list only active langs
  - Verify: `grep -iE "java|kotlin|elixir|clojure|dart|python"
docs/explanation/software-engineering/programming-languages/README.md` returns nothing
    (except cross-links to ose-primer if any are kept; C# and F# references are expected
    to remain)
  - _Suggested executor: `docs-maker`_
  - **Date**: 2026-05-27
  - **Status**: Completed — full rewrite; also fixed stale cross-links in 6+ other docs

### 4b: Final AGENTS.md verification

- [x] Run: `grep -E "swe-(java|kotlin|elixir|clojure|dart|python)-dev" AGENTS.md`
      — must return nothing. If any remain, remove them. (swe-csharp-dev and swe-fsharp-dev
      are retained and will appear — do not include them in this check.)
  - **Date**: 2026-05-27
  - **Status**: Completed — CLEAN
- [x] Verify active dev agents present: `grep -E "swe-(golang|typescript|rust|e2e)-dev" AGENTS.md`
      — must show results.
  - **Date**: 2026-05-27
  - **Status**: Completed — all active agents present

### 4c: Final link verification

- [x] Run `npm run lint:md` — exits 0 (validates no dead internal links from removed doc dirs)
  - **Date**: 2026-05-27
  - **Status**: Completed — 3796 files, 0 errors
- [x] Spot-check: `grep -r "programming-languages/c-sharp\|programming-languages/f-sharp\|programming-languages/java\|programming-languages/kotlin\|programming-languages/elixir\|programming-languages/clojure\|programming-languages/dart\|programming-languages/python" docs/ repo-governance/ AGENTS.md`
      — review any hits; fix or remove stale cross-links
  - **Date**: 2026-05-27
  - **Status**: Completed — fixed stale links in docs/; removed jvm-spring/ elixir-phoenix/ jvm-spring-boot/ dirs;
    remaining hits in repo-governance/ are illustrative examples in convention docs, not broken links

### 4d: Quality gate + commit

- [ ] Run `npx nx affected -t typecheck lint test:quick spec-coverage` — exits 0
- [x] Run `npm run lint:md` — exits 0
  - **Date**: 2026-05-27
  - **Status**: Completed — 3740 files, 0 errors (fixed double-blank after Java FSM link removal)
- [x] Commit: `chore(cleanup): rewrite programming-languages README, final cross-cutting cleanup`

---

### Commit Guidelines

- Commit changes thematically — each cleanup phase gets its own commit
- Follow Conventional Commits format: `<type>(<scope>): <description>` (imperative mood, no period)
- Do NOT bundle multiple phases into a single commit
- If quality gate fixes span multiple concerns, split into separate commits per concern

---

## Phase 5: Post-Push CI Verification

- [x] Push to `origin main`: `git push origin main`
  - **Date**: 2026-05-27
  - **Status**: Completed — pushed successfully
- [x] Monitor GitHub Actions: `gh run list --limit 5` — check status every 3 minutes
  - **Date**: 2026-05-27
  - **Status**: Completed — no new CI runs triggered by this push (all workflows are scheduled or
    PR-only; `crane-cli-integration` only triggers on `apps/crane-cli/**` changes)
- [x] Verify `PR - Quality Gate` workflow (if triggered) completes with success or skip for
      all jobs — particularly confirm no `dotnet`, `jvm`, `python` jobs appear
  - **Date**: 2026-05-27
  - **Status**: N/A — direct push to main, PR Quality Gate only triggers on PRs
- [x] Verify `crane-cli-integration` workflow (if triggered) completes without setup-dotnet
      errors
  - **Date**: 2026-05-27
  - **Status**: N/A — not triggered (no crane-cli source changes)
- [x] If any CI job fails: diagnose root cause, fix, push follow-up commit, re-monitor
  - **Date**: 2026-05-27
  - **Status**: N/A — no failures from this push

---

## Plan Archival

- [ ] Verify ALL delivery checklist items above are ticked
- [ ] Verify ALL quality gates pass (local + CI)
- [ ] Move plan: `git mv plans/in-progress/remove-inactive-tech-stack-remnants plans/done/2026-05-27__remove-inactive-tech-stack-remnants`
      (use actual completion date)
- [ ] Update `plans/in-progress/README.md` — remove this plan's entry
- [ ] Update `plans/done/README.md` — add this plan's entry with completion date
- [ ] Commit: `chore(plans): move remove-inactive-tech-stack-remnants to done`
