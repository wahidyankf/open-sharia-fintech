---
title: SDLC Gate Standard
description: Target standard for gate mechanics across ose-public and ose-private — identical check set, order, and invocation mechanism; only project/app set diverges
category: reference
tags:
  - sdlc
  - gates
  - quality
  - ci
  - hooks
created: 2026-06-30
---

# SDLC Gate Standard

> Source of truth: [`tech-docs.md`](../../plans/done/2026-07-01__standardize-rhino-cli-sdlc-parity/tech-docs.md)

This document defines the target standard for SDLC gate mechanics across the two bound OSE
repositories: `ose-public` and `ose-private`. **Identical gate mechanics** means the
same check set, the same order, and the same invocation mechanism across the bound repos. The only sanctioned variation
is the project/app set (and therefore the per-app deploy/CRON workflows and language-specific gate
jobs). See [Divergence Policy](#divergence-policy) for the exact boundary.

## Lifecycle Stages

This section is the single normative reference for what runs, in what order, at every SDLC stage.
The registry projects the command list for each surface; use `rhino-cli gate list --surface=<surface>`
rather than copying it into this reference. Each stage names the surface file and trigger.

| Stage              | Surface                                 | Trigger                       |
| ------------------ | --------------------------------------- | ----------------------------- |
| 1. pre-commit      | `.husky/pre-commit`                     | `git commit` (before message) |
| 2. commit-msg      | `.husky/commit-msg`                     | `git commit` (on the message) |
| 3. pre-push        | `.husky/pre-push`                       | `git push`                    |
| 4. PR quality gate | `.github/workflows/pr-quality-gate.yml` | pull request (+ branch push)  |

A standalone `validate-env.yml` workflow runs on `pull_request` and `push:main` in parallel with the
PR gate. No CRON pipeline is part of the gate set; `test:integration`, `test:e2e`, and
`deps:audit` (all uncacheable or heavy) run only in scheduled CRON pipelines, never in any gate.

### Command Scope

Every command carries exactly one of four controlled scope values:

- **affected file-type** — files matching a glob, limited to the changed set (staged at pre-commit;
  `--diff` at PR). For example: lint-staged formatters, tool-lint, per-file markdown validators.
- **all file-type** — files matching a glob across the whole repository. For example: `md links
validate` and `env validate`.
- **affected projects** — the touched Nx project graph (`nx affected`); per affected project only. For
  example: `test:quick`, structural specs at pre-push and PR.
- **other** — not file-type or project scoped: the commit-message text, binding regeneration from the
  whole `.claude/` tree, the path-gated governance validators, and the `detect`/`quality-gate` CI
  plumbing.

The same check moves only along this scope axis between local and CI surfaces. For example,
file-scoped checks are staged locally and recomputed from the PR or push change set in CI.

### Gate Composition Rule

One identity, one formatter verification rule, and one exclusion govern every stage:

1. **`(pre-commit ∪ pre-push) == PR gate`** — every check declared on a local hook surface reaches
   the PR/push gate. The registry is normative: CI derives matrix-wired checks from
   `gate list --surface=ci --format=json`, while declared hand-wired checks retain their setup jobs.

2. **Every formatter mutation has one CI verifier.** The local mutation auto-fixes where permitted;
   the linked `format-verify-*` check independently fails on unformatted pushed code.

3. **Heavy/uncacheable tiers never run in any gate.**
   `test:integration`, `test:e2e`, and `deps:audit` are CRON-only, never in any gate.

**Gate rule summary**: `(pre-commit ∪ pre-push) == PR gate` — the registry-defined check set reaches
the PR and push-to-main gate. `test:integration`, `test:e2e`, and `deps:audit` run only in
scheduled CRON pipelines, never in any gate.

Independent checks run in parallel within every stage: CI gates run as parallel GitHub Actions jobs;
local hooks run the per-project `nx affected` leg concurrently with the repo-wide validators
(`md links validate`, `env validate`, governance). Ordering only matters where a real data dependency
exists.

### Stage 1: pre-commit

`.husky/pre-commit`, in this exact order; stops at first failure:

| #   | Command                                                         | Scope              | What it does                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --- | --------------------------------------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | `apps/rhino-cli/scripts/rhino-bin.sh env staged-guard validate` | affected file-type | Aborts the commit if any real `.env*` file is staged (the one exception is `.env.example`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 2   | `lint-staged`                                                   | affected file-type | Dispatches by extension over only the staged files: **format** (rewrite-in-place, re-stage; never fails on style), **tool-lint** (fail on findings) — `*.sh`→`shellcheck --severity=warning`, `Dockerfile`/`*.Dockerfile`→`hadolint --failure-threshold warning`, `.github/workflows/*.{yml,yaml}`→`actionlint` — and the **per-file markdown validators** (fail on findings): `*.md`→`markdownlint-cli2` and `apps/rhino-cli/scripts/rhino-bin.sh md mermaid validate` and `apps/rhino-cli/scripts/rhino-bin.sh md heading-hierarchy validate` and `apps/rhino-cli/scripts/rhino-bin.sh md naming validate` and `apps/rhino-cli/scripts/rhino-bin.sh md frontmatter validate`; forbidden-type globs (`*.{json,yml,yaml,toml}` + source)→`apps/rhino-cli/scripts/rhino-bin.sh convention emoji validate`; `docker-compose*.{yml,yaml}`→`docker compose -f <file> config`; `*.feature`→`apps/rhino-cli/scripts/rhino-bin.sh specs gherkin-cardinality validate`. **`md links validate`, `md readme-index validate`, and `harness duplication validate` are not here** — they are cross-file validators (pre-push/PR/main, repo-wide). |
| 3   | `apps/rhino-cli/scripts/rhino-bin.sh harness bindings generate` | other              | Regenerates the platform-binding artifacts (`.opencode/`, `.amazonq/`) from the `.claude/` source of truth and auto-stages them so generated files commit in lockstep.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 4   | (lockfile-sync hook step)                                       | affected file-type | Regenerates and re-stages `package-lock.json` for any app whose `package.json` is staged (reproducible-envs guardrail).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |

Pre-commit is the fast stage — it does not run `test:quick`. Per-project `typecheck`/`lint`/`test:unit`
run at pre-push via `test:quick`, never here.

The tool-linters (`shellcheck`/`hadolint`/`actionlint`) are pure file-type dispatch — exactly what
lint-staged already does for formatters — so they are lint-staged entries, not `nx run` targets. They
stay tool-gated (skip-with-hint when the linter is absent locally — CI is the hard gate).

The `./scripts/git-identity-check.sh` script is removed and replaced by the Git Identity Guardrail: a
behavioral rule, not a mechanical gate. **No AI agent may set or modify git user identity
(`user.name`/`user.email`) at any scope.** Specifically, an agent must not run
`git config --local user.name`/`user.email`, the bare `git config user.name`/`user.email` (which
writes to the local repo config by default inside a worktree), `--global`/`--system` identity, or
edit a `[user]` section in `.git/config`. Commit identity always comes from the developer's own global
config (`~/.gitconfig`, optionally via `includeIf "gitdir:…"` for per-tree identities). This mirrors
the [no-real-.env agent guardrail](../../repo-governance/conventions/security/secrets-and-env-standards.md).
This rule governs interactive agents working in a developer's repo/worktree — it does not forbid a CI
workflow from configuring a service-account/bot identity in its own YAML (for example, the
`github-actions[bot]` identity used by the PR-gate format-commit-back).

### Stage 2: commit-msg

`.husky/commit-msg`. Identical in both bound repos:

| #   | Command                              | Scope | What it does                                                                                                                          |
| --- | ------------------------------------ | ----- | ------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `npx --no -- commitlint --edit "$1"` | other | Validates the commit message against Conventional Commits (`@commitlint/config-conventional`) — scope is the message text, not files. |

### Stage 3: pre-push

`.husky/pre-push`, in this exact order; stops at first failure:

| #   | Command                                                                         | Scope              | What it does                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| --- | ------------------------------------------------------------------------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `nx affected -t test:quick`                                                     | affected projects  | Runs typecheck → lint → test:unit → test:coverage (≥90%) → test:specs (all `specs:*` validators) per affected project. Projects with a real `compat:min-version` (Rust, Python) also run `nx affected -t compat:min-version` (cacheable). `deps:audit` is not here — it is uncacheable (network advisory DB) and runs CRON-only.                                                                                                                                                                    |
| 2   | `apps/rhino-cli/scripts/rhino-bin.sh md links validate --exclude plans/done`    | all file-type      | The cross-file markdown validator — relative paths and `#fragment` anchors resolve repo-wide. Repo-wide (not lint-staged) because adding, deleting, or renaming any markdown file can break links in untouched files.                                                                                                                                                                                                                                                                               |
| 3   | `apps/rhino-cli/scripts/rhino-bin.sh env validate`                              | all file-type      | Validates each app's `.env.example` against the repo env contract.                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 4   | `apps/rhino-cli/scripts/rhino-bin.sh harness naming validate`                   | other (path-gated) | Agent/skill filenames match the harness naming convention. **Trigger:** `.claude/agents/` or `.opencode/agents/`.                                                                                                                                                                                                                                                                                                                                                                                   |
| 5   | `apps/rhino-cli/scripts/rhino-bin.sh repo-governance workflows naming validate` | other (path-gated) | Workflow-doc filenames match the workflow naming convention. **Trigger:** `repo-governance/workflows/`.                                                                                                                                                                                                                                                                                                                                                                                             |
| 6   | `apps/rhino-cli/scripts/rhino-bin.sh repo-governance vendor validate`           | other (path-gated) | Governance docs and the canonical root instruction surface stay vendor-neutral, no vendor leakage. Two gate entries, one path each (the validator takes a single positional path). **Trigger:** `repo-governance/**.md`; `AGENTS.md`. `CLAUDE.md` is exempt by design — its Platform Binding Examples heading covers the whole body.                                                                                                                                                                |
| 7   | `apps/rhino-cli/scripts/rhino-bin.sh harness bindings validate`                 | other (path-gated) | All-harness binding parity across all 11 harnesses listed in `repo-config.yml` `harness:`: generated-tier byte-parity (`.claude/` → `.opencode/`, `.amazonq/`), native-tier catalog coverage and no-shadowing, and color/tier translation-map coverage (absorbed from the former `cross-vendor:parity-validation` gate). **Trigger:** binding or parity surfaces — agents, `AGENTS.md`, `CLAUDE.md`, `repo-governance/**.md`, native-tier shadow files.                                             |
| 8   | `apps/rhino-cli/scripts/rhino-bin.sh governance word-budget validate`           | other (path-gated) | Auto-loaded instruction files stay within their per-surface word budget. Surfaces declared explicitly in `repo-config.yml` `governance-word-budget:` (no registry-merge). Covers: `repo-governance/**/*.md`, `AGENTS.md`, `CLAUDE.md`, `.claude/**/*.md`, `.cursor/**/*.md`, `.codex/**/*.md`, `.opencode/**/*.md`, `.pi/**/*.md`, `.amazonq/**/*.md`, `**/README.md`. Registered in the `gates:` registry and armed at pre-push and in CI. **Trigger:** any covered surface, or `repo-config.yml`. |

Each governance validator (rows 4–8) is path-gated — invoked only when its trigger path is in the
changed set. Row 8 is registered in the `gates:` registry and blocks pre-push and CI like the rest;
it also runs on demand and inside `repo-governance audit`.

The former separate specs-structural step is gone — all `specs:*` validators now run inside `test:quick`
(step 1) via `test:specs`, which runs in order:

| Nx target (in `test:specs`)  | rhino-cli command                                                      | Validates                                                                                                                                                                                              | Applies to                       |
| ---------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------- |
| `specs:structure-validation` | `apps/rhino-cli/scripts/rhino-bin.sh specs structure validate`         | The spec tree is structurally valid — merged adoption + tree + counts: the app/lib has adopted BDD (no orphan project), the canonical C4 tree exists, and each required subfolder holds ≥ 1 spec file. | Every project                    |
| `specs:behavior:coverage`    | `apps/rhino-cli/scripts/rhino-bin.sh specs behavior-coverage validate` | Every Gherkin step has a step definition, and every scenario outside `domain/**` is covered at exactly its required levels via explicit `@covers` markers.                                             | Every project                    |
| `specs:domain:coverage`      | `apps/rhino-cli/scripts/rhino-bin.sh specs domain-coverage validate`   | The same coverage model scoped to `domain/**` feature files only.                                                                                                                                      | Projects in `specs.domain-areas` |

(`specs:gherkin-cardinality-validation` is not in `test:specs` — it is a per-file `.feature` check
that runs in lint-staged at pre-commit. Spec-file link integrity is likewise not in `test:specs` — the
repo-wide `md links validate` gate already covers `specs/**.md`.)

### Stage 4: PR Quality Gate

`pr-quality-gate.yml`. Job skeleton identical across repos (only language-gate jobs and infra-only IaC
jobs differ). `$P` = `$(($(nproc)-1))`.

| Job                                                               | Exact command(s) CI runs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Scope              |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| detect                                                            | `nx show projects --affected --base=origin/main --head=HEAD --json` — derives the affected-language set that drives the `<lang>` matrix. Runs no test.                                                                                                                                                                                                                                                                                                                                                                                                                                      | other              |
| lint-staged                                                       | `lint-staged --diff="origin/main...HEAD"` — per changed file, in order: formatters (auto-fix + commit back to the PR branch, never fail), then fail-on-finding: `shellcheck --severity=warning` (`*.sh`) · `hadolint --failure-threshold warning` (`Dockerfile`/`*.Dockerfile`) · `actionlint` (`.github/workflows/*.{yml,yaml}`) · `markdownlint-cli2` + `apps/rhino-cli/scripts/rhino-bin.sh md mermaid validate` + `apps/rhino-cli/scripts/rhino-bin.sh md heading-hierarchy validate` (`*.md`) · `apps/rhino-cli/scripts/rhino-bin.sh specs gherkin-cardinality validate` (`*.feature`) | affected file-type |
| `<lang>` gate (one job per affected language)                     | `nx affected -t test:quick --base=origin/main --head=HEAD --parallel=$P` — each affected project runs typecheck → lint → test:unit → test:coverage (≥90% line) → test:specs. Projects with a real `compat:min-version` also: `nx affected -t compat:min-version --base=origin/main --head=HEAD --parallel=$P` (cacheable). No `format:check`, no `test:integration`, no `test:e2e`, no `deps:audit` (uncacheable → CRON-only).                                                                                                                                                              | affected projects  |
| md-links                                                          | `apps/rhino-cli/scripts/rhino-bin.sh md links validate --exclude plans/done` — repo-wide (NOT `--diff`: a deleted/renamed file breaks links in untouched files)                                                                                                                                                                                                                                                                                                                                                                                                                             | all file-type      |
| env                                                               | `apps/rhino-cli/scripts/rhino-bin.sh env validate`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | all file-type      |
| governance (each runs only if its trigger path is in the PR diff) | `apps/rhino-cli/scripts/rhino-bin.sh harness naming validate` · `apps/rhino-cli/scripts/rhino-bin.sh harness bindings validate` · `apps/rhino-cli/scripts/rhino-bin.sh repo-governance vendor validate` · `apps/rhino-cli/scripts/rhino-bin.sh repo-governance workflows naming validate`                                                                                                                                                                                                                                                                                                   | other (path-gated) |
| quality-gate                                                      | Sentinel join — `needs: [detect, lint-staged, <lang>…, md-links, env, governance]`; green only when every required job is green. Runs no command.                                                                                                                                                                                                                                                                                                                                                                                                                                           | other              |

All jobs run in parallel (matrix + independent jobs); `quality-gate` is the join point. No
`test:integration`/`test:e2e` — same fast set as pre-push, recomputed server-side and widened to cover
everything the two local hooks run.

## Target Standard

The gate-check standard is synthesized by picking the strongest wiring per surface, even where that
means changing `ose-public`. The named winner per surface:

| Surface                                                                                                 | Standard (winner)                                                                                                                                                                                                | Rationale                                                                                                                                                                                                                                                                                                              |
| ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **commit-msg**                                                                                          | `npx --no -- commitlint --edit "$1"` + `@commitlint/config-conventional`                                                                                                                                         | Already identical in both — lock it.                                                                                                                                                                                                                                                                                   |
| **Tool-lint (file-type, via lint-staged)**                                                              | shellcheck/hadolint/actionlint as lint-staged entries (both bound repos), run at commit (staged) + CI (`--diff`)                                                                                                 | Tool-linting is pure file-type dispatch — lint-staged already does this for formatters, so one mechanism covers both; no per-project Nx graph, and changed-files-only avoids the whole-repo glob tripping on stray `local-tmp/*.sh`; standalone `shell:lint`/`dockerfiles:lint`/`actions:lint` Nx targets are dropped. |
| **PR quality-gate filename**                                                                            | `pr-quality-gate.yml`                                                                                                                                                                                            | 2-of-3 already use it; "pr" is clearer than "commons" for the gate's role.                                                                                                                                                                                                                                             |
| **Markdown workflow filename**                                                                          | None — deleted in all 3                                                                                                                                                                                          | Markdown validation is folded into the gates (per-file md validators in the lint-staged job; `md links validate` as the `md-links` gate job) — `validate-markdown.yml`/`markdown-validate.yml` is removed everywhere.                                                                                                  |
| **Env workflow filename**                                                                               | `validate-env.yml` (standalone)                                                                                                                                                                                  | Infra style; the one check that keeps a standalone workflow (secrets-adjacent, parallels the env-staged-guard carve-out).                                                                                                                                                                                              |
| **Markdown validator set**                                                                              | Per-file (lint-staged): `markdownlint-cli2` + `md mermaid validate` + `md heading-hierarchy validate` + `specs gherkin-cardinality validate` (`.feature` only); cross-file (repo-wide gate): `md links validate` | All repos run the identical set; public must add gherkin-cardinality (`.feature` only — no markdown scanning). These live in the lint-staged set (per-file) and the repo-wide `md-links` gate job — the standalone `validate-markdown.yml` workflow is deleted (absorbed into the PR/main gates).                      |
| **specs-gate validator set (PR gate)**                                                                  | structure (merged adoption + tree + counts) + behavior:coverage (+ domain:coverage on `*-be`) + gherkin-cardinality (full); spec links via repo-wide `md links validate`                                         | Public's fuller set wins; a bound repo deferring any structural validator must promote it.                                                                                                                                                                                                                             |
| **pre-push scoped validator set**                                                                       | Union including `governance:vendor-audit-validation`                                                                                                                                                             | Both bound repos include it.                                                                                                                                                                                                                                                                                           |
| **Hook/gate step order**                                                                                | See [Lifecycle Stages](#lifecycle-stages)                                                                                                                                                                        | The normative registry-backed hook and PR-gate sequence is defined in the Lifecycle Stages section of this document.                                                                                                                                                                                                   |
| **CRON pipeline shape**                                                                                 | `*-test-local-deploy-{stag,prod}.yml` + paired `*-test-{stag}.yml` calling shared `_reusable-*` workflows                                                                                                        | Public's reusable-workflow factoring is cleanest; infra keeps its own app set but adopts the naming and reusable-call shape.                                                                                                                                                                                           |
| **rhino-cli source identity** (`src/`, `Cargo.toml`, `Cargo.lock`, `project.json`, `LICENSE`, `tests/`) | Byte-identical across both bound repos — zero carve-outs, canonical source carries the union command surface (repo-inapplicable verbs dormant, not absent)                                                       | A committed manifest gate enforces the hermetic boundary and the scheduled parity audit detects cross-repository drift.                                                                                                                                                                                                |
| **`repo-config.yml` schema parity**                                                                     | `rhino-cli repo-config validate` — strict-deserialize schema check (deny-unknown-fields + required/enum checks), wired at pre-commit (staged-gated fast path) and the PR quality gate                            | Converts the "identical key set across `repo-config.yml`" boundary from prose review into an enforced, automated gate.                                                                                                                                                                                                 |

## Divergence Policy

Per the identical-result invariant, the standardization layer is identical across both bound repos. The
only sanctioned variation is what each repo actually ships (its project/app set) and the data that
follows from it. Everything in "Drift" below must converge to one form.

### rhino-cli Byte-Identity Boundary

`apps/rhino-cli` is held to a stricter, second-pass target beyond the gate mechanics above: **zero
carve-outs**. `apps/rhino-cli`'s `src/`, `Cargo.toml`, `Cargo.lock`, `project.json`, `LICENSE`, and
`tests/`, plus
the Gherkin behavior tree at `specs/apps/rhino/behavior/rhino-cli/gherkin/**` (every `.feature` file and
every `README.md`), are byte-identical across `ose-public` and `ose-private`. The
canonical source carries the
**union command surface** — every repo's `rhino-cli` binary exposes the full command superset, and a
command with no applicable projects in a given repo (for example, `java` in `ose-public`) is
**dormant, not absent**, rather than removed from the binary. A **schema-parity gate**
(`rhino-cli repo-config validate`, run at pre-commit (staged-gated) and the PR quality gate in every
repo) enforces
that each repo's `repo-config.yml` carries an **identical key set** — values may differ per repo, but
no repo may add an unknown key or omit a required one, so the byte-identical source can never
silently drift out of sync with the data it reads.

Within `apps/rhino-cli` itself, the only sanctioned divergence anywhere is:

1. **Each repo's app/language set** — the data `repo-config.yml` carries per repo (domain-areas,
   ddd-areas, env-validation scan paths) differs, driving which of the union's dormant commands are
   actually exercised in that repo.
2. **The CI runner label** (for example, `ose-private`'s `[self-hosted, linux, ose-self-hosted]`) — a
   CI-workflow-YAML concern that lives outside `apps/rhino-cli` entirely, so it never affects source
   byte-identity.

See [tech-docs.md §4 "rhino-cli Source-Identity Standard"](../../plans/done/2026-07-03__unify-rhino-cli-sdlc-parity/tech-docs.md#4-rhino-cli-source-identity-standard)
for the full synthesis approach and acceptance criteria.

**Known exception (tracked, not yet reconciled): `doctor/tools.rs` tool-provisioning extensions.**
`ose-private` legitimately needs IaC tool provisioning (the same infra-only IaC surface named under
[Allowed Divergence](#allowed-divergence) below) that the other bound repos do not, and its
`doctor/tools.rs` was originally observed to carry extra tool-definition and test entries beyond the
canonical set as a result. **Re-measured 2026-08-07** (see the linked brief's "Live re-measurement"
section): as of that measurement the two files' `fn`-signature sets and `DOCTOR_TOOL_INVENTORY` are
identical, and the file's entire diff is a separately-tracked, unpropagated fix (task #238) — not an
extra-tool-definition surplus. The structural tension this note describes may still be real in
principle, but the specific divergence that motivated writing it down is not currently observable; do
not treat this note alone as evidence of present drift. The "zero carve-outs" target above is stated
as the goal for the whole `src/` tree; this one file has a structural tension with that goal that
predates and is independent of this document's propagation work — the byte-identity boundary either
needs a narrower `BOUNDARY_PATHS` carve-out for this file, or the parity check needs an
accepted-superset comparison mode (canonical subset + declared per-repo extensions) instead of a
literal full-file match. Until one of those lands as a code change, treat drift reports naming only
`doctor/tools.rs`'s known IaC-tooling additions as this tracked exception, not as a new propagation
gap — but still diff the file in full on every byte-identity check, since a new, unrelated drift can
hide alongside the known one. Tracked as a follow-up idea brief:
[`rhino-cli-tools-superset-carveout`](../../plans/ideas/q2-not-urgent-important/rhino-cli-tools-superset-carveout.md).

### Allowed Divergence

The following variations are not flagged as drift:

- **App set and per-app deploy CRONs** — `ose-public` ships content/web apps (`ose-www`,
  `ayokoding-www`, `organiclever-www`, `wahidyankf-www`, `*-app-web`, `*-be`); `ose-private` ships
  `coralpolyp`. Each repo keeps only the deploy CRON workflows for apps it actually ships, and both
  repos' deploy CRONs push to real Vercel/self-hosted environments.
- **Language gate jobs** — the PR gate's per-language jobs (golang, jvm, dotnet, python, rust, elixir,
  clojure, dart, typescript) exist only for languages present in that repo.
- **Infra-only IaC gates** — `terraform fmt`/`validate`/`tflint`, `ansible-lint`, `yamllint` exist
  only in `ose-private`, in both hooks and the PR gate.
- **Self-hosted runner labels** — `ose-private` runs on `[self-hosted, linux, ose-self-hosted]`.
- **lint-staged formatter entries** — only for languages present (for example `*.go`, `*.{ex,exs}`
  exist where that language ships). The common entries (`*.md`, `*.json`, `*.{yml,yaml}`,
  `*.{css,scss}`, `*.rs`, `*.fs`) must match across all repos.
- **Gate-entry data** — each repository declares only the formatter and language entries supported by
  its tracked files, but every declared hook or CI command must be an entry in its own gate registry.

### Drift

The following must converge — this is the work of the standardization plan:

- Workflow **filenames** for the shared gates (PR gate, markdown, env).
- The **validator set** inside the markdown workflow and the specs-gate.
- The **invocation mechanism** for shell/docker/actions lint (inline shell vs. lint-staged file-type
  entry).
- The **pre-push scoped validator set** (governance vendor audit presence).
- The **job skeleton/names** in the PR gate (detect, markdown, naming, env, specs-gate, quality-gate
  sentinel; formatting is lint-staged at commit, not a gate job).
- The **placement** of env validation (standalone workflow vs. folded into the PR gate).
- The **Nx target names** invoked by hooks/CI, and the rhino-cli target set itself: `fmt`/`format:check`
  targets (removed — formatting via lint-staged), shell/docker/actions tool-lint (folded into
  lint-staged, not Nx targets), the env/governance/binding validators run as direct `rhino-bin.sh` calls
  in gates (not `nx run rhino-cli:` targets).

## Parity Status

> **Scope note (2026-08-16)**: the table below is a dated snapshot of a run that still included
> `ose-primer`. That repo has since been removed from the bound set and carries **no sync
> obligation** — see [Related Repositories §Repositories outside the parity set](./related-repositories.md#repositories-outside-the-parity-set).
> Rows naming primer are historical record only; no row below obligates any future work against it.

Verified 2026-07-01 across `ose-public`, `ose-primer`, `ose-private` by directly running the acceptance
command for every mechanics row (not by inspecting config alone; corrected same-day after a follow-up
audit found two rows below were marked ✅ while infra's pre-commit still ran `test:quick` in the wrong
stage via a legacy monolith that bypassed lint-staged — both fixed before this table's final pass). ✅ =
byte/behavior-identical across all three; ⚠️ = tracked, non-blocking divergence with a linked follow-up;
allowed-divergence rows (app set, language gates, infra-only IaC, runner labels, lint-staged formatter
entries) are excluded per [Divergence Policy](#divergence-policy).

| Mechanics row                                                                                         | Status | Note                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ----------------------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PR-gate / markdown / env workflow filenames                                                           | ✅     | `pr-quality-gate.yml`, `validate-env.yml` in all 3; no standalone markdown workflow anywhere.                                                                                                                                                                                                                                                                                                                                                                             |
| Markdown validator set (per-file + repo-wide)                                                         | ✅     | markdownlint-cli2 + mermaid + heading-hierarchy + naming + frontmatter (lint-staged); `md links validate` (repo-wide gate).                                                                                                                                                                                                                                                                                                                                               |
| lint-staged full set (emoji, gherkin-cardinality, docker-compose)                                     | ✅     | Identical entries in all 3 `package.json` (only per-language formatter entries differ, an allowed divergence).                                                                                                                                                                                                                                                                                                                                                            |
| Repo-wide cross-file pre-push gates (md-links, readme-index, harness-duplication, convention-license) | ✅     | All 4 present as direct `cargo run` calls in all 3 repos' `.husky/pre-push` + both CI gates, accurate as of this row's 2026-07-01 verification pass (see the 2026-08-09 dispatch-mechanism note below the table for the current state).                                                                                                                                                                                                                                   |
| specs-gate set (structure + behavior-coverage + domain-coverage + gherkin-cardinality)                | ✅     | Identical job/target composition in all 3.                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Lint invocation mechanism (lint-staged, no bare tool-lint Nx targets)                                 | ✅     | Confirmed in all 3; infra's D9 Terraform/Ansible/YAML lint is a documented allowed IaC-only addition.                                                                                                                                                                                                                                                                                                                                                                     |
| Pre-push governance-vendor presence                                                                   | ✅     | Path-gated in all 3.                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Hook/gate step order                                                                                  | ✅     | Canonical 4-step pre-commit order (env-guard→lint-staged→bindings-generate→lockfile-sync) and pre-push order match [Lifecycle Stages](#lifecycle-stages) in all 3. infra's step-1 env-guard now runs the same `env staged-guard validate` Rust command as public/primer (the former bash-script mechanism divergence and legacy pre-commit-monolith `test:quick` misplacement are both fixed).                                                                            |
| rhino-cli target-key set                                                                              | ✅     | 21 identical sorted keys in all 3 `apps/rhino-cli/project.json` (verified via `jq -r '.targets\|keys[]'\|sort`, byte-diff clean).                                                                                                                                                                                                                                                                                                                                         |
| rhino-cli command set, verb-last                                                                      | ✅     | `specs counts validate` and the `behavior-coverage`/`domain-coverage` verbs are now identical in all 3; infra's former standalone `bc`/`ul` leaves (already-duplicate logic vs. `structure validate`) are removed.                                                                                                                                                                                                                                                        |
| `repo-config.yml` section schema                                                                      | ✅     | 6 identical top-level sections (`harness`, `coverage`, `specs`, `instruction-size`, `env-contract`, `env-injection`) in all 3, accurate as of this row's 2026-07-01 verification pass (see the 2026-08-13 schema-rename note below the table for the current state).                                                                                                                                                                                                      |
| Mandatory targets on every project                                                                    | ✅     | `typecheck`/`lint`/`test:unit`/`test:integration`/`test:e2e`/`test:quick` present on every project in all 3 (0 `MISSING` in the jq sweep).                                                                                                                                                                                                                                                                                                                                |
| `test:quick` composition (typecheck→lint→test:unit→test:coverage→test:specs)                          | ✅     | Identical 5-step sequential composition; F#/C# projects additionally carry `dependsOn: [typecheck, lint]` to prevent an MSBuild concurrent-build race.                                                                                                                                                                                                                                                                                                                    |
| Native `test:coverage` ≥ 90% line, no `test-coverage` target, no Codecov                              | ✅     | Confirmed absent everywhere (`grep -ri codecov` returns only `ExcludeFromCodeCoverage`); native coverage present on every real-`test:unit` project.                                                                                                                                                                                                                                                                                                                       |
| `format` via file-type lint-staged, no per-project `format` target                                    | ✅     | Confirmed in all 3.                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| pre-push ≡ PR quality gate runs only `test:quick`                                                     | ✅     | `test:integration`/`test:e2e` never appear in any gate surface; CRON-only.                                                                                                                                                                                                                                                                                                                                                                                                |
| Per-level `@covers` coverage model                                                                    | ⚠️     | Structurally present (target names, `coverage.projects` registry) in all 3. Content maturity varies: some primer projects still carry echo-stubbed `specs:behavior:coverage` pending real `@covers` tagging; infra's `coralpolyp-be` `specs:domain:coverage` is an echo placeholder pending a real `domain/**` split; the CLI's dedicated domain-scoping engine is unwired (routes to the same engine as behavior-coverage everywhere). Tracked separately, non-blocking. |
| Canonical CI workflow names present                                                                   | ✅     | `pr-quality-gate.yml` and `validate-env.yml` in every bound repository; CI matrix entries derive from the gate registry.                                                                                                                                                                                                                                                                                                                                                  |
| Worktree-agnostic guardrails                                                                          | ✅     | Verified from both the primary checkout and a linked worktree in all 3 (infra's bare-repo-only layout is the hard case — confirmed via its actual daily worktree execution, not a throwaway check).                                                                                                                                                                                                                                                                       |
| specs/ C4 structure (every app + every lib)                                                           | ✅     | Every spec area across all 3 repos has `product/`, `system-context/`, `containers/`, `components/`, `behavior/gherkin/` — including all app-level libs (4 in public, 7 in primer, 2 in infra) that were missing this structure entirely before this pass.                                                                                                                                                                                                                 |

All CI runs for the final commit on each repo's `main` are green (a transient jar-download flake on
one `ose-public` run was confirmed via a clean re-run with zero code changes).

**Dispatch-mechanism note (2026-08-09, not part of the 2026-07-01 verification pass above)**: the
release-build `cargo run` dispatch (via `apps/rhino-cli/Cargo.toml`) cited by the
"Repo-wide cross-file pre-push gates" row was superseded in `ose-public` by the
`apps/rhino-cli/scripts/rhino-bin.sh` resolver shim created in this repo's `optimize-cis` PR
(`apps/rhino-cli/scripts/rhino-bin.sh`, added 2026-08-09). This note records the mechanism change
without re-dating the table above, which remains a historical snapshot of the 2026-07-01
cross-repo run; `ose-private` propagation of the shim is tracked separately (see
AC-15 in `plans/done/2026-08-09__optimize-cis/delivery.md`).

**Schema-rename note (2026-08-13, not part of the 2026-07-01 verification pass above)**: the
`repo-config.yml` `instruction-size:` top-level section cited by the "`repo-config.yml` section
schema" row was renamed to `governance-word-budget:` in `ose-public` by this repo's
`optimize-governance-md` plan (Phase 1b). This note records the rename without re-dating the table
above, which remains a historical snapshot of the 2026-07-01 cross-repo run and is accurate for
that date — `instruction-size:` is still the live section name in `ose-private` as of this note. The
rename opens a cross-repo parity obligation (a `repo-config.yml` schema-section rename is exactly the
class of change the [Parity Status](#parity-status) table exists to track); propagation to
`ose-private` is not yet scheduled against a specific plan at the time of this note.
