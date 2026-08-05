Posted: Sunday, July 6, 2026
Platform: LinkedIn
Window: 2026-06-29 18:00 +0700 → 2026-07-07 +0700. ~365 commits across the three repos (ose-public 189, ose-primer 107, ose-infra 69).

---

OPEN SHARIA ENTERPRISE

Week 33 / Phase 1, Week 21

Highlights: the biggest scenario-coverage push yet — every app and library across all three repos now has its Gherkin tree level-tagged and traced to real code, alongside execution of the rhino-cli SDLC parity plan and a new default delivery mode for reaching main.

🌐 Cross-repo

- Scenario coverage: every Gherkin scenario now carries a test-level tag and a @covers marker linking it to implementing code. Hollow BDD harnesses were replaced with real frameworks — cucumber-rs, vitest-cucumber, TickSpec, Kaocha, cabbage/gherkin — and fail-on-skip guards block silently-skipped scenarios everywhere. rhino-cli gained a runtime cross-check validating coverage against execution.
- rhino-cli SDLC parity executed: verb-last commands, three config files merged into one repo-config.yml, Codecov retired for native coverage, canonical CLI and Gherkin tree byte-identical across all three repos.
- Knowledge Capture made mandatory: every plan closes with a phase triaging its learnings into a home or discarding them.
- worktree-to-pr is now the default delivery mode, paired with a new pr-review maker-fixer cycle; merging to main stays human-only.
- OpenCode model mapping refreshed to current tiers (glm-5.2 thinking/execution, minimax-m3 fast).

🌳 ose-public

Coverage closed out across rust-commons, web-ui, crane-cli, ose-cli, ayokoding-cli, and every -www/-be/-app-web pair. fsharp-crane-core moved to TickSpec, the CLIs' links-check specs moved to cucumber-rs, web-ui's token spec moved to vitest-cucumber, and wahidyankf-www's hollow BDD steps got activated with real assertions.

🏗️ ose-infra

The canonical rhino-cli and Gherkin tree were regenerated from ose-public and re-licensed MIT, converging CLI verbs and env-guards with public and primer. CI fixes: setup-jvm added to compat-min-version, a missing setup-node step restored, a broken staging schedule disabled. coralpolyp-be gained compat/audit coverage plus Rust edition 2024; a new backlog plan tracks runner-fleet health.

📦 ose-primer

Coverage landed across every polyglot demo variant — all eleven CRUD backends (Rust, C#, Clojure, Elixir, F#, Go, Java, Kotlin, Python, TypeScript) and their frontends got shared Gherkin trees tagged and @covers-marked. Elixir and Clojure libraries moved off stub BDD onto real frameworks, with fail-on-skip guards everywhere.

🔜 Next 2–4 weeks

With coverage now uniform across all three repos, focus shifts to using the worktree-to-pr default and pr-review cycle in practice. k3s cluster standup and F# backend deployment remain the open milestone.

Consistency compounds: once every repo enforces the same bar, the next feature costs less to verify than the last one did.

Insha Allah.

- ose-public: https://github.com/wahidyankf/ose-public
- ose-primer: https://github.com/wahidyankf/ose-primer
- OrganicLever: https://www.organiclever.com/
- Updates: https://www.oseplatform.com/updates/
- Learning: https://www.ayokoding.com
