# OSE — DDD Artifacts

Domain-Driven Design artifacts for the OSE family. The `ose-be` backend uses a
bounded-context architecture; `ose-web` (OSE Platform) has no bounded contexts defined.

These files are the machine-readable source of truth consumed by `rhino-cli specs structure validate`
(its `bc:` and `ul:` layers).

## Structure

```
specs/apps/ose/ddd/
├── README.md                  # This file
├── bounded-contexts.yaml      # Registry — 5 bounded contexts (ose-be)
├── bounded-context-map.md     # Visual bounded-context map with Mermaid diagrams
└── ubiquitous-language/       # Per-context glossaries (one .md per bounded context)
    ├── README.md              # Authoring rules and index
    └── *.md                   # One glossary file per bounded context
```

## Files

- **[bounded-contexts.yaml](./bounded-contexts.yaml)** — Declares every bounded context
- **[bounded-context-map.md](./bounded-context-map.md)** — Visual bounded-context map
- **[ubiquitous-language/](./ubiquitous-language/README.md)** — One Markdown glossary per bounded context

## Related

- [rhino-cli commands](../../../../apps/rhino-cli/README.md#quick-start)
