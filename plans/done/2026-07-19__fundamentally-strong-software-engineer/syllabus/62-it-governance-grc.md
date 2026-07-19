# 62 · IT Governance, Risk & Compliance (Annotated-concept, ‡ no-code)

**prd row**: Pass 3 · Build for the Real World · Annotated-concept · ‡ no-code · Learn 162 / Drill 262 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: `‡` leadership/no-code — governing technology responsibly: frameworks (COBIT/ISO 27001/NIST
CSF/SOC 2 intuition), risk management (identify/assess/treat), compliance & privacy (GDPR/data-protection
concepts), policy vs control, audit trails, and how security posture ([`58-it-and-application-security`](./58-it-and-application-security.md),
[`60-defensive-security`](./60-defensive-security.md)) rolls up into organizational assurance. Deliverables
are **decision/governance artifacts**, not code.

## Why this exists · the big idea

- **The problem before the solution**: controls, audits, and policies accumulate ad hoc until no one can
  say whether the organization is actually protected or merely busy — GRC exists to turn scattered security
  activity into defensible, org-level assurance.
- **Keep-this-if-you-forget-everything**: a control is worthless unless it traces back to a named risk and
  forward to auditable evidence — governance is that traceability, not the paperwork.
- **Big ideas touched**: `mechanism-vs-policy` — separates the machinery (controls, security operations)
  from the decisions (who owns which risk, what the org will accept); `correctness-vs-pragmatism` — risk
  treatment is disciplined compromise (mitigate / transfer / accept), never the fantasy of zero risk.

## Prerequisites

- **Prior topics**: [topic 58 IT / Application Security](./58-it-and-application-security.md) (CIA, threat modeling, controls),
  [topic 60 Defensive Security](./60-defensive-security.md) (detection, IR, the blue-team view that GRC
  rolls up), and [topic 9 Project Management](./09-project-management.md)
  (policy, process, working within an org).
- **Tools & environment**: no toolchain — a text editor for the governance artifacts (risk register, policy,
  control mapping); Neovim/VSCode (DD-17). No paid account, no code (DD-20).
- **Assumed knowledge**: security controls + threat modeling (topic 58); detection/IR posture (topic 60);
  how teams adopt process (topic 09).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified (framework versions): **COBIT 2019** is still current (6 principles, 40 objectives
  across EDM/APO/BAI/DSS/MEA — no 2024/25 revision; ISACA's Feb-2026 **ITAF 5th ed.** is a companion audit
  update, not a COBIT bump — re-check at authoring time). **ISO/IEC 27001:2022** is the sole current
  baseline (2013 certs expired 2025-10-30; minor **Amd 1:2024** adds climate-change clauses). **NIST CSF
  2.0** (2024-02-26) is current — added the **Govern** function → 6 functions total. **SOC 2** (AICPA Trust
  Services Criteria) is not version-numbered — un-versioned reference is correct.
- 2026-07-12 — verified: **GDPR** (Regulation (EU) 2016/679) in force, unchanged; risk methodology
  (identify → assess likelihood×impact → treat: accept/mitigate/transfer/avoid, ISO 31000 framing) and
  policy/control/procedure + preventive/detective/corrective control taxonomy are evergreen.

### DD-35 primary-source citations (fetched-and-read)

> Every framework name, control count, and principle below traces to a primary source the author fetched
> and READ. Unverifiable specifics carry `[Needs Verification]`.

