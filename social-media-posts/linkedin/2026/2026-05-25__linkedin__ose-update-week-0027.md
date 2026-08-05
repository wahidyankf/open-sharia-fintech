Posted: Monday, May 25, 2026
Platform: LinkedIn
Window: 2026-05-18 17:27 +0700 → 2026-05-25 17:25 +0700. ~351 commits across the three repos (ose-public 195, ose-primer 92, ose-infra 64).

---

OPEN SHARIA ENTERPRISE
Week 27 / Phase 1, Week 15

Highlights: the ose-projects parent repo is gone — ose-public, ose-primer, and ose-infra are now three independent siblings; rhino-cli finished its Go → Rust port across all three; Hugo removed; multi-harness support added (Amazon Q + a vendor-neutral binding layer).

🌐 Cross-repo

- ose-projects deleted. No more parent repo — the three now sit side by side as independent siblings. generated-socials moved into ose-public; ecosystem docs document ose-infra for the first time.
- rhino-cli: Go → Rust, with byte-identical parity verified via a shadow-diff harness. ose-public + ose-infra promote Rust to canonical (Go archived); ose-primer keeps both live (see below). Strict Rust 2024 baseline: forbid(unsafe_code), pedantic clippy, fmt/deny/msrv CI gates.
- Hugo removed everywhere; multi-harness compatibility added (Amazon Q bridge + parity guard; Codex/Copilot/Cursor documented); the sync script became the vendor-neutral generate:bindings; a new guardrail blocks agent access to .env\* files in all repos.

🌳 ose-public

rhino-cli was the bulk of the work — porting every command to Rust behind verified parity. ayokoding-web got a large learn-tree reorg: a new procedural architecture track, 4 security by-example tracks (~340 examples), plus coding-agents and Rust CLI tutorials. Governance: a uniform five-folder spec tree, the rust-governance audit closed out, and a new grill-me planning skill.

🏗️ ose-infra

rhino-cli Rust migration adapted for infra (plus infra-specific Java + contracts validators), and the same env-file, multi-harness, neutrality, and Hugo-removal passes.

📦 ose-primer

Unlike ose-public, the template deliberately keeps both rhino-cli-go and rhino-cli-rust live — Go is still a perfectly reasonable CLI choice, and a template is more useful showing both. Picked up the same neutrality, multi-harness, and guardrail work.

🔜 Next 2–4 weeks

With the tooling foundation settled, focus returns to product: deploy the first real backend for ose-public — ose-app-be (F#/Giraffe) shipped to production on the DDD + Hexagonal and TDD baselines. First time the platform moves from scaffolding to a running service. Let's see where it gets us.

On Rust: porting rhino-cli changed how I see the language. It reads more clearly to me than Go did, and that explicitness hands AI agents far stronger signals to reason from. Painful to write by hand, but that mostly disappears with an AI agent doing the heavy lifting. Not my strongest language yet by a large margin — but this window convinced me it's worth investing in. I'm even considering going all-in on Rust for the backend too. Let's see.

Insha Allah.

- ose-public: https://github.com/wahidyankf/ose-public
- ose-primer: https://github.com/wahidyankf/ose-primer
- OrganicLever: https://www.organiclever.com/
- Updates: https://www.oseplatform.com/updates/
- Learning: https://www.ayokoding.com
