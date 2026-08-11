---
title: "Secrets and Environment-Variable Standards"
description: "The authoritative hub for how this repository handles secrets and environment variables — naming convention, layout, annotation format, startup validation, tooling (rhino-cli env family), tiered injection standard (env-injection: section in repo-config.yml), storage tiers, and the env-contract drift guard."
category: explanation
subcategory: conventions
tags:
  - security
  - secrets
  - env-files
  - guard-env-file-access
  - naming
  - reproducibility
created: 2026-06-10
---

# Secrets and Environment-Variable Standards

This document is the single authoritative reference for how this repository handles secrets and
environment variables. The three prior docs that covered overlapping ground now redirect here:

- [`no-secrets-in-committed-files.md`](./no-secrets-in-committed-files.md) — hard iron rule stub
- [`env-file-access.md`](./env-file-access.md) — `guard-env-file-access` policy stub
- [`reproducible-environments.md`](../../../repo-governance/development/workflow/reproducible-environments.md) — `.env.example` pattern stub

## Principles Implemented/Respected

- **[Reproducibility First](../../principles/software-engineering/reproducibility.md)**: Env templates
  (`*.env.example`) are committed; real values stay in gitignored files. A checkout is reproducible
  by design — no credential is bundled.
- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: Every
  env var is declared by name, class, and type in `.env.example`; startup validators fail fast when a
  required var is absent.
- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**: The
  `rhino-cli env` toolchain (backup, restore, init, validate) and the `env-contract:` section in
  `repo-config.yml` eliminate manual cross-checking between templates and code.
- **[Root Cause Orientation](../../principles/general/root-cause-orientation.md)**: The drift guard
  (`env validate`) catches mismatches at the source, not in production. The hard no-secrets rule
  prevents exposure at the origin — not just after-the-fact scrubbing.
- **[Documentation First](../../principles/content/documentation-first.md)**: Every rule is codified
  here so it is discoverable and binding regardless of which agent platform or human performs the work.

## 1. Hard Iron Rule — No Secrets in Committed Files

**No system secret may enter any git-tracked file in this repository.**

System secrets include: SSH/private keys, passwords, API tokens, privileged usernames, certificates,
connection strings, and any value that grants access to a system or service.

Git history is permanent and distributed. A secret committed once lives in every clone, fork, mirror,
and backup, and removing it requires a destructive history rewrite that never fully guarantees the
secret was not already harvested. The only safe posture is prevention.

Real secret values go in:

- Uncommitted `.env*` files (e.g. `.env.local`, `.env`) — gitignored globally
- Files under `.secrets/` — gitignored globally
- `secrets.json` at repo root — gitignored globally

See also: [`no-secrets-in-committed-files.md`](./no-secrets-in-committed-files.md)

### Cross-repo doc canonicalization

The cross-repo canonical name for this rule is `no-secrets-in-committed-files.md` (aligned with the
ose-private sibling). This repository previously used `no-secrets-in-git.md`; the file was renamed by
the `standardize-secrets-and-env` plan to match the canonical name.

### Secret-Exposure History Remediation

A suspected or confirmed secret in committed history is a security incident. Do not treat deleting a
file in a later commit, redacting a PR comment, or closing the PR as remediation: the secret remains
reachable in Git history and can remain visible in the PR diff.

Execute this procedure automatically under the repository's standing incident policy. Do not expose
the value while doing so; all evidence must use sanitized commit identifiers, ref names, paths, and
provider case references only.

1. **Contain and rotate.** Revoke, disable, or rotate the credential at its provider before relying
   on a Git rewrite. Treat the old value as compromised even if the repository is private.
2. **Inventory reachability.** Identify every affected reachable ref, including the PR head branch,
   target branches, tags, releases, and repository-owned mirrors or sibling refs that contain the
   contaminated commit. Keep unrelated concurrent branches out of the incident worktree.
3. **Rewrite all affected history.** From an isolated incident worktree, use a reviewed secret-removal
   tool to remove the exposure from every identified reachable ref. A partial branch-only rewrite is
   not complete when the commit is still reachable from a tag, target branch, or PR ref.
