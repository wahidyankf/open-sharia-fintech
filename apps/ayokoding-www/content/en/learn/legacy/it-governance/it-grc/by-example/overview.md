---
title: "Overview"
weight: 10000000
date: 2026-05-21T00:00:00+07:00
draft: false
description: "IT-GRC by example — 85 annotated governance scenarios for software engineers without prior GRC background, covering frameworks, risk, compliance, and strategic IT governance"
tags: ["it-grc", "it-governance", "cobit", "itil", "risk-management", "compliance", "by-example", "scenario-by-example"]
---

**IT governance shapes every technology decision you make at work** — which projects get funded,
how changes are approved, why auditors want evidence of your controls. This by-example guide
teaches IT Governance, Risk and Compliance through 85 annotated real-world scenarios, built
for software engineers without prior GRC experience.

## Why Software Engineers Need This

Every engineer eventually encounters IT governance:

- An architect review board rejects your design — governance
- A CAB blocks your deployment — change governance
- An auditor asks for evidence of access reviews — compliance
- A compliance questionnaire lands on your team — regulatory governance
- A vendor is onboarded and you need a security assessment — third-party governance

Understanding how these systems work makes you a faster, more credible contributor in every one
of these situations — and a stronger candidate for tech lead, staff engineer, and platform roles.

## What Is IT-GRC By-Example Learning?

IT-GRC by-example uses the Scenario By-Example format —
each example is an annotated governance artifact (risk register, policy excerpt, COBIT objective,
audit finding, board report) with `# =>` comments explaining the reasoning, trade-off, and
decision rationale behind every element.

This is not code. The artifacts are:

- YAML-formatted governance documents (risk registers, maturity assessments, charters)
- Markdown tables (RACI matrices, compliance mappings, KPI dashboards)
- Policy excerpts (IT policies, SLAs, treatment plans)

## Learning Progression

| Level            | Engineer Context                             | What You Learn                                                                                                                                 |
| ---------------- | -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Beginner**     | "I want to understand what IT governance is" | Governance vs management, COBIT 2019, ISO 38500, risk basics, control types, policy hierarchy, audit fundamentals                              |
| **Intermediate** | "I need to apply frameworks in my org"       | COBIT objectives, ITIL 4/V5, ISO 27001 SoA, NIST CSF 2.0, FAIR quantification, DORA basics, board reporting                                    |
| **Advanced**     | "I lead or influence governance programs"    | Operating model design, AI governance (ISO 42001, EU AI Act), DORA compliance, ERM integration, continuous compliance, transformation programs |

## Prerequisites

- Basic familiarity with organizational structures (you have worked in a company)
- No prior GRC, audit, or compliance background required
- No coding or technical setup needed

## Frameworks Covered

| Framework        | Version                       | Domain                           |
| ---------------- | ----------------------------- | -------------------------------- |
| COBIT 2019       | Current (ISACA)               | IT governance and management     |
| ISO/IEC 38500    | 2024 edition                  | IT governance principles         |
| ISO 31000        | 2018 edition                  | Risk management                  |
| ITIL 4 / ITIL V5 | V5 launched Feb 2026          | IT service management governance |
| NIST CSF         | 2.0 (Govern function)         | Cybersecurity governance         |
| ISO/IEC 42001    | 2023 edition                  | AI management system             |
| NIST AI RMF      | 1.0                           | AI governance                    |
| DORA             | In force Jan 2025             | EU financial sector resilience   |
| COSO ICIF        | 2013 + Feb 2026 AI supplement | Internal control                 |

## Structure of Each Example

Every example follows the five-part scenario-by-example format:

1. **What This Covers** — what governance concept and why it matters (2-3 sentences)
2. **Scenario** — fictional organization type, size, and decision-maker role
3. **Annotated Artifact** — YAML, table, or policy excerpt with `# =>` annotations explaining reasoning
4. **Key Takeaway** — core governance insight (1-2 sentences)
5. **Why It Matters** — production relevance (50-100 words)

## Examples by Level

### Beginner (Examples 1–28)