- **Governance vs management (COBIT)** `[Verified]` — [ISACA COBIT](https://www.isaca.org/resources/cobit):
  COBIT 2019 covers "enterprise governance of information and technology (EGIT)"; **40 governance/management
  objectives** across **5 domains — EDM, APO, BAI, DSS, MEA**. Governance = the governing body's
  Evaluate–Direct–Monitor; management = plan/build/run/monitor. The verbatim EDM-vs-management split is from
  the ISACA support KB `[Needs Verification]` (page CAPTCHA-blocked direct fetch).
- **ISO/IEC 27001:2022 — Annex A 93 controls / 4 themes** `[Verified]` (ISMS description) /
  `[Needs Verification]` (control counts, ISO text is paywalled) — [iso.org/standard/27001](https://www.iso.org/standard/27001):
  "the world's best-known standard for information security management systems (ISMS)." Consensus structure
  (10+ secondary sources): 93 controls in Organizational (37) / People (8) / Physical (14) / Technological
  (34); down from 114 in the 2013 edition.
- **NIST CSF 2.0 — six Functions (verbatim)** `[Verified]` — [NIST CSWP 29 (PDF)](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf)
  (2024-02-26): GOVERN, IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER — GOVERN is new in 2.0 (was 5 functions
  in 1.1). Verbatim GOVERN: "The organization's cybersecurity risk management strategy, expectations, and
  policy are established, communicated, and monitored."
- **Risk management — RMF 7 steps (verbatim)** `[Verified]` — [NIST SP 800-37 Rev. 2 (PDF)](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-37r2.pdf)
  (Dec 2018): **Prepare → Categorize → Select → Implement → Assess → Authorize → Monitor** (Prepare added in
  Rev. 2). Risk assessment = likelihood × impact across org / mission / system tiers per
  [NIST SP 800-30 Rev. 1](https://csrc.nist.gov/pubs/sp/800/30/r1/final). ISO 31000:2018 (8 principles /
  framework / process) `[Needs Verification]` — ISO text paywalled.
- **GRC (OCEG, verbatim)** `[Verified]` — [oceg.org/ideas/what-is-grc](https://www.oceg.org/ideas/what-is-grc/):
  "The integrated collection of capabilities that enable an organization to reliably achieve objectives,
  address uncertainty, and act with integrity — to achieve Principled Performance."
- **IIA Three Lines Model** `[Verified]` — [IIA Three Lines Model (PDF)](https://na.theiia.org/about-ia/PublicDocuments/Three-Lines-Model-Updated.pdf)
  (2020-07-20, renamed from "Three Lines of Defense"): governing body (oversight) / first line (day-to-day
  risk ownership) / second line (expert support, monitoring) / third line (independent internal-audit
  assurance).
- **SOC 2 — 5 Trust Services Criteria (verbatim)** `[Verified]` — [AICPA 2017 TSC (2022 PoF)](https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022):
  **Security, Availability, Processing Integrity, Confidentiality, Privacy**. Security = "Information and
  systems are protected against unauthorized access…"
- **PCI DSS v4.0.1 — 12 requirements / 6 goals** `[Verified]` (goal statement) / `[Needs Verification]`
  (exact requirement wording, QRG PDF 403-blocked) — [pcisecuritystandards.org/standards/pci-dss](https://www.pcisecuritystandards.org/standards/pci-dss/):
  **v4.0.1 (2024-06-11) is current** (v4.0 retired 2024-12-31; zero requirement changes). 12 requirements
  under 6 goals (build secure network / protect account data / vuln management / access control / monitor &
  test / infosec policy).
- **GDPR — Art. 5 principles (verbatim)** `[Verified]` — [EUR-Lex Reg. (EU) 2016/679](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02016R0679-20160504):
  lawfulness/fairness/transparency, purpose limitation, data minimisation, accuracy, storage limitation,
  integrity & confidentiality, + accountability (Art. 5(2)); controller "determines the purposes and means"
  (Art. 4(7)), processor "processes… on behalf of the controller" (Art. 4(8)); breach notification "not
  later than 72 hours" (Art. 33(1)).
- **HIPAA** `[Verified]` — [HHS Privacy](https://www.hhs.gov/hipaa/for-professionals/privacy/laws-regulations/index.html)
  - [HHS Security](https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html): Privacy
    Rule protects PHI in any form; Security Rule protects ePHI via **Administrative / Physical / Technical**
    safeguards ("confidentiality, integrity, and availability of all ePHI").
- **Awareness / BCP / vendor risk** — [NIST SP 800-50 Rev. 1](https://csrc.nist.gov/pubs/sp/800/50/r1/final)
  `[Verified]` ("Building a Cybersecurity and Privacy Learning Program", Sept 2024, retitled; original
  withdrawn 2024-09-12). RTO/RPO ([NIST SP 800-34 Rev. 1](https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final))
  and vendor/C-SCRM risk ([NIST SP 800-161 Rev. 1](https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final))
  both `[Needs Verification]` (403-blocked; definitions search-corroborated).
- **`[Needs Verification]` pedagogical syntheses** — the "compliance vs security" contrast, the four-tier
  policy/standard/procedure/guideline hierarchy (NIST SP 800-12 uses a three-policy-type model), the COSO
  preventive/detective/corrective triad, and CMMI levels / PMBOK RACI rest on consistent secondary sources,
  not a single fetched standards-body verbatim. Teach as instructor synthesis; flag verbatim claims.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (‡ Leadership/no-code). Each scenario below cites the co-NN it exercises. -->

- **co-01 · it-governance-definition** — governance (evaluate/direct/monitor) is distinct from management (plan/build/run); COBIT draws the line.
- **co-02 · cobit-framework** — COBIT 2019 organizes 40 governance/management objectives across EDM/APO/BAI/DSS/MEA.
- **co-03 · iso-27001-isms** — ISO/IEC 27001:2022 defines an ISMS with 93 Annex A controls in four themes (org/people/physical/technological).
- **co-04 · nist-csf** — NIST CSF 2.0 organizes cybersecurity outcomes into six Functions: Govern, Identify, Protect, Detect, Respond, Recover.
- **co-05 · risk-management-lifecycle** — risk management runs identify → assess → treat (NIST RMF's seven steps / ISO 31000).
- **co-06 · risk-assessment** — assess risk as likelihood × impact; qualitative vs quantitative scoring (NIST SP 800-30).
- **co-07 · risk-register** — the risk register tracks each risk with an owner, a rating, and a treatment decision.
- **co-08 · risk-treatment** — treat a risk by accept / mitigate / transfer / avoid; residual risk is owned, not eliminated.
- **co-09 · grc-integrated** — GRC integrates governance, risk, and compliance into one capability (OCEG's Principled Performance).
- **co-10 · three-lines-model** — the IIA Three Lines: governing body, first line (owns risk), second line (oversees), third line (independent audit).
- **co-11 · soc-2** — SOC 2 reports against the AICPA Trust Services Criteria: Security, Availability, Processing Integrity, Confidentiality, Privacy.
- **co-12 · pci-dss** — PCI DSS (v4.0.1) structures cardholder-data protection into 12 requirements under 6 goals.
- **co-13 · gdpr-principles** — GDPR Art. 5 principles, controller vs processor, and the 72-hour breach-notification duty.
- **co-14 · hipaa** — HIPAA's Privacy Rule (PHI) and Security Rule (ePHI: administrative/physical/technical safeguards).
- **co-15 · compliance-vs-security** — compliance means meeting external requirements; security means actual risk reduction — they are not the same.
- **co-16 · policy-hierarchy** — policy → standard → procedure → guideline: the enforceable-intent-to-how hierarchy.
- **co-17 · control-types-function** — controls are preventive, detective, or corrective by when they act relative to the event.
- **co-18 · control-types-nature** — controls are administrative, technical, or physical by their nature.
- **co-19 · control-mapping** — mapping controls to a framework's categories and back to the risks they mitigate.
- **co-20 · audit** — internal vs external audit; evidence and findings that substantiate assurance.
- **co-21 · business-continuity-dr** — business continuity and disaster recovery, quantified by RTO and RPO.
- **co-22 · vendor-third-party-risk** — assessing and governing third-party / supply-chain (C-SCRM) risk.
- **co-23 · security-awareness** — security awareness and role-based training programs (NIST SP 800-50 Rev. 1).
- **co-24 · maturity-raci** — maturity models (CMMI's five levels) and RACI accountability (one accountable per activity).
- **co-25 · assurance-rollup** — how security operations and control evidence roll up into org-level assurance.
- **co-26 · software-licensing-ip** — permissive vs copyleft licensing (MIT/Apache vs GPL/AGPL), compatibility, SBOMs, and dependency IP risk.
- **co-27 · privacy-by-design** — data minimization, purpose limitation, and privacy defaults built in rather than bolted on.

## Worked examples

Colocated under `it-governance-grc/learning/artifacts/` (no `code/` — governance decision scenarios per the
`‡` shape, DD-27/DD-30). Contiguous `ex-01..ex-30`. Every scenario cites the `co-NN` it exercises. Concepts
come before scenarios.

### Beginner

- **ex-01 · governance-vs-management** — a scenario separating a governance decision from a management action — verify the evaluate/direct/monitor vs plan/build/run split. (co-01)
- **ex-02 · cobit-domain-map** — map an IT activity to a COBIT domain (EDM/APO/BAI/DSS/MEA) — verify the domain fit. (co-02)
- **ex-03 · risk-identify** — identify risks for a small system — verify each risk names an asset + threat. (co-05, co-07)
- **ex-04 · risk-assess-likelihood-impact** — rate a risk by likelihood × impact — verify the score placement. (co-06)
- **ex-05 · risk-treatment-choice** — choose accept/mitigate/transfer/avoid for a risk — verify the rationale. (co-08)
- **ex-06 · risk-register-entry** — a full risk-register entry (risk, owner, rating, treatment) — verify all fields present. (co-07)
- **ex-07 · policy-vs-procedure** — distinguish a policy from a standard/procedure/guideline — verify the hierarchy level. (co-16)
- **ex-08 · control-function-type** — classify a control preventive/detective/corrective — verify the timing relative to the event. (co-17)
- **ex-09 · control-nature-type** — classify a control administrative/technical/physical — verify the nature. (co-18)

### Intermediate

- **ex-10 · nist-csf-functions** — map controls to the CSF 2.0 six Functions — verify all six covered or justified. (co-04)
- **ex-11 · iso-27001-annex-a** — map a control to an ISO 27001:2022 Annex A theme — verify the theme (org/people/physical/tech). (co-03)
- **ex-12 · control-mapping-traceability** — map controls to a framework + back to risks — verify each control traces both ways. (co-19)
- **ex-13 · soc-2-criteria** — choose which SOC 2 Trust Services Criteria apply to a service — verify the category selection. (co-11)
- **ex-14 · pci-dss-scope** — scope which PCI DSS requirements apply to a cardholder-data flow — verify the requirement mapping. (co-12)
- **ex-15 · gdpr-principles** — check a data flow against GDPR Art. 5 principles — verify each principle addressed. (co-13)
- **ex-16 · gdpr-controller-processor** — classify parties as controller vs processor + the breach-notification duty — verify the 72h rule. (co-13)
- **ex-17 · hipaa-safeguards** — classify HIPAA safeguards (admin/physical/technical) for ePHI — verify the safeguard categories. (co-14)
- **ex-18 · compliance-vs-security** — a scenario where a system is compliant but not secure — verify the gap. (co-15)

### Advanced

- **ex-19 · three-lines-roles** — assign a responsibility across the IIA Three Lines — verify the line placement. (co-10)
- **ex-20 · risk-appetite** — set a risk appetite and accept a residual risk — verify the accountable owner. (co-08, co-01)
- **ex-21 · audit-evidence** — assemble audit evidence for a control — verify the evidence is concrete + auditable. (co-20)
- **ex-22 · internal-vs-external-audit** — distinguish an internal from an external audit engagement — verify the assurance role. (co-20)
- **ex-23 · bcp-rto-rpo** — set RTO/RPO for a business process — verify the recovery targets. (co-21)
- **ex-24 · vendor-risk-assessment** — assess a third-party vendor's risk — verify the tiered controls. (co-22)
- **ex-25 · security-awareness-program** — design a security-awareness training scenario — verify the role-based coverage. (co-23)
- **ex-26 · maturity-model** — place a process on a CMMI maturity level — verify the level rationale. (co-24)
- **ex-27 · raci-matrix** — build a RACI matrix for a security decision — verify one accountable per row. (co-24)
- **ex-28 · privacy-by-design** — apply privacy-by-design to a data flow (minimization/purpose-limitation/defaults) — verify the built-in privacy. (co-27)
- **ex-29 · licensing-ip-sbom** — assess OSS license risk (permissive vs copyleft) + an SBOM — verify the compatibility + dependency risk. (co-26)
- **ex-30 · grc-capstone** — a coherent GRC set: risk register + control mapping + policy/procedure/evidence + assurance roll-up — verify each part present + traceable. (co-07, co-09, co-19, co-25)

## Capstone spec — intra-topic (leadership → governance/decision artifact, no code)

- **Goal**: produce a **coherent GRC artifact set** for a small system — a risk register (risks identified,
  assessed by likelihood × impact, and treated), a control mapping to a named framework, and a short policy
  with supporting procedures + the audit evidence that would satisfy it — demonstrating that security
  posture rolls up into organizational assurance. **No code.**
- **Concepts exercised**: [ ] a risk register (identify → assess likelihood × impact → treat) (co-05, co-06,
  co-07, co-08) [ ] a control mapping to a named framework (ISO 27001 / NIST CSF / SOC 2) (co-03, co-04,
  co-11, co-19) [ ] policy vs control vs procedure (co-16, co-17, co-18) [ ] an audit-evidence / auditability
  trail (co-20) [ ] the security-ops → org-assurance roll-up (co-25).
- **Ordered steps**:
  1. `.../learning/capstone/artifacts/risk-register.md` — identify + assess (likelihood × impact) + treat
     a realistic set of risks for a small system. Verify each risk has an owner, a rating, and a treatment
     decision.
  2. `control-mapping.md` — map controls to a named framework's categories. Verify each mapped control
     traces to a real risk and a framework category.
  3. `policy.md` + `evidence.md` — a short policy with supporting procedures and the audit evidence that
     would demonstrate compliance. Verify the policy is enforceable, the procedures operationalize it, and
     the evidence is concrete and auditable.
- **Acceptance criteria**: risks are assessed and treated with owners; controls map to a real framework and
  back to risks; the policy/procedure/evidence chain is coherent and auditable; the artifact set holds
  together as org-level assurance. No code.
- **Done bar**: complete governance artifact set + internally coherent + web-verified.

## Read more

**Books**

- **IT Governance: How Top Performers Manage IT Decision Rights for Superior Results** — Peter Weill, Jeanne W. Ross (2004). The foundational business-school text defining IT governance as a discipline.

**Papers & articles**

- **NIST Cybersecurity Framework (CSF) 2.0** — National Institute of Standards and Technology (2024). Foundational risk-management framework central to most modern GRC programs. <https://www.nist.gov/cyberframework>
- **ISO/IEC 27001:2022 — Information Security Management Systems** — ISO/IEC (2022). The internationally recognized standard for information security management systems (ISMS), central to most GRC programs. <https://www.iso.org/standard/27001>
- **COBIT 2019 Framework** — ISACA (2018). The widely adopted framework specifically for IT governance and management objectives. <https://www.isaca.org/resources/cobit>

---

← Previous: [61 · Vulnerability Management & Assessment](./61-vulnerability-management-and-assessment.md) · Next: [63 · Analytics & Experimentation](./63-analytics-and-experimentation.md) →
