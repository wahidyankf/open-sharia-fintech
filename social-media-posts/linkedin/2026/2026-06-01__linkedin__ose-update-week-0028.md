Posted: Monday, June 1, 2026
Platform: LinkedIn
Window: 2026-05-25 17:25 +0700 → 2026-06-01 20:15 +0700. ~205 commits across the three repos (ose-public 113, ose-primer 40, ose-infra 52).

---

OPEN SHARIA ENTERPRISE
Week 28 / Phase 1, Week 16

Highlights: the backend went all-in on Rust; the whole codebase adopted Hexagonal + DDD with OpenAPI contract-first; the planning system got an overhaul; and ose-infra moved CI off my Mac onto self-hosted Proxmox runners.

🌐 Cross-repo

- Hexagonal + DDD bounded-contexts adopted everywhere — every backend, frontend, and CLI across the three repos now shares the same domain/application/infrastructure layering. Plus OpenAPI contract-first with codegen drift enforcement: generated clients must match the spec or CI fails.
- Planning system overhaul: a grill-me skill that interrogates a plan before I commit, a repo-setup-manager for clean baselines, a hard TDD Red→Green→Refactor rule, [AI]/[HUMAN] executor tags, and per-phase gates. Plans are executable checklists now, not prose.
- New hard iron rule in every repo: no secrets in any git-tracked file, ever. Inactive languages (JVM, Elixir, Clojure, Dart, Python) swept out of governance and tooling.

🌳 ose-public

The backend committed to Rust: ose-app-be reset from F# to a Rust/Axum scaffold, and organiclever-be migrated off Java/Maven to Rust/Axum (cucumber-rs BDD, 98% coverage). The CLI Rust sweep finished too — ose-cli and ayokoding-cli rewritten in Rust on a shared rust-commons crate, the old Go libs deleted; crane-cli alone reverted to F# for .NET interop.

🏗️ ose-infra

The big move: CI no longer runs on my Mac — retired it and stood up self-hosted runners on Proxmox VMs, then committed a scrubbed on-premise IaC tree — Terraform + Ansible, secrets gitignored — with a fresh C4 model. coralpolyp got the same hexagonal/DDD + contract-first treatment.

📦 ose-primer

The template absorbed the planning overhaul, hexagonal/DDD layers across all 11 backend demos, and the contract-first conventions. Plus a dependency-hygiene pass: exact-version pinning across the board and a CVE-free polyglot toolchain.

🔜 Next 2–4 weeks

Expand the on-premise cluster: bring up staging and production k3s beside the CI runners. Proxmox is much cheaper than the cloud right now — with the IDR weakening against the USD and hardware prices climbing, it's the sane call, and Rust backends keep the footprint and the bill small. The real risk is power: a blackout here isn't unlikely, so production moves incrementally to the cloud — or proper datacenter colocation with a DR site — as we grow. On-prem first for now — first tenant is ose-app-be, the platform's first running service.

Last week I was "considering" going all-in on Rust; this week I stopped considering — ose-app-be and organiclever-be flipped off F#/Java, crane-cli went back to F#. Not indecision: Rust for services I run and scale, .NET where it earns its keep.

Insha Allah.

- ose-public: https://github.com/wahidyankf/ose-public
- ose-primer: https://github.com/wahidyankf/ose-primer
- OrganicLever: https://www.organiclever.com/
- Updates: https://www.oseplatform.com/updates/
- Learning: https://www.ayokoding.com
