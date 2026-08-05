Posted: Monday, June 15, 2026
Platform: LinkedIn
Window: 2026-05-10 → 2026-06-15 (monthly). ~1,536 commits across the three repos (ose-public 855, ose-infra 388, ose-primer 293).

---

OPEN SHARIA ENTERPRISE
Week 30 / Phase 1, Week 18 — monthly update

This past month was about foundations — finding the patterns, architecture, and infrastructure — not shipping product. Highlights: the backends went F# → Java → Rust → back to F#; a clean -www / -app-web / -be naming split; app.organiclever.com got its first deploy on Vercel (not even alpha yet).

🌐 Cross-repo

- governance/ → repo-governance/ rename. Unified markdown gate (links, anchors, headings, mermaid) in one CI workflow.
- Cross-language lint gates — shellcheck, hadolint, actionlint at warning threshold, joining strict F#.
- Dependency policy clears CVEs vs five sources incl. CISA KEV + EPSS; exact pins throughout.
- Blameless post-mortem convention adopted across all three repos.

🌳 ose-public

The honest story: both backends churned through stacks — F#/Giraffe → Java/Spring → Rust/Axum — before settling back on F#/Giraffe (.NET 10, EF Core, DbUp, NATS.Net). The rule that emerged: Rust for the CLIs and lean infra; F#/.NET for the product backends. ose-app-be → the generic ose-be (now an ERP-direction backend); organiclever-be became a real backend; crane-cli reverted Rust → F# too.

Naming got legible — -www marketing/landing site, -app-web app client, -be backend. ose/ayokoding/wahidyankf -web → -www; OrganicLever split into marketing + app.

🏗️ ose-infra

The strategy: on-premise first. Cloud prices keep climbing and the IDR keeps weakening vs the USD, so self-hosting on hardware we own is the cost-driven default — expand to cloud as needed.

A "host unreachable" outage became a blameless post-mortem and a hardened two-node fleet: Wake-on-LAN, scheduled backups, watchdog, off-host alerting. A second self-hosted node came online, plus a Proxmox Datacenter Manager VM; twin k3s clusters (staging-1/prod-2) next.

📦 ose-primer

Absorbed the cross-cutting work across the polyglot demos — markdown gate, dependency hygiene, post-mortems, toolchain parity. Also dropped the Go rhino-cli for Rust, matching ose-public.

🔜 Next 2–4 weeks

Ship ose-be and organiclever-be to the on-premise k3s clusters — first backends in a real environment. Stand up staging + production k3s. Power is the honest risk; production moves to cloud/colocation as we grow.

Last month I said "all-in on Rust." This month I walked it back: Rust where I run it lean, F#/.NET where it earns its keep. The throughline — strong static typing as a deterministic guardrail, plus code a human can read: if an engineer can't read the patterns, don't expect an AI to write good code in them either.

Full write-up: https://www.oseplatform.com/updates/2026-06-15-phase-1-week-18-fsharp-backends-and-tier-split

Insha Allah.

- ose-public: https://github.com/wahidyankf/ose-public
- ose-primer: https://github.com/wahidyankf/ose-primer
- OrganicLever: https://www.organiclever.com/
- Updates: https://www.oseplatform.com/updates/
- Learning: https://www.ayokoding.com
