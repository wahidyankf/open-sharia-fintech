Posted: Sunday, April 12, 2026
Platform: LinkedIn

---

OPEN SHARIA ENTERPRISE
Week 21 / Phase 1, Week 9

This week: parent coordination repo born, self-hosted CI runner live in ose-infra, 304 docs files renamed to kebab-case in ose-public, ose-infra shed its non-infra apps — and a hard lesson in multi-repo AI cost.

What changed:

🏗️ Parent Coordination Repo Live
ose-projects went from empty to fully operational this week. 15 cross-repo AI agents cover the full plan lifecycle, two governance-sync lanes (ose-public → ose-infra, ose-public → parent), and repo governance validation. Subrepo worktree workflow, parent Nx workspace, Diátaxis docs, and generated-socials all landed. Both ose-projects and ose-infra are private — coordination layers tend to accumulate sensitive information, accidentally or otherwise.

⚙️ Self-Hosted CI Runner Live (ose-infra)
All ose-infra CI workflows now run on a self-hosted ARM64 Linux runner — Java 21 + Maven, Flutter 3.41.6, Elixir, Go, TypeScript, and more baked into the image. Fixed Docker socket-mount incompatibilities with Mac Docker Desktop. Smoke test PR merged.

Why self-hosted? GitHub-hosted runner costs on the public ose-public repo hit nearly $80 USD in just the first 12 days of April. The self-hosted runner runs on my home server — isolated in Docker — at "zero" marginal cost.

🗂️ ose-infra Scope Reset
ayokoding, oseplatform, and organiclever apps removed from ose-infra — keeping it strictly about infrastructure. Governance sync now uses working-tree copy instead of an upstream remote.

📁 ose-public: Obsidian Out, Kebab-Case In
304 files renamed to kebab-case. Obsidian vault deleted. rhino-cli's validate-naming removed. File-naming convention rewritten on standard-markdown and GitHub norms. AI agent model tiers right-sized: 8 downgraded Opus→Sonnet, 1→Haiku.

💡 Multi-Repo Lesson Learned
Working across three repos isn't just a tooling problem — it's a coherence problem. Without explicit sync and anti-drift mechanisms, repos silently diverge. That's what governance-sync lanes and the parent coordination layer exist to solve.

The cost side hit harder than expected. I burned 40% of my Claude Max $200/month weekly quota in under 18 hours — running Opus on multi-repo sessions. The model has to hold three codebases worth of context simultaneously, and at Opus pricing that compounds fast. Switching back to Sonnet in the meantime. Next week I'm exploring token-preservation strategies and better interaction patterns for multi-repo work. Two tools on my radar: Caveman (https://github.com/JuliusBrussee/caveman) and RTK (https://www.rtk-ai.app/). Still figuring out the right mental model here.

🔜 What's next:
CD pipelines are on hold. Before going deeper into multi-repo infra work, I need to solve the token cost and interaction pattern problem first — otherwise the burn rate makes the pace unsustainable. Insha Allah.

GitHub: https://github.com/wahidyankf/ose-public
Updates: https://www.oseplatform.com/updates/
Learning: https://www.ayokoding.com/
