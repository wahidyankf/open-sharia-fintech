# `nx affected` Silently Skips rhino-cli Rust Changes in ose-public

One-line summary: in `ose-public` only, `nx affected` fails to detect changes confined to
`apps/rhino-cli/src/**/*.rs`, so the `.husky/pre-push` gate silently skips rhino-cli-only commits.

> Demoted from a full five-document plan folder to a two-pager on 2026-08-05. The full plan carried
> `README.md`, `brd.md`, `prd.md`, `tech-docs.md`, and a two-phase `delivery.md` (root-cause phase
> plus fix phase, each with its own gate). Root cause was never found, so the material here is an
> investigation brief rather than an executable plan.
> Relocated from ose-private/plans/ideas/ose-public-nx-affected-rhino-cli-gap.md on 2026-08-06 by plan-ideas-grooming.

## Problem / context

In `ose-public`, a commit whose only changed file was `apps/rhino-cli/src/application/docs/naming.rs`
produced "No tasks were run" from `npx nx affected -t lint`, from the same command with
`--base=HEAD~1`, and again after `npx nx reset` cleared the cache. `npx nx show projects --affected
--verbose` returned empty for that commit. Yet `npx nx show projects` lists `rhino-cli`, and
`npx nx run rhino-cli:lint` runs and passes correctly — so the project exists and its targets work;
only affected-detection misses it. The same silent skip was observed during a real `git push` in
`ose-public`, which means `.husky/pre-push`'s own `npx nx affected -t test:quick` invocation
reproduces the gap in normal use, not only under manual testing. The behavior is specific to
`ose-public`: `ose-primer` and `ose-private` both detect rhino-cli changes through `nx affected`
correctly. One candidate has already been ruled out — the missing `root` key in
`apps/rhino-cli/project.json` is absent identically in all three repos, so it cannot explain a
divergence that appears in only one of them.

## Why now

`ose-public` is the upstream source of truth for the `apps/rhino-cli` byte-identity boundary spanning
`ose-public`, `ose-primer`, and `ose-private`. A silent test-coverage hole sits in exactly the repo
whose rhino-cli copy the other two mirror: a breaking rhino-cli change can clear pre-push in
`ose-public` even though the equivalent change would be caught in either sibling. The workaround —
invoking `nx run rhino-cli:<target>` by explicit project name — works, but it depends on a human or
agent already knowing that `nx affected` lied, and nothing warns them.

## Prior art / precedents

- [rhino-cli-sync-validator-wrong-model-drift](./rhino-cli-sync-validator-wrong-model-drift.md)
  — the other open rhino-cli cross-repo defect, tracked separately and explicitly out of scope here.
- [2026-07-29 rename-ose-infra-to-ose-private learnings](https://github.com/wahidyankf/ose-private/blob/main/plans/done/2026-07-29__rename-ose-infra-to-ose-private/learnings.md)
  — the Knowledge Capture entry this item was filed from, where the gap was first hit.
- [standardize-cis](./standardize-cis.md) — the standing audit for CI-standardization residue left by
  the toolchain-parity work; a one-repo-only config divergence is precisely that residue's shape.
- `nx graph --file=graph.json` — Nx's own project-graph dump, the direct instrument for confirming
  whether `rhino-cli` appears as a node with correct `inputs`/`implicitDependencies` wiring.
- `.husky/pre-push` in `ose-public` — the existing gate this defect weakens; whatever fix lands must
  keep working through this hook unchanged.

## Proposed direction (sketch)

Treat this as a genuine investigation, not a known fix waiting to be typed. Diff the Nx surface
across the three repos and look for the `ose-public`-only difference: `nx.json` `namedInputs`,
`implicitDependencies`, and plugin configuration; the presence of an `.nxignore` or an
`ignoredFiles`-style exclusion absent in the siblings; a `workspaceLayout` or project-graph filter
that omits `apps/rhino-cli`; and the installed `nx` / `@nx/*` versions (`npm ls nx`, lockfile diff),
since a version-specific bug is plausible if `ose-public`'s toolchain has drifted. Then dump
`nx graph --file=graph.json` in both `ose-public` and `ose-primer` and compare the `rhino-cli` node
directly. Once the difference is identified, fix it in `ose-public` alone. If the root cause turns
out to be an upstream Nx bug rather than local configuration, fall back to a pre-push mechanism that
does not depend on the broken detection.

## Rough scope & non-goals

In scope: root-causing why `nx affected` misses `apps/rhino-cli/src/**/*.rs` changes in `ose-public`
specifically, and fixing the underlying gap so the existing `.husky/pre-push` invocation reliably
covers rhino-cli-only commits without a manual workaround.

Out of scope: the `sync_validator.rs` byte-identity drift, which is tracked separately; and any
change to `ose-primer`'s or `ose-private`'s Nx configuration, since both already detect rhino-cli
changes correctly and are unaffected by this gap.

## Risks & open questions

- What is the actual root cause? Every named candidate is still a hypothesis; the only thing
  eliminated is the missing `project.json` `root` key. (open)
- Is this local configuration drift or an upstream Nx / plugin bug? The answer decides whether the
  fix is a config edit or a mechanism replacement. (open)
- Does the gap extend beyond `apps/rhino-cli` — are other `ose-public` projects also silently
  invisible to `nx affected`, and has anything already shipped through the hole? (open)
- Any fix risks regressing affected-detection for other projects, so the change needs spot-checking
  against several recent multi-project commits, not just the rhino-cli case.
- The investigation list itself is expected to grow before it converges; a fast answer should not be
  assumed.

## What success looks like + promotion signal

Success: a commit touching only `apps/rhino-cli/src/**/*.rs` in `ose-public` is listed by
`nx show projects --affected --verbose`, and `nx affected` runs `lint`, `typecheck`, and `test:quick`
for it without anyone reaching for `nx run rhino-cli:<target>` — with no other project's
affected-detection regressed and CI green. Promotion signal: re-promote to a `backlog/` plan as soon
as one concrete root-cause candidate is confirmed by a reproducible diff — a named `ose-public`-only
difference in `nx.json`, `.nxignore`, the graph dump, or the installed Nx version — because at that
point the work becomes a scoped fix with a verifiable acceptance test rather than an open hunt.
