Posted: Monday, June 8, 2026
Platform: LinkedIn
Window: 2026-06-01 20:15 +0700 → 2026-06-08 18:01 +0700. ~352 commits across the three repos (ose-public 116, ose-primer 92, ose-infra 144).

---

OPEN SHARIA ENTERPRISE
Week 29 / Phase 1, Week 17

Highlights: walked DDD back out of the web frontends, shipped a unified markdown quality gate with a CISA KEV-aware dependency policy, and turned an outage into a hardened two-node fleet.

🌐 Cross-repo

- Dependency-security pass: exact-version pinning, CVE clearance. Bump policy now adds the CISA KEV catalog and EPSS scoring—key bumps: Next.js 16.2.7, Node 24.16.0, .NET 10.
- Unified markdown gate: repo-wide link + #anchor validation, heading-hierarchy on a prose allowlist, mermaid with --exclude — one `validate-markdown` CI workflow.
- Blameless post-mortem convention adopted across all three repos.
- Plan-domain parity: planning canon unified; execution defaults to synced worktrees; TDD enforced.
- Gherkin keyword-cardinality HARD rule: one Given/When/Then shape per scenario, new rhino-cli audit.
- Harness binding update: OpenCode emits a permission object; Codex config in `config.toml` sub-tables.

🌳 ose-public

Last week: "hexagonal + DDD everywhere." This week, I corrected the DDD part. ayokoding-web, ose-web, and wahidyankf-web dropped their DDD bounded-context registries and empty domain-layer stubs — DDD belongs in backends with real domain logic, not content sites. ayokoding-web and ose-web keep their hexagonal feature modules; wahidyankf-web, a static portfolio, flattened to a flat layout — the new static-site exemption. It also got an SSR pass: removed `useSearchParams`, added SSR props, switched its Dockerfile to `next start`.

🏗️ ose-infra

Recovered from a real outage: a self-hosted node lost connectivity after a network flap, then went fully host-down. Hardening: automated remote power recovery, off-host alerting, scheduled VM backups, watchdog, auto-power-on. Then expanded: a CI runner moved onto a second self-hosted node, completing Part 1 of the twin-cluster plan. IaC provider upgraded several majors; architecture refreshed. Non-prod domain standard set; secrets standardization plan started.

📦 ose-primer

Absorbed the cross-repo work across the polyglot demos: dependency-hygiene, markdown gate, post-mortems, plan parity, gherkin rule, bindings. Flutter image migrated to instrumentisto; F# packages pinned to exact versions.

🔜 Next 2–4 weeks

Part 2: staging and production clusters on the two-node fleet, running the organiclever-be and ose-app-be Rust backends. Standardize secrets and env handling. Power outage remains the honest risk. When the time comes, we'll move production to the cloud or another on-premises DC-DRC, depending on conditions.

Last week: "hexagonal + DDD everywhere." This week: DDD lives in backends, not content sites; the outage became a hardened fleet: right tool, right place.

Insha Allah

- ose-public: https://github.com/wahidyankf/ose-public
- ose-primer: https://github.com/wahidyankf/ose-primer
- OrganicLever: https://www.organiclever.com/
- Updates: https://www.oseplatform.com/updates/
- Learning: https://www.ayokoding.com
