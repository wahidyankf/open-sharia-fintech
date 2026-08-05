Posted: Monday, July 13, 2026
Platform: LinkedIn
Window: 2026-06-16 → 2026-07-13 (monthly). ~717 commits across the three repos (ose-public 427, ose-primer 166, ose-infra 124).

---

OPEN SHARIA ENTERPRISE
Week 34 / Phase 1, Week 22 — monthly update

Highlights: near-zero new product surface, still one of the month's most consequential stretches — rhino-cli went byte-identical, hollow Gherkin specs got rewired onto real BDD harnesses, delivery moved behind pull requests by default, and a post-mortem-born tester triad gated the one thing that shipped to users.

🌐 Cross-repo

- rhino-cli converged into one byte-identical tool across all three repos — consistent commands, one repo-config.yml, one Nx target set — now a formal SDLC Gate Standard; ose-infra's copy relicensed MIT to preserve identity.
- Hollow Gherkin stubs that passed by asserting nothing were replaced with real, per-language BDD harnesses plus @covers traceability and fail-on-skip guards — a green spec can no longer lie.
- worktree-to-pr is now the default delivery mode, with a pr-review maker-fixer cycle and mandatory Knowledge Capture — "done" (a green, reviewed PR) isn't "merged" (the human's schedule).
- Amazon Q Developer joined as a third agent-harness binding from the same .claude/ source; OpenCode models refreshed to glm-5.2 and minimax-m3.

🌳 ose-public

A blameless post-mortem found a UI change had shipped past every green gate because the gates checked stub specs, not the rendered page. The fix: a live-site tester triad (exploratory, usability, design) plus an api-exploratory-tester, and a hardening convention now at sixteen rules — one forcing a near-end browser retest before any UI plan closes. First workout: a cost-of-living calculator and IA navigation revamp went live on ayokoding.com, this month's one user-facing ship.

🏗️ ose-infra

Twin-k3s deploy plans were sharpened — right-sized capacity, corrected figures, Tailscale SSH — plus a runner health-monitoring plan and a post-mortem on a false observer-side outage. coralpolyp moved to Rust edition 2024; clusters aren't up yet, and no backend runs in a real environment.

📦 ose-primer

Green CI restored across all eleven polyglot demo backends and frontends after fixing contract-codegen races across Dart, Elixir, .NET, and Rust; the same de-hollowing pass, Rust edition 2024, and 103 resolved orphaned docs bring the template to this repo's bar.

🔜 Next 2–4 weeks

Ship a backend to the twin k3s clusters — the pending milestone since Week 18. Turn the new "Fundamentally Strong Software Engineer" 94-topic curriculum into real content for ayokoding-www. Exercise worktree-to-pr and the PR-review cycle in practice, and route more routine work to cheaper models.

The guardrails are the product until the product exists.

Full write-up: https://www.oseplatform.com/updates/2026-07-13-phase-1-week-22-hardening-the-substrate

Insha Allah.

- ose-public: https://github.com/wahidyankf/ose-public
- ose-primer: https://github.com/wahidyankf/ose-primer
- OrganicLever: https://www.organiclever.com/
- Updates: https://www.oseplatform.com/updates/
- Learning: https://www.ayokoding.com
