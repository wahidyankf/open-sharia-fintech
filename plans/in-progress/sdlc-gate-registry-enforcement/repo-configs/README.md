---
title: "Target-State repo-config.yml — SDLC Gate Registry Enforcement"
description: The complete post-change repo-config.yml for each of the four repos, copied in during execution
category: explanation
subcategory: plans
tags:
  - ci-cd
  - rhino-cli
  - parity
created: 2026-08-02
---

# Target-State `repo-config.yml`

One file per repo, holding the **complete `repo-config.yml` as it should look after this plan lands**
— every existing section reproduced verbatim from that repo's current file, plus the `gates:` section
this plan adds. Execution copies from here, so the four registries are reviewable side by side before
any repo is touched.

| File                                                           | Repo          | Formatters | Registry notes                                             |
| -------------------------------------------------------------- | ------------- | ---------- | ---------------------------------------------------------- |
| [`repo-config-ose-public.yml`](./repo-config-ose-public.yml)   | `ose-public`  | 9          | Canonical. Prunes 5 dead entries                           |
| [`repo-config-ose-primer.yml`](./repo-config-ose-primer.yml)   | `ose-primer`  | 10         | Polyglot. Prunes 0, **adds** shfmt and sql/html globs      |
| [`repo-config-ose-private.yml`](./repo-config-ose-private.yml) | `ose-private` | 4          | Prunes 5, adds shfmt and tofu. Carries the `iac-lint` pair |
| [`repo-config-beaver-nest.yml`](./repo-config-beaver-nest.yml) | `beaver-nest` | 5          | Prunes 9                                                   |

## Before copying, re-verify the unchanged part

Each file opens with a `# TARGET STATE` banner that must **not** be copied into the repo. Everything
between the banner and `gates:` is that repo's content as of 2026-08-02. These repos are edited
concurrently by other actors, so confirm nothing else has landed since:

```sh
# Strip the banner and the gates section, then compare against the live file.
# The range starts at the schema line, so the `# TARGET STATE` banner is skipped;
# the two `sed '$d'` passes drop the trailing `gates:` line and its blank separator.
diff <(sed -n '/^# repo-config.yml/,/^gates:/p' repo-config-<repo>.yml | sed '$d' | sed '$d') \
     <repo>/repo-config.yml
```

Verified against `ose-public` at authoring time: the command above prints nothing. Each per-repo
file carries the same command in its own banner.

A non-empty diff is a Phase 0 finding: reconcile it rather than overwriting, or the copy silently
reverts someone else's change.

## Why the entry sets differ

Gate entry **sets** are data and legitimately differ per repo; the **schema** and the engine reading
it do not. This is the same rule that already lets `ose-private` carry an `iac-lint` pair the others
lack — see
[tech-docs §2.3](../tech-docs.md#23-why-gate-sets-may-differ-per-repo-but-the-schema-may-not).

Formatter counts differ under the presence rule: a formatter is declared **if and only if** the repo
has at least one tracked file matching its glob, measured by `git ls-files`. The counts behind each
number above are in
[tech-docs §2.2.4](../tech-docs.md#224-the-full-formatter-and-per-file-inventory).

**One deliberate exception.** `sql` stays in every repo's prettier glob, including the two repos with
zero tracked `.sql` files, because SQL is expected in their future and a prettier extension carries no
tool cost. This is user-directed and recorded rather than inferred.

## Two structural findings these files surfaced

- **`ose-primer` carries a `doctor:` section the other three lack.** The header comment in every
  repo's `repo-config.yml` claims the structure is "byte-identical across all three repos" — that
  claim is already false. The schema-parity gate does not catch it, because it validates each file
  against the schema rather than against the other repos.
- **Every repo's header comment says "all three repos"** and lists six sections. With `beaver-nest`
  joining the byte-identity boundary and `gates:` being added, that comment is wrong on both counts
  in all four repos and is corrected as part of this plan.

## Related

- [tech-docs §2.2](../tech-docs.md#22-registry-location-and-shape) — the field contract these files conform to
- [husky-hooks/](../husky-hooks/README.md) — the hook shims that invoke these gates
- [package-json/](../package-json/README.md) — the `lint-staged` block emitted from these gates
