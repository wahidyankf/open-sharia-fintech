Posted: Monday, May 18, 2026
Platform: LinkedIn

---

OPEN SHARIA ENTERPRISE
Week 26 / Phase 1, Week 14

Window: 2026-05-10 23:01 +0700 → 2026-05-18 17:27 +0700.

Highlights: governance/ → repo-governance/ rename across all four repos; Go lint baseline at 16 active linters; ayokoding-web architecture tutorials grew an Examples-by-Level layer with FP and OOP by-example splits for DDD+Hex and Finite State Machines.

🌐 Cross-repo

- governance/ → repo-governance/ in parent + ose-public + ose-infra + ose-primer, via plan-quality-gate.
- Plans archived: stack-update, ddd-hex-in-the-field, ddd-hex-hypothetical-rewrite, p2p-shared-architecture-domain, rename-governance-to-repo-governance, golang-lint-parity.
- Vendor-name mentions replaced with generic terms in ose-public and ose-primer governance docs.

🌳 ose-public

ayokoding-web: architecture/by-example populated with DDD+Hex and FSM tutorials, FP/OOP variants split; Examples-by-Level anchor layer added; Patterns and Principles section added; E2E + unit step smoke for DDD+Hex in-the-field tutorials.

Governance: new conventions codified — FP-variant multi-language layout, subagent orchestration, Examples-by-Level anchor linking.

crane-cli (Content Retrieval And Normalization Engine, F# CLI for media-handling pipelines; today PDF-to-Markdown, broader media planned): stableKey 16 hex chars; skiplist switched to global markdown source; normalized MD cached; check-all aggregator wired.

pdf-to-md: stagnation exit + confidence-downgrade logic; applied to docs/security/nist-sp-800-53 with missing H2 fixes.

🏗️ ose-infra

golang-lint-parity: 5 strict linters added (errorlint, godot, revive, gochecksumtype, …); 16 active linters now documented; rhino-cli fixes applied; no-date-metadata convention enforced.

📦 ose-primer

Same golang-lint-parity adoption; worktrees/ + .memsearch gitignored, worktrees/ added to .nxignore; Mermaid node labels shortened; vendor-neutral terms applied.

🔜 Next 2–4 weeks

Focus: solidify the fundamentals of code and software architecture across the repos — shared conventions and standards before app-level work. Picking and enforcing architecture up front is what lets future work run at the highest possible speed without cognitive debt.

Approach: DDD + Hexagonal across all projects, paired with standardized code-level practice — TDD by default, shared linting and testing baselines. Backends split by product line: ose\* on F#-based stacks, organiclever\* on JVM-based stacks.

In the same window: ose-app\* foundation (ose-app-be, ose-app-web) laid on top of that baseline; ose-app-mobile deferred.

Personally: next 1 week starts with surveying interesting code architectures to feed the convention work.

Insha Allah.

- ose-public: https://github.com/wahidyankf/ose-public
- ose-primer: https://github.com/wahidyankf/ose-primer
- OrganicLever: https://www.organiclever.com/
- Updates: https://www.oseplatform.com/updates/
- Learning: https://www.ayokoding.com/
