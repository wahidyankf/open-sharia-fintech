Posted: Sunday, May 10, 2026
Platform: LinkedIn

---

Open Sharia Enterprise — Phase 1, Week 13 monthly update.

A few notable changes from the last five weeks:

- OrganicLever moved to a local-first model. The data layer now runs in the browser via PGlite (PostgreSQL compiled to WASM); the F# backend remains as a kept-warm scaffold.
- The codebase split from one repository into four: ose-public, ose-infra, ose-primer, and ose-projects (parent). The polyglot demo apps moved out of ose-public into the ose-primer template.
- organiclever-web was restructured into 9 DDD bounded contexts. The same C4 + DDD specs format was adopted across all four web apps.
- rhino-cli picked up DDD validators, vendor-audit, cross-vendor parity, a mermaid validator, and a stricter Go linting baseline.
- Rust is the chosen language for ose-infra going forward.
- The license reverted from FSL-1.1-MIT back to MIT.

Cadence over the period: roughly 38 commits per day across the four repos. The next month focuses on stabilizing what was added — BDD and DDD hardening, more experiments with cheaper Chinese LLM models via OpenCode Go, and an AI-powered demo family in ose-primer.

Full write-up: https://www.oseplatform.com/updates/2026-05-10-phase-1-week-13-local-first-and-repo-split

Insha Allah.

- ose-public: https://github.com/wahidyankf/ose-public
- ose-primer: https://github.com/wahidyankf/ose-primer
- OrganicLever: https://www.organiclever.com/
- Updates: https://www.oseplatform.com/updates/
- Learning: https://www.ayokoding.com/
