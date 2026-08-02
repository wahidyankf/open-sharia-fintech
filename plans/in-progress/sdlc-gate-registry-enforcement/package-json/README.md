---
title: "Target-State lint-staged Blocks — SDLC Gate Registry Enforcement"
description: The lint-staged block gate emit must produce for each repo, used as the emitter's acceptance oracle
category: explanation
subcategory: plans
tags:
  - ci-cd
  - rhino-cli
  - parity
created: 2026-08-02
---

# Target-State `lint-staged` Blocks

One file per repo, holding the `lint-staged` object exactly as
`rhino-cli gate emit --surface=pre-commit` must produce it. Paste each into that repo's
`package.json` under the `"lint-staged"` key.

| File                                                             | Repo          | Glob keys |
| ---------------------------------------------------------------- | ------------- | --------- |
| [`lint-staged-ose-public.json`](./lint-staged-ose-public.json)   | `ose-public`  | 22        |
| [`lint-staged-ose-primer.json`](./lint-staged-ose-primer.json)   | `ose-primer`  | 23        |
| [`lint-staged-ose-private.json`](./lint-staged-ose-private.json) | `ose-private` | 17        |
| [`lint-staged-beaver-nest.json`](./lint-staged-beaver-nest.json) | `beaver-nest` | 18        |

These are the emitter's **acceptance oracle**. Phase 1's `gate emit` is correct when:

```sh
rhino-cli gate emit --surface=pre-commit
diff <(jq '."lint-staged"' package.json) <plan>/package-json/lint-staged-<repo>.json
```

is empty. That is a diff, not a judgement — which is the point of authoring the target rather than
describing it.

## Why prettier keeps separate glob keys

An earlier draft consolidated every prettier file type into one key
(`*.{md,json,yml,yaml,css,scss,html,sql,ts,...}`). That is a **behaviour change**, and a harmful one.

`lint-staged` runs the commands within a single glob key **sequentially**, but runs different glob
keys **concurrently**. Today `*.md` is an ordered chain — `prettier --write` first, then
`markdownlint-cli2`, then the four `md * validate` commands — so markdown is always formatted before
it is linted. Moving prettier to its own key breaks that ordering guarantee and lets markdownlint run
against unformatted markdown.

So `format-prettier` declares a **list** of globs (`globs:`) rather than one, and the emitter writes
it into each. Because declaration order is execution order and `format-prettier` is declared before
`markdownlint`, prettier lands first in the `*.md` chain automatically.

## Verified delta against the current blocks

For `ose-public`, comparing the generated block to the live one in `package.json`:

| Change                                                         | Deliberate?                                                                  |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Removed `*.go`, `*.{ex,exs}`, `*.cs`, `*.clj`, `*.dart`        | Yes — those five languages have zero tracked files here                      |
| Added `apps/*/package.json` running `git lockfile sync`        | Yes — the lockfile step moves out of inline hook shell so it can be declared |
| `--quiet` added to four `cargo run` invocations that lacked it | Yes — normalization; the hooks already used `--quiet`, `lint-staged` did not |
| `--exclude apps/ayokoding-www/content` gains quotes            | Yes — an unquoted glob-shaped argument is shell-expandable                   |
| 17 of 26 glob keys byte-identical                              | Unchanged                                                                    |

Nothing else changed. Any other difference at execution time is drift that landed after 2026-08-02
and must be reconciled, not overwritten.

## Related

- [repo-configs/](../repo-configs/README.md) — the registry these blocks are emitted from
- [husky-hooks/](../husky-hooks/README.md) — the `pre-commit` shim that invokes `npx lint-staged`
- [tech-docs §2.2.2](../tech-docs.md#222-lint-staged-is-generated-not-replaced) — why lint-staged is generated rather than replaced
