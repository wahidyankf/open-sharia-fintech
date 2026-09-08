---
description: Which terms need glossing on first use in specs/ files (and which mainstream SWE terms do not), for the SWE-background TPM audience.
when_to_use: Use when writing a specs/apps/ file and checking whether a term needs a parenthetical gloss on first use.
---

# Standard 5 — PM-Readability Contract for specs/ (Glossary)

Every NEW or MOVED file under `specs/apps/` must be readable by a **SWE-background Technical Product/Project Manager** — the kind of TPM embedded with a developer-tools team who has shipped software and reads code fluently. The contract is calibrated to gloss only the genuinely niche. Over-glossing mainstream SWE vocabulary is patronizing noise.

**Terms that do NOT need glossing** (the SWE-background TPM already knows): TypeScript, JavaScript, Next.js, React, Node.js, Postgres, Docker, Kubernetes, REST, HTTP, JSON, YAML, OpenAPI, IndexedDB, FSM, finite state machine, CI, CD, CI/CD, ADR, Architecture Decision Record, build pipeline, lockfile, version pinning, Volta, npm, ESLint, Prettier, Mermaid, Playwright, Vercel, monorepo, Nx.

**Terms that DO need glossing on first use within each file** (genuinely niche to this product):

| Term                                                                     | Gloss to use on first occurrence                                                                                                     |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| DDD (when first introducing the OrganicLever-specific application of it) | Domain-Driven Design — here applied as one bounded context per UI screen domain                                                      |
| bounded context                                                          | a self-contained slice of the app with its own vocabulary, types, and rules; contexts communicate only through narrow published APIs |
| aggregate                                                                | a cluster of domain objects treated as one consistent unit by writes                                                                 |
| ubiquitous language                                                      | the shared vocabulary used by both the team and the code for one bounded context                                                     |
| PGlite                                                                   | Postgres-WASM — Postgres compiled to WebAssembly running directly in the browser, persisted via IndexedDB                            |
| XState                                                                   | a JavaScript/TypeScript state-machine library used here for UI flow orchestration                                                    |
| Effect TS                                                                | a TypeScript library for typed effect composition, used in the infrastructure layer                                                  |
| F#                                                                       | functional .NET language used for the OrganicLever backend                                                                           |
| Giraffe                                                                  | F# web framework on top of ASP.NET Core, used for the OrganicLever HTTP API                                                          |
