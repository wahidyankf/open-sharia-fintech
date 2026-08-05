Posted: Tuesday, July 21, 2026
Platform: LinkedIn
Window: 2026-07-13 → 2026-07-21. 264 commits across the three repos (ose-public 213, ose-primer 27, ose-infra 24), 65 pull requests merged (46 / 10 / 9).

---

OPEN SHARIA ENTERPRISE
Week 35 / Phase 1, Week 23

Highlights: the curriculum shipped — 37 phases of "Fundamentally Strong" content live on ayokoding.com — and a one-line parser bug turned out to have silenced 73% of this repo's diagram validation.

🌳 ose-public

- 37 phases of the Fundamentally Strong Software Engineer curriculum merged and deployed: Just Enough Nvim / Lua / Python / Bash / TypeScript primers, by-example topics from Git and data structures through concurrency, advanced SQL, ORMs and agentic coding, plus four capstones — 34 of the window's 46 merged PRs, in eight days.
- The plan then closed as delivered-as-descoped — Passes 0–2 (topics 1–33) shipped; Passes 3–5 (topics 34–94) transferred to a successor that turns it into a shared course library composed by four learning paths.
- Reader-facing UI: a resizable, scrollable docs sidebar, and a copy button on every code block — a shared web-ui primitive, live on ayokoding-www and pre-wired in ose-www.

🌐 Cross-repo

- [AI] merge is now the default. An agent merges its own PR once review cycles complete, zero CRITICAL/HIGH findings remain, the branch is current, and gates are green. Last week's update still described merging as the human's call. A follow-up sweep closed the guards that failed open under it.
- Orchestration formalized as N+1: one main thread plus N background agents, default N=3, DAG-first.
- rhino-cli stayed byte-identical across all three repos while gaining e2e scenario-coverage validation, Rule/Feature-level skip detection, and shared cargo target dirs with GC.
- ideas.md became plans/ideas/: two-pager briefs with a mandatory Prior art section, 22 backfilled.

🔧 The bug worth naming

The mermaid validator skipped any diagram whose first line was a %% comment — it read the comment as an unknown diagram type and bailed out. The repo's own convention mandates a %% comment for one exception case, and the shared color-palette header is a %% line. So 2,851 of 3,905 diagram blocks — 73%, across 637 files — passed without a single rule running. One-line fix, plus tests. It surfaced 665 violations here and 16 across the siblings; 45 fixed, and the remaining 636 — all in tutorial content — scoped behind a documented exclude and a filed brief.

A green check that never ran is worse than no check at all.

🏗️ ose-infra / 📦 ose-primer

Both took the same rhino-cli changes byte-for-byte, plus the governance update. ose-primer also de-flaked its Kotlin/Ktor CI build. The twin k3s clusters are still not up — the milestone has been open since Week 18.

🔜 Next 2–4 weeks

Ship a backend to the twin k3s clusters. Build the shared course library and path-aware navigation. Remediate the 636 diagram findings and drop the exclude.

Insha Allah.

- ose-public: https://github.com/wahidyankf/ose-public
- ose-primer: https://github.com/wahidyankf/ose-primer
- OrganicLever: https://www.organiclever.com/
- Updates: https://www.oseplatform.com/updates/
- Learning: https://www.ayokoding.com
