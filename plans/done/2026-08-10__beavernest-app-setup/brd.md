# Business Requirements Document — BeaverNest App Setup

## Business Goal

Turn the BeaverNest hello-world quad into the smallest durable, privately reachable application
foundation that can safely support later assistant and content features without operating public
web infrastructure.

## Rationale

[Repo-grounded] BeaverNest's product vision describes a self-owned personal operating layer, while
the current runtime is stateless and its frontend is a promotional hello-world page. The current
architecture cannot retain future workspace state and carries server-rendering/runtime machinery
that provides no value for a private application with no marketing site.

[Judgment call] The expected audience is one person or a small trusted group on an existing VPN. A
single-host SQLite system and browser-rendered SPA therefore match the actual scale and trust
boundary with less operational machinery than a public multi-tier deployment or client/server ORM.

## Business Impact

- The maintainer receives a durable local application boundary rather than a disposable demo.
- Trusted VPN peers can reach one address-scoped endpoint without learning backend ports or Docker
  DNS.
- Later feature plans inherit explicit persistence, migration, backup, health, and test seams without
  prematurely inheriting a domain schema.
- Removing SSR and the standalone frontend server reduces the number of production runtime
  processes to operate.
- Technology-neutral real-database testing guidance prevents canonical documentation from
  contradicting SQLite-backed projects.

## Affected Roles

| Role                        | Need                                                                                          |
| --------------------------- | --------------------------------------------------------------------------------------------- |
| Maintainer as operator      | One private Compose service, transparent data location, safe restart, and recoverable backups |
| Maintainer as product owner | An application home rather than promotional content, without speculative product features     |
| Trusted VPN peer            | A responsive, accessible shared workspace status screen with clear degraded states            |
| Executing agents            | Exact file paths, commands, Gherkin bindings, and safe data-handling boundaries               |
| Future feature makers       | A small explicit SQL seam and real SQLite test harness, not an ORM-imposed domain model       |
| Review/checker agents       | Canonical governance, specs, contracts, code, and runtime behavior that agree                 |

These are operating hats and plan consumers, not approval authorities. PR review is the repository's
approval mechanism.

## Business-Level Success Metrics

All metrics are observable facts; no measured baseline or fabricated percentage is claimed.

- The production Compose rendering publishes exactly one application port on the configured VPN
  host address and publishes no separate backend port.
- The final runtime process list contains one BeaverNest application container, excluding one-shot
  operator commands used for backup or verification.
- A repository search finds no active BeaverNest documentation that calls `/` a promotional landing
  page or describes the frontend as server-rendered.
- A repository search finds no ORM package in the BeaverNest backend manifests and no domain table
  in the foundation migration set.
- Every current BeaverNest project passes its applicable Nx quick, integration, E2E, and companion
  spec gates.
- A backup created while the application is running passes both SQLite integrity and foreign-key
  validation, and a restore returns the application to ready state.

## Business-Scope Non-Goals

- This plan does not make BeaverNest a multi-tenant or public SaaS product.
- It does not define the first assistant/content feature or any product-data shape.
- It does not provide confidentiality between trusted VPN peers.
- It does not provision or administer the VPN, host firewall, certificates, DNS, or host backup
  scheduler.
- It does not promise horizontal scaling; one writable backend process owns one local SQLite file.

## Business Risks and Mitigations

| Risk                                                                | Impact                                          | Mitigation                                                                                                                            |
| ------------------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| VPN access is mistaken for per-user authorization                   | Every admitted peer can view future shared data | State the shared-workspace trust model in UI/operator docs; block account semantics from this plan                                    |
| A repository/worktree cleanup removes personal data                 | Irrecoverable local data loss                   | Require an operator-owned host directory outside the repo; reject missing mount paths; remove destructive restart scripts             |
| SQLite is later stretched beyond one-host/small-group constraints   | Lock contention or unsafe storage topology      | Document one writer/one host/no network filesystem; test busy timeout and revisit only from measured need                             |
| Infrastructure schema becomes speculative product schema            | Future features inherit accidental abstractions | Persist only the DbUp journal; create domain tables only with the feature that needs them                                             |
| “Less magic” is undermined by an ORM                                | Hidden queries and mapping behavior             | Prohibit ORM dependencies; use DbUp for explicit SQL migrations and direct parameterized SQL for readiness                            |
| HTTP is published on unintended host addresses                      | Private workspace traffic becomes visible       | Publish only on the exact VPN host IP, reject wildcard publication, inspect sockets, and document that source ACLs remain external    |
| A same-disk backup is mistaken for host-loss protection             | Data remains vulnerable to host/disk failure    | Validate the backup, then require operator attestation that a copy resides on independent/off-host storage; scheduling stays external |
| General governance edit unintentionally weakens PostgreSQL projects | Other apps receive poorer test coverage         | Require each app's real production database; retain PostgreSQL and SQLite manifestations and checker examples                         |
