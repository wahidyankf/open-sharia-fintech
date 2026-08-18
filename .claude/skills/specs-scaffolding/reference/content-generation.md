# Content Generation

## Create Missing READMEs

Generate `README.md` files for specific directories, inferring content from: feature files
present in the directory; domain folder structure; existing README patterns from sibling spec
areas; surface profile (web/be/cli determines Background step and vocabulary).

## Generate Feature Files

Create new `.feature` files following conventions: `Feature:` header with user story block (As a
/ I want / So that); `Background:` with standard context step (surface-appropriate); `Scenario:`
blocks with Given/When/Then steps; UI-semantic steps for web specs, HTTP-semantic for BE specs,
shell-semantic for CLI specs; BE/web/CLI placed in a domain subdirectory under
`behavior/<product>-<surface>/gherkin/<domain>/` (e.g., `ayokoding-build-tools` for ayokoding
build-time features).

## Create C4 Diagrams

Generate Mermaid-based C4 diagrams following the accessible color palette
(`Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC, Brown #CA9161, Gray #808080`):

- Context (`system-context/context.md`) — C4 L1: system boundary with actors.
- Container (`containers/container.md`) — C4 L2: runtime containers and data stores.
- Component BE (`components/be/component-be.md`) — C4 L3: internal structure of backend
  container.
- Component Web (`components/web/component-web.md`) — C4 L3: internal structure of web
  container.

## Scaffold DDD Artifacts

When `target` includes `components/<surface>/ddd/`, scaffold:

```
{target}/ddd/
├── README.md
├── bounded-contexts.yaml     # registry stub
├── bounded-context-map.md    # PM-readable narrative + Mermaid diagram
└── ubiquitous-language/
    ├── README.md
    └── {bc}.md               # one per bounded context (if known)
```

DDD scaffolding is only created when explicitly targeted — it is never added automatically during
full app tree scaffolding. Adoption is a team decision.
