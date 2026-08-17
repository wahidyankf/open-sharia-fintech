# OrganicLever DDD Artifacts

Domain-Driven Design artifacts for the `organiclever-app-web` bounded-context architecture.
These files are the machine-readable source of truth consumed by `rhino-cli specs structure validate`
(its `bc:` and `ul:` layers) during `nx run organiclever-app-web:test:quick`.

DDD artifacts live at the application root (`specs/apps/organiclever/ddd/`), not under
`components/app-web/`, because the ubiquitous language belongs to the bounded context — not to one
implementation surface. Today only `organiclever-app-web` implements these contexts; when
`organiclever-be` grows domain code, its paths join the same registry without a folder rename.

## Structure

```
specs/apps/organiclever/ddd/
├── README.md                  # This file
├── bounded-contexts.yaml      # Registry — 9 bounded contexts with layers, paths, relationships
├── bounded-context-map.md     # Visual bounded-context map with Mermaid diagrams
└── ubiquitous-language/       # Per-context glossaries (one .md per bounded context)
    ├── README.md              # Authoring rules and index
    └── *.md                   # One glossary file per bounded context
```

## Files

- **[bounded-contexts.yaml](./bounded-contexts.yaml)** — Declares every bounded context: layer
  subfolders, list of code paths (one per implementation surface — FE today, BE later), glossary
  path, gherkin path, and inter-context relationships. Read by the `bc:` layer of `specs structure validate` to validate
  structural parity against the filesystem.

- **[ubiquitous-language/](./ubiquitous-language/README.md)** — One Markdown glossary per bounded
  context. Each term entry maps a domain concept to its code identifiers and feature file
  references. Read by the `ul:` layer of `specs structure validate` to validate vocabulary consistency.

## How enforcement works

See [specs/apps/organiclever/README.md § DDD Registry](../README.md#ddd-registry-bounded-contextsyaml)
for full details on what each command checks.

## Related

- [bounded-context-map.md](./bounded-context-map.md) — Visual bounded-context map with Mermaid
- [rhino-cli commands](../../../../apps/rhino-cli/README.md#quick-start)
