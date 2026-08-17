---
title: "Dependency Bump Stability & Safety Policy"
description: "Three-path decision tree (LTS, 60-day soak, security waiver) governing every dependency bump across the polyglot monorepo."
when_to_use: "Read this index to find the right Dependency Bump Stability & Safety Policy child document."
---

# Dependency Bump Stability & Safety Policy

- [Principles and Conventions Implemented](./01-principles-and-conventions-implemented.md) — The principles and companion conventions the Dependency Bump Stability & Safety Policy implements and respects. Use when tracing why the three-path decision tree and exact-pinning rules exist back to the principles and conventions they respect.
- [Scope](./02-scope.md) — The manifest types and version pins this policy covers, and the workspace-internal references, lockfiles, and type-only deps it excludes. Use when determining whether a specific manifest field or file falls under this policy.
- [Three-Path Decision Tree](./03-three-path-decision-tree.md) — The LTS, 60-day stable, and security-override waiver paths used to classify every dependency bump. Use when classifying which of the three paths applies to a specific package or runtime bump.
- [KEV Fast-Track and EPSS Escalation](./04-kev-fast-track-and-epss-escalation.md) — How a CISA KEV listing bypasses the 60-day soak and forces Path C, and how a high EPSS score flags a bump for expedited scheduling. Use when a CVE affecting the currently pinned version might be actively exploited, to decide whether to bypass the normal Path B soak window.
- [Selection Rules Within Every Path](./05-selection-rules-within-every-path.md) — The two rules — recency and functional stability — that narrow a chosen path's eligible versions down to the single version to pin. Use once a path (A, B, or C) is chosen, to select the exact version to pin from that path's eligible set.
- [Pinning Policy (Hard Rule)](./06-pinning-policy-hard-rule.md) — The required exact-pin form for every manifest type — npm, Cargo, .NET, Dockerfile, GitHub Actions — and the caret/tilde verification command. Use when writing or reviewing a version string in any manifest to confirm it is an exact pin.
- [CVE Clearance Process (Mandatory for Every Bump)](./07-cve-clearance-process.md) — The five sources every selected version must be checked against, the EPSS recording requirement, and the four clearance status values. Use after selecting a version for any path, to clear it against all CVE sources and record its clearance status.
- [Cutoff Date Computation and Plan Duration](./08-cutoff-date-computation-and-plan-duration.md) — How to state the Path B cutoff date in writing, and why a plan spanning more than 60 days must re-run the eligibility check. Use when computing the 60-day cutoff for a bump, or when a plan with dependency bumps has been open longer than 60 days.
- [Examples](./09-examples.md) — Worked examples of Path A (LTS), Path B (60-day eligible), and Path C (security waiver) decisions. Use as a reference when classifying a real bump into Path A, B, or C.
- [Application Workflow](./10-application-workflow.md) — The twelve-step ordered procedure for proposing or executing a dependency bump, from classification through quality gates. Use as the step-by-step checklist when proposing or executing any dependency bump.
- [Tools, Automation, and References](./11-tools-automation-and-references.md) — The tools and feeds that automate this policy, and the full set of related conventions, principles, and external references. Use when looking up which tool enforces a specific part of this policy, or when tracing a related convention, principle, or external database.