- [Example 1: What Is IT Governance](/en/learn/it-governance/it-grc/by-example/beginner#example-1-what-is-it-governance)
- [Example 2: Governance vs Management — The COBIT Distinction](/en/learn/it-governance/it-grc/by-example/beginner#example-2-governance-vs-management--the-cobit-distinction)
- [Example 3: COBIT 2019 — Six Governance Principles](/en/learn/it-governance/it-grc/by-example/beginner#example-3-cobit-2019--six-governance-principles)
- [Example 4: COBIT 2019 — Five Domains](/en/learn/it-governance/it-grc/by-example/beginner#example-4-cobit-2019--five-domains)
- [Example 5: ISO/IEC 38500:2024 — Six Principles of IT Governance](/en/learn/it-governance/it-grc/by-example/beginner#example-5-isoiec-385002024--six-principles-of-it-governance)
- [Example 6: ISO 31000:2018 — Risk Management Lifecycle](/en/learn/it-governance/it-grc/by-example/beginner#example-6-iso-310002018--risk-management-lifecycle)
- [Example 7: ITIL 4 Service Value System Overview](/en/learn/it-governance/it-grc/by-example/beginner#example-7-itil-4-service-value-system-overview)
- [Example 8: IT Governance Committee Structure](/en/learn/it-governance/it-grc/by-example/beginner#example-8-it-governance-committee-structure)
- [Example 9: IT Governance Roles — RACI Matrix](/en/learn/it-governance/it-grc/by-example/beginner#example-9-it-governance-roles--raci-matrix)
- [Example 10: IT Policy Hierarchy](/en/learn/it-governance/it-grc/by-example/beginner#example-10-it-policy-hierarchy)
- [Example 11: Writing an IT Policy — Acceptable Use Policy](/en/learn/it-governance/it-grc/by-example/beginner#example-11-writing-an-it-policy--acceptable-use-policy)
- [Example 12: Information Asset Classification](/en/learn/it-governance/it-grc/by-example/beginner#example-12-information-asset-classification)
- [Example 13: IT Risk Identification — Starter Risk Register](/en/learn/it-governance/it-grc/by-example/beginner#example-13-it-risk-identification--starter-risk-register)
- [Example 14: IT Risk Assessment — 5×5 Matrix](/en/learn/it-governance/it-grc/by-example/beginner#example-14-it-risk-assessment--55-matrix)
- [Example 15: Risk Treatment Options](/en/learn/it-governance/it-grc/by-example/beginner#example-15-risk-treatment-options)
- [Example 16: Writing a Risk Treatment Plan](/en/learn/it-governance/it-grc/by-example/beginner#example-16-writing-a-risk-treatment-plan)
- [Example 17: Control Objectives — What They Are](/en/learn/it-governance/it-grc/by-example/beginner#example-17-control-objectives--what-they-are)
- [Example 18: Control Types](/en/learn/it-governance/it-grc/by-example/beginner#example-18-control-types)
- [Example 19: Control Testing — Design vs Effectiveness](/en/learn/it-governance/it-grc/by-example/beginner#example-19-control-testing--design-vs-effectiveness)
- [Example 20: IT Audit Basics — Scope, Objectives, Evidence](/en/learn/it-governance/it-grc/by-example/beginner#example-20-it-audit-basics--scope-objectives-evidence)
- [Example 21: Audit Findings — The 4Cs](/en/learn/it-governance/it-grc/by-example/beginner#example-21-audit-findings--the-4cs)
- [Example 22: Compliance Framework Overview](/en/learn/it-governance/it-grc/by-example/beginner#example-22-compliance-framework-overview)
- [Example 23: IT Governance Metrics — KPIs](/en/learn/it-governance/it-grc/by-example/beginner#example-23-it-governance-metrics--kpis)
- [Example 24: Service Level Agreement Writing](/en/learn/it-governance/it-grc/by-example/beginner#example-24-service-level-agreement-writing)
- [Example 25: IT Governance Maturity Model](/en/learn/it-governance/it-grc/by-example/beginner#example-25-it-governance-maturity-model)
- [Example 26: IT Governance Stakeholder Communication](/en/learn/it-governance/it-grc/by-example/beginner#example-26-it-governance-stakeholder-communication)
- [Example 27: IT Governance Charter](/en/learn/it-governance/it-grc/by-example/beginner#example-27-it-governance-charter)
- [Example 28: IT Investment Decision Framework](/en/learn/it-governance/it-grc/by-example/beginner#example-28-it-investment-decision-framework)

### Intermediate (Examples 29–57)

- [Example 29: COBIT 2019 Gap Analysis — EDM01](/en/learn/it-governance/it-grc/by-example/intermediate#example-29-cobit-2019-gap-analysis--edm01)
- [Example 30: COBIT 2019 APO12 — Risk Management Objective](/en/learn/it-governance/it-grc/by-example/intermediate#example-30-cobit-2019-apo12--risk-management-objective)
- [Example 31: COBIT 2019 BAI06 — Change Management Objective](/en/learn/it-governance/it-grc/by-example/intermediate#example-31-cobit-2019-bai06--change-management-objective)
- [Example 32: COBIT 2019 MEA01 — Monitoring Performance](/en/learn/it-governance/it-grc/by-example/intermediate#example-32-cobit-2019-mea01--monitoring-performance)
- [Example 33: ITIL 4 — Change Enablement Practice](/en/learn/it-governance/it-grc/by-example/intermediate#example-33-itil-4--change-enablement-practice)
- [Example 34: ITIL 4 — Incident Management Practice](/en/learn/it-governance/it-grc/by-example/intermediate#example-34-itil-4--incident-management-practice)
- [Example 35: ITIL 4 — Service Level Management Practice](/en/learn/it-governance/it-grc/by-example/intermediate#example-35-itil-4--service-level-management-practice)
- [Example 36: ITIL 4 vs ITIL V5 — What Changed in February 2026](/en/learn/it-governance/it-grc/by-example/intermediate#example-36-itil-4-vs-itil-v5--what-changed-in-february-2026)
- [Example 37: ISO/IEC 38500:2024 Applied to Cloud Adoption](/en/learn/it-governance/it-grc/by-example/intermediate#example-37-isoiec-385002024-applied-to-cloud-adoption)
- [Example 38: ISO 31000:2018 — Risk Treatment Plan](/en/learn/it-governance/it-grc/by-example/intermediate#example-38-iso-310002018--risk-treatment-plan)
- [Example 39: ISO 27001:2022 as a Governance Instrument](/en/learn/it-governance/it-grc/by-example/intermediate#example-39-iso-270012022-as-a-governance-instrument)
- [Example 40: NIST CSF 2.0 Govern Function](/en/learn/it-governance/it-grc/by-example/intermediate#example-40-nist-csf-20-govern-function)
- [Example 41: SOC 2 Governance Requirements](/en/learn/it-governance/it-grc/by-example/intermediate#example-41-soc-2-governance-requirements)
- [Example 42: GDPR Data Governance Obligations](/en/learn/it-governance/it-grc/by-example/intermediate#example-42-gdpr-data-governance-obligations)
- [Example 43: PCI DSS v4.0 Governance Requirements](/en/learn/it-governance/it-grc/by-example/intermediate#example-43-pci-dss-v40-governance-requirements)
- [Example 44: FAIR Risk Quantification](/en/learn/it-governance/it-grc/by-example/intermediate#example-44-fair-risk-quantification)
- [Example 45: Enterprise Risk Management Integration](/en/learn/it-governance/it-grc/by-example/intermediate#example-45-enterprise-risk-management-integration)
- [Example 46: Third-Party Governance Program](/en/learn/it-governance/it-grc/by-example/intermediate#example-46-third-party-governance-program)
- [Example 47: IT Audit Program Development](/en/learn/it-governance/it-grc/by-example/intermediate#example-47-it-audit-program-development)
- [Example 48: Control Deficiency Classification](/en/learn/it-governance/it-grc/by-example/intermediate#example-48-control-deficiency-classification)
- [Example 49: Remediation Tracking — Findings Management](/en/learn/it-governance/it-grc/by-example/intermediate#example-49-remediation-tracking--findings-management)
- [Example 50: Continuous Control Monitoring Program](/en/learn/it-governance/it-grc/by-example/intermediate#example-50-continuous-control-monitoring-program)
- [Example 51: Board IT Governance Reporting Dashboard](/en/learn/it-governance/it-grc/by-example/intermediate#example-51-board-it-governance-reporting-dashboard)
- [Example 52: IT Investment Portfolio Governance](/en/learn/it-governance/it-grc/by-example/intermediate#example-52-it-investment-portfolio-governance)
- [Example 53: Data Governance Program Basics](/en/learn/it-governance/it-grc/by-example/intermediate#example-53-data-governance-program-basics)
- [Example 54: Architecture Governance Review](/en/learn/it-governance/it-grc/by-example/intermediate#example-54-architecture-governance-review)
- [Example 55: Business Continuity Governance](/en/learn/it-governance/it-grc/by-example/intermediate#example-55-business-continuity-governance)
- [Example 56: Regulatory Compliance Calendar](/en/learn/it-governance/it-grc/by-example/intermediate#example-56-regulatory-compliance-calendar)
- [Example 57: GRC Tool Selection Criteria](/en/learn/it-governance/it-grc/by-example/intermediate#example-57-grc-tool-selection-criteria)

### Advanced (Examples 58–85)

- [Example 58: IT Governance Operating Model Design](/en/learn/it-governance/it-grc/by-example/advanced#example-58-it-governance-operating-model-design)
- [Example 59: COBIT 2019 Implementation Roadmap — 7-Phase Approach](/en/learn/it-governance/it-grc/by-example/advanced#example-59-cobit-2019-implementation-roadmap--7-phase-approach)
- [Example 60: COBIT Focus Area — AI Governance Using COBIT 2019](/en/learn/it-governance/it-grc/by-example/advanced#example-60-cobit-focus-area--ai-governance-using-cobit-2019)
- [Example 61: ISO/IEC 38500:2024 — AI and Sustainability Additions](/en/learn/it-governance/it-grc/by-example/advanced#example-61-isoiec-385002024--ai-and-sustainability-additions)
- [Example 62: ITIL V5 Transition Planning](/en/learn/it-governance/it-grc/by-example/advanced#example-62-itil-v5-transition-planning)
- [Example 63: Cloud Governance Framework](/en/learn/it-governance/it-grc/by-example/advanced#example-63-cloud-governance-framework)
- [Example 64: AI Governance Program — ISO 42001 and NIST AI RMF Mapping](/en/learn/it-governance/it-grc/by-example/advanced#example-64-ai-governance-program--iso-42001-and-nist-ai-rmf-mapping)
- [Example 65: EU AI Act Compliance for IT Governance](/en/learn/it-governance/it-grc/by-example/advanced#example-65-eu-ai-act-compliance-for-it-governance)
- [Example 66: DORA Compliance Program — ICT Risk Management Requirements](/en/learn/it-governance/it-grc/by-example/advanced#example-66-dora-compliance-program--ict-risk-management-requirements)
- [Example 67: DORA — Incident Reporting and Resilience Testing](/en/learn/it-governance/it-grc/by-example/advanced#example-67-dora--incident-reporting-and-resilience-testing)
- [Example 68: ESG Integration with IT GRC](/en/learn/it-governance/it-grc/by-example/advanced#example-68-esg-integration-with-it-grc)
- [Example 69: Data Governance Maturity Model](/en/learn/it-governance/it-grc/by-example/advanced#example-69-data-governance-maturity-model)
- [Example 70: ERM Integration — IT Risk Committee Structure](/en/learn/it-governance/it-grc/by-example/advanced#example-70-erm-integration--it-risk-committee-structure)
- [Example 71: IT Governance During M&A](/en/learn/it-governance/it-grc/by-example/advanced#example-71-it-governance-during-ma)
- [Example 72: Regulatory Examination Preparation — Financial Services](/en/learn/it-governance/it-grc/by-example/advanced#example-72-regulatory-examination-preparation--financial-services)
- [Example 73: Continuous Compliance Automation](/en/learn/it-governance/it-grc/by-example/advanced#example-73-continuous-compliance-automation)
- [Example 74: GRC Platform Implementation — ServiceNow GRC Process Mapping](/en/learn/it-governance/it-grc/by-example/advanced#example-74-grc-platform-implementation--servicenow-grc-process-mapping)
- [Example 75: IT Governance Benchmarking](/en/learn/it-governance/it-grc/by-example/advanced#example-75-it-governance-benchmarking)
- [Example 76: IT Governance Transformation Program](/en/learn/it-governance/it-grc/by-example/advanced#example-76-it-governance-transformation-program)
- [Example 77: Third-Party Risk Governance — Advanced TPRM](/en/learn/it-governance/it-grc/by-example/advanced#example-77-third-party-risk-governance--advanced-tprm)
- [Example 78: COSO ICIF 2013 Applied to IT Controls](/en/learn/it-governance/it-grc/by-example/advanced#example-78-coso-icif-2013-applied-to-it-controls)
- [Example 79: IT Governance ROI — Business Case](/en/learn/it-governance/it-grc/by-example/advanced#example-79-it-governance-roi--business-case)
- [Example 80: Board Technology Committee](/en/learn/it-governance/it-grc/by-example/advanced#example-80-board-technology-committee)
- [Example 81: IT Governance Culture and Awareness Program](/en/learn/it-governance/it-grc/by-example/advanced#example-81-it-governance-culture-and-awareness-program)
- [Example 82: IT Governance Annual Program Review](/en/learn/it-governance/it-grc/by-example/advanced#example-82-it-governance-annual-program-review)
- [Example 83: Regulatory Change Management](/en/learn/it-governance/it-grc/by-example/advanced#example-83-regulatory-change-management)
- [Example 84: IT Governance Succession Planning](/en/learn/it-governance/it-grc/by-example/advanced#example-84-it-governance-succession-planning)
- [Example 85: Building a World-Class IT Governance Program](/en/learn/it-governance/it-grc/by-example/advanced#example-85-building-a-world-class-it-governance-program)