4. **Replace remote state.** Verify the rewritten objects contain neither the secret nor its exposed
   file/path representation, force-push affected refs with `--force-with-lease`, and delete
   contaminated remote branches and tags. The exception in
   [Git Push Safety](../../development/workflow/git-push-safety.md#secret-exposure-history-remediation-exception)
   authorizes only these necessary lease-protected pushes; never use `--no-verify`.
5. **Replace the PR and complete external cleanup.** Close the contaminated PR, open a replacement PR
   from clean history, and run its normal required checks. Request provider-side purge of cached PR
   diffs and repository views where available. State accurately that external clones, forks, mirrors,
   and third-party caches cannot be erased by the repository; rotation remains the real containment.

No normal merge proceeds while a contaminated ref or PR remains reachable. The remediation record
must never include a secret value, matching fragment, command line containing it, or copied diff.

## 2. Environment Variable Naming Standard

### Variable classes

| Class                      | Rule                                        | Example                                           |
| -------------------------- | ------------------------------------------- | ------------------------------------------------- |
| App-defined value          | `SCREAMING_SNAKE`, per-app prefix           | `ORGANICLEVER_BE_PORT`, `OSE_BE_OPENROUTER_MODEL` |
| Framework-reserved         | Keep the framework's required name          | `NEXT_PUBLIC_*`, Next.js `PORT`                   |
| Shared service connection  | Unprefixed, conventional name               | `DATABASE_URL`                                    |
| Environment tier in a name | **Forbidden** (keys identical across tiers) | not `PROD_DATABASE_URL`                           |

The **per-app prefix** is the app's Nx project name upcased with `_` separators: `ose-be` →
`OSE_BE_`, `ose-www` → `OSE_WWW_`.

### Framework-reserved exempt names

| Name            | Why exempt                                                                    |
| --------------- | ----------------------------------------------------------------------------- |
| `NEXT_PUBLIC_*` | Framework-required (Next.js browser-exposure prefix)                          |
| `PORT`          | Platform convention (host/PaaS injects it) — **webs only**                    |
| `NODE_ENV`      | Node reserved                                                                 |
| `DATABASE_URL`  | Cross-ecosystem convention; prefixing breaks every tool that reads it by name |
| `HOSTNAME`      | Platform convention for Next.js dev server                                    |

**Critical asymmetry**: The **Next.js dev server** reads `PORT` natively — renaming it to
`OSE_WWW_PORT` would break `nx dev ose-www`. Rust **backend** ports are app-defined code, so they
**do** take the prefix (`ORGANICLEVER_BE_PORT`, `OSE_BE_PORT`). This is the single most
error-prone point of the naming standard.

## 3. Layout Standard — One Template per App

Each app's env template lives in exactly one place: `apps/<app>/.env.example`.

- **Rust backends**: template lives at `apps/<app>/.env.example` (where `Cargo.toml` lives).
- **Next.js webs**: template lives at `apps/<app>/.env.example` (where `next.config.*` lives). Next.js
  auto-loads `.env.local` from this directory; the `.env.example` is a documentation file only —
  never auto-loaded by Next.js or Nx.
- **Duplication is forbidden**: no second template for the same app under `infra/dev/` or elsewhere.

Relocating real gitignored `.env*` files (`.env.local` etc.) is a **[HUMAN]** task — the
`guard-env-file-access` policy forbids agents from touching them directly.

## 4. `.env.example` Annotation Format

Every env var line is preceded by a comment block:

```
# REQUIRED | <type> | <description>
# Format: <format note>
KEY=obviously-dev-placeholder

# OPTIONAL | <type> | <description> (default: <value>)
# OPTIONAL_KEY=
```

Rules:

- `REQUIRED` or `OPTIONAL` (no other values).
- Type is the runtime type: `string`, `u16`, `boolean`, `url`.
- Description is one short phrase; format notes go on a second `# Format:` line.
- **Required vars**: active line with an obviously-dev placeholder value (never a real secret).
- **Optional vars**: commented-out line (`# KEY=`), so the template is parseable without forcing
  developers to set non-required vars.
- Placeholders must be obviously fake: `postgres://postgres:postgres@localhost:5432/appname` is
  obviously local; `your-api-key-here` is obviously a placeholder.

## 5. Startup Validation

### Rust backends — `dotenvy` + `envy`

```rust
#[derive(serde::Deserialize)]
pub struct Config {
    pub database_url: String,               // required; no default
    #[serde(default = "default_port")]
    pub organiclever_be_port: u16,          // optional; typed default
}

impl Config {
    pub fn load() -> Result<Self, envy::Error> {
        dotenvy::dotenv().ok();             // no-op in CI; loads .env.local locally
        envy::from_env::<Config>()
    }
}
```

- `envy` maps struct field `organiclever_be_port` ↔ env var `ORGANICLEVER_BE_PORT` automatically.
- Required fields are non-`Option`, no `#[serde(default)]` — a missing value is a typed error at
  startup naming the field.
- Deps: `dotenvy = "0.15.7"` (exact pin, successor to the unmaintained `dotenv` RUSTSEC-2021-0141),
  `envy = "0.4.2"` (exact pin; last release Jan 2021; advisory-clean; narrow scope).

### TypeScript webs — `@t3-oss/env-nextjs` + `zod`

```typescript
// apps/<app>/src/env.ts
import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";
export const env = createEnv({
  server: {
    OSE_WEB_CONTENT_DIR: z.string().optional(),
    OSE_WEB_SHOW_DRAFTS: z.string().optional(),
  },
  experimental__runtimeEnv: {},
});
```

```typescript
// apps/<app>/next.config.ts — import triggers build-time validation
import "./src/env";
```

- `t3-env` validates at **build time** — a missing required var fails `nx build`, not at runtime.
- `NEXT_PUBLIC_*` client vars are enforced by t3-env's TypeScript types — a client var without the
  prefix is a compile error.
- Deps: `@t3-oss/env-nextjs` (exact pin, `0.12.0`), `zod` (exact pin, `4.0.5`).

## 6. `rhino-cli env` Toolchain

The full `rhino-cli env` family manages the local secrets lifecycle:

| Command                             | What it does                                                                       |
| ----------------------------------- | ---------------------------------------------------------------------------------- |
| `rhino-cli env backup [--dry-run]`  | Copies all secret files to `~/<repo-name>-env-backup/`                             |
| `rhino-cli env restore [--dry-run]` | Restores from the backup directory                                                 |
| `rhino-cli env init`                | Scaffolds `.env.local` from every `apps/<app>/.env.example` template               |
| `rhino-cli env validate`            | Checks each surface in `env-contract:` (`repo-config.yml`) for code↔template drift |

### Backup scope — hybrid floor + registry

Backup coverage = hardcoded floor ∪ `backup_globs` from the `env-contract:` section in `repo-config.yml`:

| Pattern                      | Status                                                  |
| ---------------------------- | ------------------------------------------------------- |
| `.env`, `.env.*`             | active                                                  |
| Everything under `.secrets/` | active                                                  |
| `secrets.json` at repo root  | active                                                  |
| `*.tfvars`, `*.tfvars.json`  | commented forward-scaffold — activate when IaC is added |
| Generated inventories        | commented forward-scaffold — activate when IaC is added |

The default backup target is `~/<repo-root-basename>-env-backup/` (e.g. `~/ose-public-env-backup/`).
This is the canonical per-repo backup directory aligned across the ose-public/ose-primer/ose-private
sibling repos.

### `env-contract:` section and drift validation

The `env-contract:` section in `repo-config.yml` at repo root declares each surface to validate:

```yaml
env-contract:
  surfaces:
    - root: apps/organiclever-be
      kind: app
      lang: rust
      allowlist: []
    - root: apps/ose-www
      kind: app
      lang: typescript
      allowlist: [PORT, HOSTNAME]
    # Terraform/Ansible: forward-scaffold — activate when IaC is added
```

`rhino-cli env validate` compares declared keys in `.env.example` against read keys in source code,
reporting `declared-but-unread` (stale template entry) and `read-but-undeclared` (undocumented read)
drift findings. Invoked by `.husky/pre-push` and `.github/workflows/validate-env.yml`.

## 7. Tiered Injection Standard

The sections above standardize how an app **declares** its env vars locally — naming convention (§2),
template layout (§3), annotation format (§4), and the `env-contract:` drift guard (§6). This
section closes the remaining gap: how a declared key is **injected** into each running surface across
GitHub Actions, Vercel, and the backend container / k3s path at each deploy stage.

### Source of truth

`apps/<app>/.env.example` is the canonical key set for every app-runtime variable. Every injection
target (GitHub Environment, Vercel project, k3s secret) uses the **same key names**. The rule from
§2 — a tier qualifier never appears in a key (`DATABASE_URL`, not `PROD_DATABASE_URL`) — is what
makes one key set serve all three stages. The stage is encoded by **which injection target** holds
the value, never by the key name.

### Variable classes with injection homes

The table below extends §2 with the injection home for each class:

| Class                      | Example                                                                     | `.env.example`?    | Injection home                                                                                 |
| -------------------------- | --------------------------------------------------------------------------- | ------------------ | ---------------------------------------------------------------------------------------------- |
| App-runtime (server)       | `DATABASE_URL`, `ORGANICLEVER_BE_NATS_URL`                                  | **yes**            | local `.env.local` · GitHub Env (CI) · Vercel encrypted env · k3s secret                       |
| App-runtime (public build) | `NEXT_PUBLIC_*`                                                             | **yes**            | same homes as server class, but **build-time** bundled by Next.js (never a secret)             |
| CI test-harness            | `WEB_BASE_URL`, `VERCEL_AUTOMATION_BYPASS_SECRET`, `PLAYWRIGHT_GREP_INVERT` | **no** (test-only) | GitHub Environment `vars.`/`secrets.` only; registered in `env-injection:` (`repo-config.yml`) |
| Platform-injected          | `VERCEL_GIT_COMMIT_REF`, `PORT`, `HOSTNAME`                                 | allowlisted        | supplied by the platform or framework; never declared by us, never set by us                   |

The CI test-harness class is new and important. `WEB_BASE_URL` and
`VERCEL_AUTOMATION_BYPASS_SECRET` are not app config — they describe the deployed staging target
that the e2e job probes. They must never appear in `apps/<app>/.env.example`. If they did, the
drift guard would flag them `declared-but-unread` (the app source code never reads them), producing
false findings. These keys belong exclusively in their own registry (see `env-injection:` section below).

`VERCEL_AUTOMATION_BYPASS_SECRET` is **load-bearing, not optional**. Every app-web Vercel deployment
has Deployment Protection enabled, which returns `401` to unauthenticated requests to the staging or
preview URL. The staging e2e job runs Playwright against that protected URL, so it must send Vercel's
Protection Bypass for Automation token. Without it, every staging run returns `401`. The real token
value is created by the `wire-vercel-www-app-cutover` plan (enable Protection Bypass per project,
then set the GitHub Environment secret); this standard only declares the key in the manifest and
reads it in the reusable workflow.

### Injection matrix

The table below maps each app type and stage to its injection platform and value owner:

| App type         | Stage      | Platform / target                               | Injection home                                                            | Values owned by                                |
| ---------------- | ---------- | ----------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------- |
| www / app-web    | local      | dev machine                                     | `apps/<app>/.env.local` (gitignored), auto-loaded by Next.js              | developer                                      |
| www / app-web    | local (CI) | GitHub Actions + docker-compose                 | `infra/dev/<stack>/` compose env, sourced from app `.env.example` keys    | this plan (refs only) / committed placeholders |
| www              | production | Vercel Production target (`prod-*-www` branch)  | Vercel project env, keys from `.env.example`                              | wire-vercel `[HUMAN]`                          |
| app-web          | staging    | Vercel Preview target (`stag-*-app-web` branch) | Vercel project env (Preview scope)                                        | wire-vercel `[HUMAN]`                          |
| app-web e2e gate | staging    | GitHub Env `{group}-app-staging`                | `vars.WEB_BASE_URL`, `secrets.VERCEL_AUTOMATION_BYPASS_SECRET`            | wire-vercel `[HUMAN]`                          |
| be (F#)          | local (CI) | GitHub Actions + docker-compose                 | `infra/dev/<group>/` compose env, sourced from app `.env.example` keys    | this plan (refs only) / committed placeholders |
| be (F#)          | staging    | k3s via ose-private `coralpolyp`                | container env from the ose-private secret store, keys from `.env.example` | ose-private (cross-repo)                       |

Two load-bearing boundaries follow from the matrix:

- **This plan writes only references** — the `environment:` names, the `vars.`/`secrets.` reads,
  the compose env wiring sourced from committed placeholders, and the value-less `env-injection:`
  manifest (in `repo-config.yml`). It creates no real values.
- **`wire-vercel` populates the values** — GitHub Environment secrets/vars and Vercel project env
  at each target. **coralpolyp (ose-private)** owns the backend k3s secret values. The contract (key
  set) is defined here; the cutover plan and ose-private fill it in.

### `infra/dev/<stack>` compose env — no duplicate templates

§3 forbids a second template per app. Compose stacks must not introduce their own `.env.example`
key list. They load a gitignored local `.env` (e.g. `infra/dev/organiclever-app/.env`, already
gitignored) and override with inline `environment:` in `docker-compose.ci.yml` for CI — never a
committed second template. Any value a CI job needs is set inline in the compose override or
sourced from the app's canonical `apps/<app>/.env.example` keys (placeholders only), so the drift
guard still sees one source of truth. New stacks (e.g. `infra/dev/organiclever-www/`) and stack
renames (e.g. `infra/dev/organiclever` → `infra/dev/organiclever-app`) follow this rule and keep
the gitignored `.env` in place.

### GitHub Environment key registry

Each `environment:` named by the pipeline holds exactly the keys that stage's jobs read, split into
non-secret `vars.` and secret `secrets.`. Values are placeholders or secrets only in-repo (created
by wire-vercel):

| Environment               | `vars.`                 | `secrets.`                        | Read by                                |
| ------------------------- | ----------------------- | --------------------------------- | -------------------------------------- |
| `{group}-app-local`       | _(none — compose-only)_ | local-CI secrets, if any          | `_reusable-app-test-local-deploy-stag` |
| `{group}-app-staging`     | `WEB_BASE_URL`          | `VERCEL_AUTOMATION_BYPASS_SECRET` | `_reusable-app-test-stag`              |
| _(www has no GitHub Env)_ | —                       | —                                 | www e2e runs entirely on local compose |

If `{group}-app-local` holds no secrets after wire-vercel completes, **omit the `environment:` key**
rather than bind an empty environment.

### `env-injection:` section — value-less injection manifest

The `env-injection:` section in `repo-config.yml` declares, per app, the injection home for every
key at every stage it runs in — names only, never values. It is the static contract that
`validate-env` checks for manifest consistency: every app-runtime key in `.env.example` has a
documented home at each stage the app runs; every CI test-harness key is registered and has no
`.env.example` entry. It is also the **checklist wire-vercel works from** when populating real values.

```yaml
# repo-config.yml — env-injection: section (value-less injection contract)
env-injection:
  apps:
    - app: organiclever-app-web
      runtime: { local: env-local, staging: vercel-preview, production: vercel-production }
      keys-from: apps/organiclever-app-web/.env.example
    - app: organiclever-be
      runtime: { local-ci: compose, staging: k3s-coralpolyp }
      keys-from: apps/organiclever-be/.env.example
  ci-harness:
    # test-only keys, never in any .env.example
    - key: WEB_BASE_URL
      class: var
      environments: [organiclever-app-staging, ose-app-staging]
    - key: VERCEL_AUTOMATION_BYPASS_SECRET
      class: secret
      environments: [organiclever-app-staging, ose-app-staging]
```

`rhino-cli env validate` gains a manifest-consistency pass — not a separate Nx target. The manifest
and `.env.example` are the same conceptual surface (the env contract), and `env validate` is already
wired into `.husky/pre-push` and `validate-env.yml`, so extending it adds the check with no
new target wiring. The check remains static and value-free. Actual presence of secret values in
GitHub, Vercel, or k3s is not machine-checkable from this repo and stays a wire-vercel / ose-private
`[HUMAN]` responsibility — the manifest is what they verify against.

## 8. Secret-Surface Census

| Surface                   | Path                                        | Backing tool       | Backed up          | Validated                                        |
| ------------------------- | ------------------------------------------- | ------------------ | ------------------ | ------------------------------------------------ |
| App env file              | `apps/<app>/.env.local`                     | dotenvy / Next.js  | Yes (floor)        | Yes (`env validate`)                             |
| Blessed secrets dir       | `.secrets/`                                 | manual             | Yes (floor)        | No                                               |
| Root secrets blob         | `secrets.json`                              | manual             | Yes (floor)        | No                                               |
| Terraform vars            | `infra/terraform/**/*.tfvars`               | Terraform          | Commented scaffold | Commented scaffold                               |
| Ansible inventory         | `infra/ansible/**/inventory`                | Ansible            | Commented scaffold | Commented scaffold                               |
| GitHub Environment secret | `{group}-app-staging` / `{group}-app-local` | GitHub Actions Env | No (platform)      | Manifest (`env-injection:` in `repo-config.yml`) |
| Vercel project env        | Vercel project settings (per target)        | Vercel dashboard   | No (platform)      | Manifest (`env-injection:` in `repo-config.yml`) |
| k3s / coralpolyp secret   | ose-private secret store                    | k3s + coralpolyp   | No (ose-private)   | ose-private cross-repo                           |

Template files (`*.env.example`) are tracked in git — they are not secrets. Real gitignored files are
the backup target. Injection-target rows (GitHub / Vercel / k3s) hold real values outside this repo;
the `env-injection:` section in `repo-config.yml` is the in-repo record of which key lives where.

## 9. `guard-env-file-access` Policy

AI agents must not directly read, write, edit, or commit any `.env*` file except `.env.example`. The
canonical identifier for this policy is **`guard-env-file-access`**.

Exceptions: project scripts under `apps/`, `libs/`, and `scripts/` are exempt (they are part of the
app's own startup/setup logic, not AI-agent operations).

### Content-fixture exclusion

Course and teaching material sometimes ships an env file as a **worked example** — an
ayokoding-www self-hosting kata that demonstrates a secret committed to a repo, for instance. Those
files are published curriculum, not real environment files, and blocking them stops agents from
authoring, linting, or even `git stash`-ing the course they belong to.

A file is excluded from `guard-env-file-access` when **both** hold:

1. It lives under an app's published content tree — `apps/<app>/content/**`.
2. Its basename ends in `.env` and is **not** a dotfile — `kata.env`, `app.env` qualify;
   `.env`, `.env.local` do not.

Everything else stays denied. A dotfile `.env*` under `content/` is still denied, and a
`<word>.env` outside any content tree is still denied.

**The exclusion is expressed by pattern shape, not by an enumerated path list.** Every guard keys on
a **dotfile** basename — `.env`, `.env.local` — so a `<word>.env` fixture falls outside the deny
without any per-tree entry. A new content tree needs no configuration change.

| Surface                                  | Carries the exclusion as                                                                  |
| ---------------------------------------- | ----------------------------------------------------------------------------------------- |
| `.claude/hooks/block-env-file-access.sh` | Bash-branch allow for `apps/*/content/**` where the char before `.env` is not `/` or `.`  |
| `.claude/settings.json`                  | `Read`/`Edit` allow for `apps/*/content/**/*.env`; deny globs were dotfile-shaped already |
| `.opencode/opencode.json`                | `apps/*/content/**/*.env: allow` in the read and edit permission maps                     |
| `~/.codex/config.toml` (untracked)       | deny globs written `**/.env*`, **never** `**/*.env*`                                      |
| `rhino-cli env staged-guard validate`    | no change — already keys on a dotfile `.env*` basename                                    |

**The Codex surface is the one that bites.** Its deny globs were originally `**/*.env`; the leading
`*` matched `kata.env` and blocked the whole course. Adding a narrower `apps/<app>/content/** =
"write"` does **not** reopen the files — Codex keeps the broader deny in force, contrary to the
"more specific overrides broader" wording in its own documentation. It also rejects a glob with
`write` outright:

```
Error loading configuration: filesystem glob path `...` only supports `deny` access;
use an exact path or trailing `/**` for `write` subtree access
```

So the deny itself must be shaped correctly — `**/.env`, `**/.env.local`, `**/.env.*.local`,
`**/.env.development`, `**/.env.test`, `**/.env.production`, `**/.env.staging`, `**/.env.preview` —
which also brings that profile in line with the dotfile assumption the rest of this repo already
makes.

**Residual gap, accepted deliberately**: a real env file named without a leading dot (`prod.env`)
is not covered by any guard here. That gap predates the exclusion — every surface in the table was
already dotfile-keyed — and a 2026-08-03 sweep of both Codex workspace roots found no such file:
every non-dotfile `*.env` on disk was an ayokoding course fixture. Name real env files as dotfiles.

See also: [`env-file-access.md`](./env-file-access.md)

## 10. IaC Forward Scaffold

Terraform and Ansible surfaces are documented in the `env-contract:` section of `repo-config.yml`
as **commented forward-scaffold** entries — syntactically present but inactive. Uncomment and fill
in `root` when IaC surfaces are added
to the repository. This prevents the drift guard from producing false findings before IaC exists while
ensuring the pattern is immediately available when it does.

## Related Documents

- [`no-secrets-in-committed-files.md`](./no-secrets-in-committed-files.md) — hard iron rule (stub)
- [`env-file-access.md`](./env-file-access.md) — `guard-env-file-access` agent policy (stub)
- [`reproducible-environments.md`](../../../repo-governance/development/workflow/reproducible-environments.md) — environment setup (stub for env section)
- [`docs/explanation/standardize-secrets-and-env-parity-decisions.md`](../../../docs/explanation/standardize-secrets-and-env-parity-decisions.md) — cross-repo parity decisions
- [`repo-config.yml`](../../../repo-config.yml) — unified config hub; `env-contract:` section = surface registry; `env-injection:` section = value-less injection manifest (names only; see §7)
