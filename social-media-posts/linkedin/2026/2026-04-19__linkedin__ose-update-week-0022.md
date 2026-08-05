Posted: Sunday, April 19, 2026
Platform: LinkedIn

---

OPEN SHARIA ENTERPRISE
Week 22 / Phase 1, Week 10

This week: ose-primer (forked from ose-public) stripped to a generic MIT init template, sync infrastructure live, naming conventions enforced by CI, plan format grew BRD+PRD layers, wahidyankf-web adopted — 358 commits across four repos.

The repos:

- ose-public (public) — main product monorepo; Phase 1 OrganicLever + AyoKoding
- ose-infra (private) — infra monorepo; self-hosted CI, coralpolyp app
- ose-projects (private) — parent coordination; tracks the other three as gitlinks
- ose-primer (public, MIT) — template fork of ose-public for easier repo init

What changed:

🤖 Multi-Repo AI Way of Working Is Taking Shape
Cross-repo naming rules, sync infrastructure, plan format, and agent tiers are now systematically governed across all four repos. Working with AI at this scale is becoming a real discipline.

🧩 ose-primer Cleaned Up as Generic Init Template
Forked from ose-public but still carried all product content. This week: product apps, agents/skills, Gherkin specs, FSL license docs, Codecov, and orphaned libs removed. Demo apps dropped `a-` prefix. License → MIT. Clone it freely — commercial or non-commercial.

🔗 Third Gitlink + Sync Live
Parent tracks three bare gitlinks. Sync layer: classifier, shared skill, two agents, orchestration workflow. First propagation PR to ose-primer merged.

🏷️ Naming Convention — With CI Enforcement
Rule: `<scope>(-<qualifier>)*-<role>`. repo-governance → repo-rules, swe-_-developer → swe-_-dev. rhino-cli validators in pre-push and PR gates.

📄 Plan Format: BRD + PRD Split
Splitting requirements into BRD (business rationale) and PRD (product requirements + Gherkin) makes plans easier for us humans to read and comprehend — and gives AI models more to cross-check. plan-executor removed; execution via workflow directly.

🌐 wahidyankf-web: full Nx app, Playwright-BDD E2E, Vercel CD. ⚖️ Model tiers: 16 OMIT→SONNET, 2 OPUS→SONNET, 2 SONNET→HAIKU across all repos.

🏗️ ose-infra: a-demo removed, GHA runner capped 2CPU/8GB concurrency 4→3. coralpolyp E2E fixed — planned core app for OSE Platform's infra orchestrator.

🛠️ RTK + Caveman — I Personally Recommend Both
RTK (https://www.rtk-ai.app/): 8,401 commands (Apr 13-19), 76.8% tokens saved (10.4M tokens) — fewer tokens means less context compaction in Sonnet, hence increasing its performance. Caveman (https://github.com/JuliusBrussee/caveman) — use full mode, not ultra; keeps AI responses tight without losing substance.

🔜 What's next:
organiclever-fe local-first mode + full client-side CI/CD (local, staging, production). Stabilize wahidyankf-web with a personal blog. BE side deferred to W3 next month until the FE is more stable. Insha Allah.

ose-public: https://github.com/wahidyankf/ose-public
ose-primer: https://github.com/wahidyankf/ose-primer
Updates: https://www.oseplatform.com/updates/
Learning: https://www.ayokoding.com/
