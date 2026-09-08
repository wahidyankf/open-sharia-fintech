---
description: What belongs in docs/, repo-governance/, plans/, and specs/, plus the temporary directories that may be swept at any time.
when_to_use: Use when deciding which tree a new document belongs in, or when a file feels misfiled.
---

# Content Trees

Four trees hold written material. They differ by **who is bound and for how long**, not by subject
matter — the same topic can legitimately appear in more than one.

| Tree               | Audience and force                                     | Lifetime                           |
| ------------------ | ------------------------------------------------------ | ---------------------------------- |
| `docs/`            | Explains the product and monorepo to humans and agents | Lives as long as what it describes |
| `repo-governance/` | Binds contributors — rules, conventions, workflows     | Until deliberately changed         |
| `plans/`           | Intent for one piece of work                           | Expires on archival                |
| `specs/`           | Executable acceptance criteria for products            | Lives with the feature             |

The distinction that misfiles most often: `docs/` **describes**, `repo-governance/` **binds**. A
document explaining how the monorepo is laid out is `docs/`; a document stating how contributors
must lay out a new app is `repo-governance/`.

The exception worth memorising is the language style guides under
`docs/explanation/software-engineering/`, which bind despite their location — see
[Repo Rules — Scope Boundaries](./repo-rules-scope.md).

## Temporary Directories

`generated-reports/` holds artifacts a human asked for and will read. `local-tmp/<agent-family>/`
holds everything an agent produces for itself or for another agent — checker and fixer reports
included. The split is by who asked, not by artifact type. Both may be swept at any time without
warning. Anything there is regenerable by definition; never write something you would need to
protect.

## Choosing a Tree

Ask in order:

1. Does it constrain what a contributor may do? → `repo-governance/`
2. Is it acceptance criteria a test can consume? → `specs/`
3. Is it intent for one piece of work that ends? → `plans/`
4. Otherwise → `docs/`, placed by Diátaxis category.

Within `repo-governance/`, the layer is chosen by the question the document answers — see the
"Choose the Right Home" table in the [governance index](../README.md).

## Related Documents

- [Glossary](../glossary.md) — the other term clusters.
- [Repo Rules — Scope Boundaries](./repo-rules-scope.md) — which of these trees bind.
- [Plans Organization Convention](../conventions/structure/plans.md) — the `plans/` lifecycle.
