Posted: Sunday, April 26, 2026
Platform: LinkedIn

---

OPEN SHARIA ENTERPRISE
Week 23 / Phase 1, Week 11

This week: ose-public back to MIT, organiclever local-first pivot completed, ts-ui design system + wahidyankf-web migration shipped, rhino-cli mermaid validator propagated, quality gates standardized across all four repos.

🌐 Cross-repo

- ⚖️ License: FSL-1.1-MIT → MIT (ose-public + wahidyankf-web). Friction-free for any use.
- 🦏 rhino-cli mermaid validator built in ose-public; ported to ose-infra + ose-primer; adopted by parent.
- ✅ Quality gates standardized: strict mode + max-iterations=7 default; new quality-gate, GitHub-CI, post-push verification conventions.
- 🔀 Worktree push default = direct to main, per Trunk-Based Development.
- 📵 No-date metadata: manual "Created:" / "Last Updated:" rows banned — git already knows.

🌳 ose-public (public, MIT) — main product monorepo; Phase 1 OrganicLever + AyoKoding

- 🔓 organiclever local-first pivot completed. Google auth + DB plumbing removed across web, BE, e2e, specs, contracts, C4, GHA. Initial schema migration dropped.
- 🚦 organiclever CI staging split: development + staging + production replace test-and-deploy. Vercel Protection Bypass.
- 🧪 organiclever.com landing page — my first Claude Design experiment.
- 🏷️ "organiclever-fe*" → "organiclever-web*" rename.
- 🎨 ts-ui design system: AppHeader, Sheet, Toggle, Icon, HuePicker, InfoTip, StatCard, TabBar, SideNav, ProgressRing, Badge, Textarea + alert/button variants. OKLCH tokens.
- 🚚 wahidyankf-web → ts-ui: HighlightText, ScrollToTop, SearchComponent, ThemeToggle moved to shared lib. Docker Turbopack hardened.
- 🚮 Codecov removed end-to-end.
- 📚 ayokoding: "Lisp interpreter" 6-part series in Go and F# + compilers-and-interpreters section.

🏗️ ose-infra (private) — infra monorepo; self-hosted CI, coralpolyp app

- 🦏 Ported rhino-cli mermaid validator into pre-push; doc violations swept.

📦 ose-primer (public, MIT) — template fork of ose-public

- 🏷️ "demo-_" → "crud-_" across Elixir, F#, C#, Fullstack templates. Clarifies the CRUD family scope.
- 📐 Mermaid width constraint governance (MaxWidth=4) + doc sweep.
- ⏰ Weekly test-crud schedule (Friday 5 pm WIB).

🏠 ose-projects (private) — parent coordination; tracks the other three as gitlinks

- 🦏 rhino-cli + golang-commons adopted into apps/ + libs/. Pre-commit + pre-push wired.

🛠️ Tools: RTK (https://www.rtk-ai.app/) — 19.6M tokens saved across 15K commands (98% on git push, 25% on read). Caveman (https://github.com/JuliusBrussee/caveman) full mode keeps long sessions tight.

🔜 Next week (main focus):

- ose-primer: "chat with PDF" demo app using multiple LLM models.
- ose-public: continue experimenting with local-first web app.

Insha Allah.

- ose-public: https://github.com/wahidyankf/ose-public
- ose-primer: https://github.com/wahidyankf/ose-primer
- OrganicLever: https://www.organiclever.com/
- Updates: https://www.oseplatform.com/updates/
- Learning: https://www.ayokoding.com/
