Posted: Monday, June 22, 2026
Platform: LinkedIn
Window: 2026-06-15 → 2026-06-22 18:51 +0700. ~333 commits across the three repos (ose-public 241, ose-primer 51, ose-infra 41).

---

OPEN SHARIA ENTERPRISE
Week 31 / Phase 1, Week 19

Highlights: the week's focus was a repeatable workflow for Web UI development — yielding three live-site testers, one orchestrating workflow, and a 15-rule delivery-hardening convention, after UI shipped past green gates.

🌐 Cross-repo

- OSE is now MIT-licensed — genuinely open source, not "source-available." Footer labels corrected across all three repos.
- User-Facing Delivery Hardening (15 rules) propagated to all three repos, born from a post-mortem of UI shipped broken past a green gate.
- Repeatable Web UI dev workflow — web-ux-test-fixing-planning — orchestrates the new three-tester triad (web-exploratory-tester, web-usability-tester, web-design-tester), turning live-site findings into one fix-ready plan.
- Governance: one-Gherkin-per-TDD-cycle; integration tier = app-tier only; regression-test mandate; UI-mockup-in-plan convention; CI poll cadence 2 minutes.

🌳 ose-public

Headline build: ayokoding-www cost-of-living and salary-savings calculator — FX + city cost data, salary-to-savings modeling, minimum-role reverse lookup, dual-currency display, household scaling, foreigner school eligibility by country, URL-as-state for shareable links. Multiple exploratory, usability, and design-tester rounds before release. Live: https://www.ayokoding.com/en/tools/cost-of-living-calculator

Navigation overhauled: /c content URL namespace with 308 redirects, global header/footer/mobile nav, landing homepage, breadcrumbs, locale-aware copy (English/Indonesian).

Shared design system: libs/web-ui with brand CSS token sheets and Storybook on Vercel. Functional core / imperative shell adopted across the three web frontends.

🏗️ ose-infra

Governance parity synced. CI fixes: Rust installed in the TypeScript quality gate; per-language gates scoped to tagged affected projects. A false-outage post-mortem documented (alert fired; host was healthy). k3s clusters remain planned, not shipped.

📦 ose-primer

Polyglot demo-app CI restored: contract-codegen fixed across .NET, Elixir, Go, Rust, Dart, and TypeScript; a CVE pin (CVE-2025-6965). MIT relabel and governance parity propagated.

🔜 Next 2–4 weeks

Stand up staging and production k3s clusters and ship the F# backends (ose-be, organiclever-be) to a real environment — still the open goal. Power remains the honest risk; production may move to cloud or colocation as it grows. Keep hardening the ayokoding-www UI through the three-tester + rule-15 retest loop.

I built real UI, shipped some of it broken past green gates, then turned that into a third live-site tester, a 15-rule delivery-hardening convention, and a near-end retest loop. OSE is now properly MIT.

Insha Allah.

- ose-public: https://github.com/wahidyankf/ose-public
- ose-primer: https://github.com/wahidyankf/ose-primer
- OrganicLever: https://www.organiclever.com/
- Updates: https://www.oseplatform.com/updates/
- Learning: https://www.ayokoding.com
