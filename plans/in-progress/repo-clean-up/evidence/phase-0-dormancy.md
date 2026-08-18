# Phase 0 Dormancy Proof — Repository Clean-Up

Every execution surface was searched for `ayokoding-cli`, `ose-cli`, `rust-commons`, and
`beavernest-app-web`. A hit on any surface other than the two permitted ones halts the plan.

## Execution surfaces

| Surface                                 | Result          |
| --------------------------------------- | --------------- |
| `package.json` scripts                  | **zero**        |
| `.husky/**`                             | **zero**        |
| `.github/**` (21 workflow files)        | **zero**        |
| `repo-config.yml` gate `command:` lines | **zero**        |
| Nx `project.json` command strings       | one — see below |

## The Nx hits, enumerated

| Location                              | Kind                                                            | Executed?                                                                                                                                                                                                                                  |
| ------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `apps/ose-www/project.json:118`       | `links:check` target invoking `../../apps/ose-cli/dist/ose-cli` | **No.** `ose-www:test:quick` runs only `typecheck`, `lint`, `test:unit`, `test:coverage`, `test:specs`. A repo-wide search for `links:check` outside `plans/**` returns exactly one hit — the target's own definition. Nothing invokes it. |
| `apps/ose-www/project.json:5`         | `"implicitDependencies": ["ose-cli"]`                           | Graph edge only; no target runs the binary.                                                                                                                                                                                                |
| `apps/ayokoding-www/project.json:191` | `"implicitDependencies": ["ayokoding-cli"]`                     | Graph edge only. `ayokoding-www` has no `links:check` target at all, despite the governance doc instructing readers to run one.                                                                                                            |
| `libs/rust-commons/project.json:123`  | `deps:audit` echo string naming all three CLIs                  | Prints a message; invokes nothing.                                                                                                                                                                                                         |

**Verdict: dormancy proven.** Both permitted hits are the ones the plan predicted; no other
execution surface references any retired project.

## `apps/beavernest-app-web`

```
$ git ls-files apps/beavernest-app-web
apps/beavernest-app-web/LICENSE
```

Exactly one tracked file. No `project.json`, so Nx does not see it; no `repo-config.yml` registry
entry. In scope.

## `libs/rust-commons` has no consumer outside the two CLIs

```
$ grep -rn "rust-commons" --include=Cargo.toml apps/ libs/ | grep -v "^libs/rust-commons/"
apps/ayokoding-cli/Cargo.toml:20:rust-commons = { path = "../../libs/rust-commons" }
apps/ose-cli/Cargo.toml:20:rust-commons = { path = "../../libs/rust-commons" }
```

`apps/rhino-cli/Cargo.toml` contains **zero** references. Deleting both CLIs orphans it.

## Every `apps/rhino-cli/**` mention is inert

Four files mention a deleted path. None reads the real path, so no rhino-cli test can break and no
four-repo parity obligation is opened.

| File:line                                           | Nature                  | Evidence                                      |
| --------------------------------------------------- | ----------------------- | --------------------------------------------- |
| `src/application/doctor/checker.rs:1044,1059,1088`  | `TempDir` fixture paths | `#[cfg(test)]` at line 652 precedes all three |
| `src/application/docs/links.rs:1091,1093,1110,1115` | `TempDir` fixture paths | `#[cfg(test)]` at line 759 precedes all four  |
| `src/commands/specs_validate_counts.rs:5`           | `//!` doc comment       | module-level comment                          |
| `tests/cargo_target_share.rs:38`                    | `//!` doc comment       | module-level comment                          |

**Verdict: no rhino-cli source change is required, and none will be made.**
