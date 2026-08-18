# Pre-Push Quality Evidence — `worktree/repo-clean-up`

Run from the plan's worktree on 2026-08-18, at the delivery boundary (Phase 4, before the single
push that carries all five commits).

## `apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`

**Exit code 0.** Every registered `pre-push` gate ran. Notable results:

| Gate                                                                        | Result                                                                                                                                          |
| --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `test-quick`                                                                | PASS — coverage `88.26% >= 80%` threshold                                                                                                       |
| `md-links`                                                                  | PASS with **no content exclusions** — this is the first pre-push run where `apps/ayokoding-www/content` and `apps/ose-www/content` are in scope |
| `governance-readme-index`                                                   | 423 `unannotated` findings, none of the armed `orphan`/`ghost` kinds — pre-existing, unchanged by this branch                                   |
| `governance-readme-completeness`                                            | PASS — no orphan or ghost references                                                                                                            |
| `governance-word-budget`                                                    | PASS — warnings only, all pre-existing; every file this branch touched was verified to be at or below its `origin/main` word count              |
| `harness-duplication`                                                       | PASS — 0 clusters                                                                                                                               |
| `harness-bindings`                                                          | PASS — 96/96 in sync                                                                                                                            |
| `parity-manifest`                                                           | PASS — `apps/rhino-cli/**` untouched, so no cross-repo obligation opened                                                                        |
| `vendor-independence`                                                       | PASS — no violations                                                                                                                            |
| `convention-license`                                                        | PASS — no findings                                                                                                                              |
| `specs-structure`, `workflows-naming`, `compat-min-version`, `env-validate` | PASS                                                                                                                                            |
| E2E coverage gap detector                                                   | PASS on every app — 0 new unbound scenarios beyond baseline                                                                                     |

## `npm exec nx affected -t build,test:quick,lint --base=origin/main`

**Exit code 0.** `Successfully ran targets build, test:quick, lint for 33 projects and 19 tasks they
depend on` (78 of 99 tasks served from cache).

Nx flagged `beavernest-app:codegen` as a flaky task. It passed on this run and the flake is a known
standing condition of that target, unrelated to this branch — this plan touches no Flutter code.

## Formatter sweep (not covered by the gates)

`format-verify-prettier` declares `ci: { scope: affected-file-type }`, so a documentation-heavy
branch can leave files unformatted with every gate green. The branch's own changed Markdown set was
therefore swept by hand with the repo-pinned binaries:

- `./node_modules/.bin/prettier --check` over all 76 changed Markdown files — 5 initially failed and
  were rewritten; re-check clean.
- `./node_modules/.bin/markdownlint-cli2` (v0.21.0) over the same set — `0 error(s)`.
- `rhino-cli md mermaid validate` — the repository carries 786 pre-existing violations, **none** in
  any file this branch changed.

That prettier gap is filed as a second independent instance on the
[`markdownlint-ci-gate-lints-zero-files`](../../../ideas/q1-urgent-important/markdownlint-ci-gate-lints-zero-files.md)
two-pager.
