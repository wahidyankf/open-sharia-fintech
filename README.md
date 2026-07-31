# 🌙 Open Sharia Enterprise

✨ An enterprise solutions platform for Sharia-compliant business systems.

🌐 **Live Sites**:

- **OSE Platform** ([oseplatform.com](https://oseplatform.com)) - Main platform website (under construction)
- **AyoKoding** ([ayokoding.com](https://ayokoding.com)) - Engineering research and learnings from this project, shared publicly as educational content
- **OrganicLever** ([organiclever.com](https://www.organiclever.com/)) - Marketing site for the
  active OrganicLever product workstream

## 🚧 Project Status

> ⚠️ **Pre-Alpha - In Development** - APIs and implementations may change significantly.
> **Contributions and pull requests are not being accepted** at this time.

**Current delivery focus: OrganicLever — local-first productivity tracker**

OrganicLever is the highest-priority product delivery workstream:

- 🌐 **Marketing site**:
  [organiclever.com](https://www.organiclever.com/)
  ([`organiclever-www`](./apps/organiclever-www/))
- 💻 **Product client**: [`organiclever-app-web`](./apps/organiclever-app-web/) — Next.js 16
  local-first web application
- 🔧 **Backend**: [`organiclever-be`](./apps/organiclever-be/) — F#/Giraffe/ASP.NET REST API

Research and prototyping for Shariah compliance, security, business systems, enterprise domains,
infrastructure, and public education can progress in parallel. Workstreams coordinate through
explicit dependencies and per-deliverable readiness checks instead of portfolio-wide stage
transitions.

**What to Expect:**

- 🔄 Breaking changes without notice
- 📐 Architecture still evolving
- 🧪 Experimental implementations

See the **[development roadmap](./roadmap.md)** for the concurrent workstreams, readiness model,
and strategy.

## 🚀 Getting Started

### 📋 Prerequisites

- **Node.js** 24.13.1 LTS & **npm** 11.10.1 (managed via [Volta](https://docs.volta.sh/guide/getting-started))

### 📥 Installation

```bash
npm install
```

## 🛠️ Tech Stack

**Guiding Principle**: Technologies that keep you free - open formats, portable data, no vendor lock-in.

**Established platform:**

- Node.js & npm (via Volta) - Tooling and development infrastructure
- Next.js 16 - Public websites and content platforms
- Rust - CLI tools ([ayokoding-cli](./apps/ayokoding-cli/),
  [rhino-cli](./apps/rhino-cli/), and [ose-cli](./apps/ose-cli/))
- F# - PDF-to-Markdown tooling and shared processing libraries

**Active OrganicLever product work:**

- Product client: Next.js 16 + TypeScript + PGlite
- Backend: F# + Giraffe + ASP.NET 10
- Data: Local-first PostgreSQL-WASM in the product client; PostgreSQL for backend integration
- Operations: Vercel deployment plus Kubernetes, observability, and reliability research

Technology choices belong to the initiatives that need them; no language or architecture is
reserved for a future project stage. See the **[development roadmap](./roadmap.md)** for details.

## 📂 Project Structure

This project uses **Nx** to manage applications and libraries:

```
open-sharia-enterprise/
├── apps/                  # Deployable applications (Nx monorepo)
├── libs/                  # Reusable libraries (Nx monorepo, flat structure)
├── docs/                  # Project documentation (Diataxis framework)
│   ├── tutorials/         # Learning-oriented guides
│   ├── how-to/            # Problem-oriented guides
│   ├── reference/         # Technical reference
│   └── explanation/       # Conceptual documentation
├── plans/                 # Project planning documents
│   ├── in-progress/       # Active project plans
│   ├── backlog/           # Planned projects for future
│   └── done/              # Completed and archived plans
├── nx.json                # Nx workspace configuration
├── tsconfig.base.json     # Base TypeScript configuration
├── package.json           # Project manifest with npm workspaces
└── README.md              # This file
```

**Applications** (`apps/`):

- **Public websites**: [`ose-www`](./apps/ose-www/),
  [`ayokoding-www`](./apps/ayokoding-www/),
  [`organiclever-www`](./apps/organiclever-www/), and
  [`wahidyankf-www`](./apps/wahidyankf-www/)
- **Product apps**: [`organiclever-app-web`](./apps/organiclever-app-web/),
  [`organiclever-be`](./apps/organiclever-be/), [`ose-app-web`](./apps/ose-app-web/), and
  [`ose-be`](./apps/ose-be/)
- **CLI and processing tools**: [`ayokoding-cli`](./apps/ayokoding-cli/),
  [`rhino-cli`](./apps/rhino-cli/), [`ose-cli`](./apps/ose-cli/), and
  [`crane-cli`](./apps/crane-cli/)
- **End-to-end suites**: see the [applications index](./apps/README.md) and
  [monorepo structure reference](./docs/reference/monorepo-structure.md)
- **Polyglot demo apps**: extracted 2026-04-18 to the downstream
  [`ose-primer`](https://github.com/wahidyankf/ose-primer) template repository, which is now
  authoritative for the polyglot showcase.

**Libraries** (`libs/`): Reusable shared code

**Learn More**: [Monorepo Structure Reference](./docs/reference/monorepo-structure.md) | [How to Add New App](./docs/how-to/add-new-app.md) | [How to Add New Library](./docs/how-to/add-new-lib.md) | [How to Run Nx Commands](./docs/how-to/run-nx-commands.md)

## 💻 Development

**Code Quality**: Automated checks run on every commit (Prettier formatting, Commitlint validation, markdown linting).

**Common Commands**:

```bash
npm run build                    # Build all projects
npm run test                     # Run tests
npm run lint                     # Lint code
nx dev [app-name]                # Start development server
nx build [app-name]              # Build specific project
nx affected -t build             # Build only affected projects
nx affected -t test:quick        # Run fast quality gate for affected projects
nx graph                         # Visualize dependencies
```

See [Code Quality](./repo-governance/development/quality/code.md) and [Commit Messages](./repo-governance/development/workflow/commit-messages.md) for details.

## 📊 CI & Test Coverage

All projects enforce ≥90% test coverage as part of `test:quick`.

**Quality gates**: pre-commit hooks (formatting, linting), pre-push hooks (`typecheck`, `lint`, `test:quick` for affected projects), and [PR quality gate](./.github/workflows/pr-quality-gate.yml).

- OSE Platform
  - [![Deploy](https://github.com/wahidyankf/ose-public/actions/workflows/ose-www-test-local-deploy-prod.yml/badge.svg)](https://github.com/wahidyankf/ose-public/actions/workflows/ose-www-test-local-deploy-prod.yml)
- AyoKoding
  - [![Deploy](https://github.com/wahidyankf/ose-public/actions/workflows/ayokoding-www-test-local-deploy-prod.yml/badge.svg)](https://github.com/wahidyankf/ose-public/actions/workflows/ayokoding-www-test-local-deploy-prod.yml)
- OrganicLever (app — staging)
  - [![Deploy](https://github.com/wahidyankf/ose-public/actions/workflows/organiclever-app-test-local-deploy-stag.yml/badge.svg)](https://github.com/wahidyankf/ose-public/actions/workflows/organiclever-app-test-local-deploy-stag.yml)
- Wahidyankf
  - [![Deploy](https://github.com/wahidyankf/ose-public/actions/workflows/wahidyankf-www-test-local-deploy-prod.yml/badge.svg)](https://github.com/wahidyankf/ose-public/actions/workflows/wahidyankf-www-test-local-deploy-prod.yml)
- [`rhino-cli`](./apps/rhino-cli/)

For polyglot demo app CI badges, see the [`ose-primer`](https://github.com/wahidyankf/ose-primer) repository.

## 📚 Documentation

Organized using the [Diátaxis framework](https://diataxis.fr/): [Tutorials](./docs/tutorials/) (learning), [How-To](./docs/how-to/) (problem-solving), [Reference](./docs/reference/) (lookup), [Explanation](./docs/explanation/) (understanding).

See [`docs/README.md`](./docs/README.md) for details.

## 🔗 Related Repositories

- **[`ose-primer`](https://github.com/wahidyankf/ose-primer)** — public, MIT-licensed template repository derived from `ose-public`. Packages scaffolding (governance, AI agents, skills, conventions, CI harness, polyglot demo apps) into a reusable starting point. `ose-public` is upstream source of truth; content parity with `ose-primer` is maintained manually via the multi-repo parity planning workflows. For the upstream/downstream relationship and license difference, see [Related Repositories reference](./docs/reference/related-repositories.md).

## 🎯 Motivation

Our mission is to democratize access to trustworthy, Sharia-compliant enterprise technology for organizations of all sizes, regardless of region or industry.

**The Opportunity:**

- Islamic enterprise (finance, commerce, cooperatives) is a multi-trillion dollar global market
- Existing platforms are proprietary, expensive, and domain-limited
- Most organizations rely on legacy systems retrofitted for Sharia compliance
- The gap: open-source, compliance-first solutions with radical transparency

**Our Approach:**

- Concurrent product, research, assurance, platform, and public-learning workstreams
- Progressive complexity within each initiative, based on evidence rather than a fixed sequence
- Explicit dependencies and readiness gates for every production-facing deliverable
- Sustainable prioritization based on user value, risk, capacity, and funding
- Sharia-compliance built in from the ground up, not bolted on after

**What We Believe:**

- 🕌 **Sharia-compliance as a foundation** - Built in from the ground up, not bolted on later
- 🔓 **Transparency builds trust** - Open source code enables community verification of Sharia compliance
- 🤖 **AI-assisted development** - Systematic use of AI tools to enhance productivity and code quality
- 🛡️ **Security and governance from day one** - Architectural foundations, not afterthoughts
- 📚 **Learning in public** - Share our research and knowledge through [ayokoding.com](https://ayokoding.com)
- 🏗️ **Long-term foundation over quick wins** - Building solid foundations for a life-long project

For complete principles, see [repo-governance/principles/](./repo-governance/principles/README.md).

## 🤝 Contributing

🔒 **Contributions are currently closed** while we stabilize the architecture and patterns.

🎉 **Forking is welcome!** Build your own version for your region or use case — once the foundation is solid, we'll open contributions to the community.

## 📜 License

This repository is licensed under the **[MIT License](./LICENSE)**. All code, documentation,
governance materials, specifications, and AI agent configuration are MIT-licensed — free to use,
fork, modify, and distribute for any purpose.

See [LICENSING-NOTICE.md](./LICENSING-NOTICE.md) for full details |
[LICENSE](./LICENSE) for the root license text |
[Licensing Convention](./repo-governance/conventions/structure/licensing.md) for internal rules.
