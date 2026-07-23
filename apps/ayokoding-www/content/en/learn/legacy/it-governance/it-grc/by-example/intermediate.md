---
title: "Intermediate"
weight: 10000002
date: 2026-05-21T00:00:00+07:00
draft: false
description: "IT-GRC intermediate examples — framework application, compliance programs, FAIR quantification, vendor governance, audit development, board reporting (Examples 29–57)"
tags: ["it-grc", "it-governance", "cobit", "itil", "compliance", "fair", "intermediate", "by-example"]
---

## Example 29: COBIT 2019 Gap Analysis — EDM01

**What this covers:** A COBIT 2019 gap analysis for EDM01 (Governance Framework Setting and
Maintenance) measures current capability maturity against a target, identifies gaps per capability
practice, and prescribes remediation actions. It converts the abstract governance objective into a
prioritized improvement roadmap.

**Scenario:** Northgate Credit Union (NCU), a 400-person financial cooperative, is preparing for a
regulatory examination. The Chief Risk Officer commissions a COBIT 2019 EDM01 gap analysis to
demonstrate governance maturity to examiners and identify the highest-priority remediation items.

```yaml
# COBIT 2019 Gap Analysis — EDM01: Governance Framework Setting and Maintenance
# Organization: Northgate Credit Union (NCU) | Date: May 2026
# Assessor: Internal Governance Team + External Advisor
# Maturity Scale: 0 (Incomplete) → 1 (Initial) → 2 (Managed) → 3 (Defined) → 4 (Quantitatively Managed) → 5 (Optimizing)

gap_analysis:
  objective: EDM01
  # => EDM01 is the COBIT 2019 governance objective responsible for establishing and maintaining
  # => the IT governance framework — the foundation all other COBIT objectives rely on

  target_maturity_overall: 3
  # => Level 3 (Defined) is the regulatory baseline for supervised financial institutions;
  # => NCU does not need Level 4-5 for examination purposes but must demonstrate consistency

  practices:
    - id: EDM01.01
      name: "Evaluate the governance system"
      current_maturity: 1
      target_maturity: 3
      gap: 2
      priority: HIGH
      # => Gap of 2 is the largest in this analysis — NCU has no formal governance
      # => evaluation cycle; reviews happen ad hoc when regulators ask, not on a defined schedule
      finding: "Governance framework reviewed only when triggered by examination; no annual cycle."
      remediation: "Establish annual governance framework review; document findings in board minutes."
      owner: CRO
      due: "2026-Q3"

    - id: EDM01.02
      name: "Direct the governance system"
      current_maturity: 2
      target_maturity: 3
      gap: 1
      priority: MEDIUM
      # => Gap of 1 indicates the practice exists but is not fully consistent — board resolutions
      # => reference IT governance but the linkage to strategic objectives is implicit, not explicit
      finding: "Board sets IT direction in budget cycle; linkage to strategic objectives not formally documented."
      remediation: "Create IT strategy alignment map approved by board annually."
      owner: CEO
      due: "2026-Q4"

    - id: EDM01.03
      name: "Monitor the governance system"
      current_maturity: 1
      target_maturity: 3
      gap: 2
      priority: HIGH
      # => Monitoring gap is critical: without it, even a well-designed governance framework
      # => will drift — NCU has no defined metrics or reporting cadence for governance effectiveness
      finding: "No governance effectiveness KPIs defined; board receives ad hoc IT updates only."
      remediation: "Define 5 governance KPIs; establish quarterly board IT governance dashboard."
      owner: CRO
      due: "2026-Q3"

  summary:
    average_gap: 1.67
    # => Average gap of 1.67 across three practices signals systemic underdevelopment,
    # => not isolated failures — root cause is absence of a deliberate governance program
    highest_priority_action: "Implement annual governance evaluation cycle (EDM01.01 + EDM01.03)"
    regulatory_risk: "MEDIUM-HIGH — examiners will look for board-level governance evidence"
    budget_estimate_usd: 45000
    # => $45K covers external advisor facilitation, policy development, and training;
    # => this is a documentation and process program, not a technology investment
```

**Key Takeaway:** The largest EDM01 gaps at NCU are in evaluation and monitoring — not in
direction-setting — which means the board sets strategy but never verifies whether governance
is actually working, creating a systematic blind spot that examiners routinely flag.

**Why It Matters:** COBIT EDM01 is the governance meta-objective: it governs the governance
system itself. Organizations that skip EDM01 remediation while improving operational COBIT
objectives (APO, BAI, DSS) are building on an unstable foundation. Regulators in the financial
sector increasingly expect boards to demonstrate not just that governance policies exist, but
that leadership monitors whether those policies produce the intended outcomes. Closing the
EDM01.01 and EDM01.03 gaps directly reduces examination findings risk.

---

## Example 30: COBIT 2019 APO12 — Risk Management Objective

**What this covers:** COBIT 2019 APO12 (Manage Risk) defines six practices covering risk
identification, analysis, response, and monitoring. This example annotates the full APO12
objective structure — practices, key activities, RACI, and metrics — for an operational
financial services context.

**Scenario:** Meridian Capital Partners (MCP), a 300-person asset management firm, is
implementing COBIT 2019 as its IT governance framework. The CIO is responsible for APO12
implementation and needs to present the objective structure to the risk committee.

```yaml
# COBIT 2019 APO12 — Manage Risk
# Organization: Meridian Capital Partners (MCP) | Scope: IT Risk Management
# Owner: CIO | Status: Implementation in progress

objective:
  id: APO12
  domain: Align, Plan and Organize (APO)
  # => APO domain covers strategy, architecture, and enterprise arrangements —
  # => APO12 sits here because risk management is a planning discipline, not an operational one

  practices:
    - id: APO12.01
      name: "Collect data"
      description: "Identify and collect relevant risk data from internal and external sources."
      key_activities:
        - "Maintain threat intelligence feeds (ISAC for asset management sector)"
        - "Collect vulnerability scan results from IT operations"
        - "Log near-miss incidents and operational risk events"
      # => Data collection is the foundation — garbage in, garbage out applies to risk registers;
      # => MCP uses FS-ISAC for sector-specific threat intelligence as a primary external feed
      raci:
        responsible: IT Risk Analyst
        accountable: CIO
        consulted: [CISO, Business Unit Heads]
        informed: [Board Risk Committee]

    - id: APO12.02
      name: "Analyse risk"
      description: "Analyze risk scenarios to determine likelihood and impact."
      key_activities:
        - "Apply FAIR model for top-5 risks requiring quantification"
        - "Maintain qualitative risk register for operational risks"
        - "Conduct quarterly risk scenario analysis workshops"
      # => FAIR quantification is reserved for top risks — applying it to all risks
      # => would consume more analyst time than the precision gain justifies
      raci:
        responsible: IT Risk Analyst
        accountable: CIO
        consulted: [CFO, CISO]
        informed: [Board Risk Committee]

    - id: APO12.03
      name: "Maintain a risk profile"
      description: "Maintain an accurate current risk profile across IT domains."
      key_activities:
        - "Update risk register monthly; review risk ratings quarterly"
        - "Map risks to strategic objectives and business processes"
        - "Flag risks exceeding risk appetite threshold to CIO within 48 hours"
      # => 48-hour escalation threshold ensures high-velocity risks (e.g., zero-day exploits)
      # => reach decision-makers before they become incidents — this is a governance SLA
      raci:
        responsible: IT Risk Analyst
        accountable: CIO
        consulted: [Business Continuity Manager]
        informed: [CEO, Board Risk Committee]

    - id: APO12.04
      name: "Articulate risk"
      description: "Communicate risk information to stakeholders in business terms."
      key_activities:
        - "Produce quarterly board risk report with heat map and trend analysis"
        - "Translate technical risks into financial impact language (FAIR outputs)"
        - "Brief risk committee on material changes between quarterly meetings"
      # => Articulation practice is where most IT risk programs fail — technical teams
      # => produce register updates that boards cannot use for decision-making
      raci:
        responsible: CIO
        accountable: CEO
        consulted: [IT Risk Analyst, CFO]
        informed: [Board of Directors]

    - id: APO12.05
      name: "Define a risk management action portfolio"
      description: "Prioritize and select risk responses; align with risk appetite."
      key_activities:
        - "Apply treat/tolerate/transfer/terminate framework to each risk"
        - "Align risk treatment investment with risk appetite statement"
        - "Track treatment implementation through project governance"
      # => The four-T framework forces explicit decisions — "we accept this risk" is a valid
      # => board decision when documented, but undocumented acceptance creates audit findings
      raci:
        responsible: CIO
        accountable: CEO
        consulted: [CFO, CISO, Business Unit Heads]
        informed: [Board Risk Committee]

    - id: APO12.06
      name: "Respond to risk"
      description: "Act on risk events and incidents; update risk profile post-event."
      key_activities:
        - "Activate incident response for materialized risks"
        - "Conduct post-incident risk profile update within 5 business days"
        - "Report material risk events to board within 24 hours of discovery"
      # => Post-incident risk profile update closes the loop — many organizations respond to
      # => incidents but fail to update the risk register, leaving the profile stale
      raci:
        responsible: CISO
        accountable: CIO
        consulted: [Legal, Compliance, CFO]
        informed: [Board, Regulators (if material)]

  metrics:
    - name: "Risk register coverage"
      definition: "Percentage of IT processes with at least one documented risk"
      target: ">=95%"
      current: "78%"
      # => 78% coverage means 22% of processes are unexamined — regulators will ask about gaps

    - name: "Risk treatment completion rate"
      definition: "Percentage of planned treatments completed on schedule"
      target: ">=85%"
      current: "71%"
      # => 71% on-time treatment rate signals resource or prioritization constraints;
      # => CIO must investigate whether overdue treatments are low-priority or systemically blocked

    - name: "Risk appetite breach count"
      definition: "Number of risks currently exceeding defined risk appetite thresholds"
      target: "0 unmitigated for >30 days"
      current: "3 breaches, oldest 47 days"
      # => Three appetite breaches over 30 days are a governance escalation trigger —
      # => the board risk committee must be briefed regardless of whether treatment is in progress
```

**Key Takeaway:** APO12 is only as strong as its articulation practice — practices APO12.01
through APO12.03 build analytical rigor, but APO12.04 determines whether that rigor translates
into board decisions and investment allocations.

**Why It Matters:** COBIT APO12 structures IT risk management as a closed loop: collect,
analyze, maintain, articulate, plan responses, respond. Organizations that implement only the
analytical practices while neglecting articulation and response tracking accumulate risk
intelligence that never drives action. At Meridian Capital Partners, the three appetite breaches
exceeding 30 days signal that the loop is broken between risk identification and treatment
execution — precisely the gap that regulatory examinations surface as findings.

---

## Example 31: COBIT 2019 BAI06 — Change Management Objective

**What this covers:** COBIT 2019 BAI06 (Manage IT Changes) defines the control activities,
RFC lifecycle, CAB approval criteria, and emergency change procedures that govern how IT
changes are authorized, tested, and implemented. Effective change management prevents
unauthorized changes from introducing instability or security vulnerabilities.

**Scenario:** Crestview Insurance Group (CIG), a 500-person regional insurer, has experienced
three production outages in six months caused by uncontrolled changes. The CIO implements
BAI06 to formalize the change governance process before the upcoming SOX compliance review.

```yaml
# COBIT 2019 BAI06 — Manage IT Changes
# Organization: Crestview Insurance Group (CIG)
# Owner: CIO | Trigger: Three production outages from uncontrolled changes

change_management_framework:
  change_types:
    standard:
      definition: "Pre-approved, low-risk, repeatable change with documented procedure"
      examples: ["OS patch (tested monthly)", "Firewall rule update (routine)"]
      approval_required: false
      # => Standard changes bypass CAB because risk is pre-assessed at procedure approval time;
      # => the procedure itself is the control — each execution follows the documented steps
      cab_review: false
      implementation_window: "Normal business hours or maintenance window"

    normal:
      definition: "Change requiring individual risk assessment and CAB approval"
      examples: ["New application deployment", "Database schema change", "Network reconfiguration"]
      approval_required: true
      # => Normal changes require full RFC documentation so CAB can assess risk before authorization;
      # => the RFC must be submitted at least 5 business days before the planned implementation date
      cab_review: true
      cab_quorum: "CIO + at least 2 of: Security, Operations, Business Representative"
      # => CAB quorum requires the CIO because CIG's governance model makes the CIO accountable
      # => for change risk; business representation ensures operational impact is considered
      lead_time_days: 5
      implementation_window: "Scheduled maintenance window (Saturdays 01:00-05:00 local)"

    emergency:
      definition: "Unplanned change required immediately to restore service or address critical security vulnerability"
      examples: ["Zero-day patch deployment", "Emergency rollback after production failure"]
      approval_required: true
      # => Emergency changes still require approval — the difference is compressed timeline
      # => and post-hoc CAB ratification, not approval bypass
      approval_authority: "CIO + on-call Security Lead (verbal or electronic)"
      post_hoc_cab_review: true
      post_hoc_deadline_hours: 48
      # => 48-hour post-hoc ratification window ensures emergency changes are not forgotten;
      # => CAB reviews the change record, validates the risk was genuine, and approves closure
      documentation_required: ["RFC with emergency justification", "Impact assessment", "Rollback plan"]

  rfc_lifecycle:
    stages:
      - stage: "Submit"
        actor: Change Requestor
        action: "Complete RFC template; specify change type, risk, rollback plan, test evidence"
        # => RFC template completeness gates CAB review — incomplete RFCs are returned,
        # => not deferred; this prevents last-minute submissions without adequate documentation

      - stage: "Technical Review"
        actor: Change Advisory Board (technical members)
        action: "Assess technical risk, dependency conflicts, resource requirements"
        sla_hours: 48

      - stage: "CAB Approval"
        actor: CAB (full membership)
        action: "Approve, reject, or defer; document rationale in change record"
        # => CAB decisions must be documented — "approved" without rationale is an audit finding
        sla_hours: 24

      - stage: "Schedule"
        actor: Change Manager
        action: "Assign implementation window; notify affected stakeholders 48 hours in advance"

      - stage: "Implement"
        actor: Change Implementor
        action: "Execute change following approved procedure; record actual start/end times"

      - stage: "Post-Implementation Review"
        actor: Change Implementor + Operations
        action: "Verify successful implementation; document any deviations from plan"
        # => PIR within 5 business days for normal changes; within 48 hours for emergency changes;
        # => deviations from the approved RFC require a new RFC if scope has materially changed

      - stage: "Close"
        actor: Change Manager
        action: "Close change record; update CMDB; trigger lessons-learned if adverse outcome"

  cab_approval_criteria:
    mandatory_checks:
      - "Rollback plan documented and validated by a second technician"
      - "Test evidence from non-production environment attached"
      - "Business impact window confirmed with affected business unit"
      - "No conflicts with other scheduled changes in the same maintenance window"
      # => Conflict checking is a common CAB failure point — two teams both patching the
      # => same server in the same window creates race conditions that cause outages
      - "Security review completed if change touches authentication, encryption, or network perimeter"

    rejection_criteria:
      - "Rollback plan absent or untested"
      - "Insufficient test evidence for production-impacting changes"
      - "Submission received less than 24 hours before planned implementation (non-emergency)"
      # => Sub-24-hour submissions are rejected automatically by Change Manager before CAB —
      # => this removes time pressure from CAB and prevents rushed approvals

  metrics:
    change_success_rate:
      definition: "Changes implemented without unplanned incidents or rollbacks"
      target: ">=97%"
      # => 97% is the industry benchmark for mature change management programs;
      # => CIG's current rate is 84% — the gap is the primary driver for BAI06 implementation
      current: "84%"
    emergency_change_ratio:
      definition: "Emergency changes as percentage of all changes"
      target: "<=5%"
      current: "18%"
      # => 18% emergency change ratio indicates poor planning discipline or change avoidance
      # => (teams bypass normal process by declaring emergency); target is <=5%
    unauthorized_change_count:
      definition: "Changes detected in production without an approved RFC"
      target: "0"
      current: "7 in last 90 days"
      # => Seven unauthorized changes in 90 days is a SOX compliance finding —
      # => CIG must implement automated CMDB drift detection to catch unauthorized changes
```

**Key Takeaway:** CIG's 18% emergency change ratio and seven unauthorized changes reveal
that the cultural barrier to using the normal change process is higher than the cost of
bypassing it — BAI06 implementation must address incentives and training alongside procedure.

**Why It Matters:** Change management failures are the leading cause of production incidents
in mid-sized organizations. COBIT BAI06 does not exist to slow down IT — it exists to ensure
changes are tested, reversible, and approved before they affect production systems. At Crestview,
the three outages from uncontrolled changes each cost more in business disruption than the
entire BAI06 implementation program. The unauthorized change metric is the most critical: zero
is the only acceptable target for SOX-regulated organizations.

---

## Example 32: COBIT 2019 MEA01 — Monitoring Performance

**What this covers:** COBIT 2019 MEA01 (Manage Performance and Conformance Monitoring) defines
how organizations collect, validate, and report governance metrics. An MEA01 scorecard maps
governance objectives to measurable KPIs, assigns RAG (Red/Amber/Green) status, and tracks
trends to support board-level oversight decisions.

**Scenario:** Northgate Credit Union (NCU) from Example 29 has completed its EDM01 remediation
and now needs to demonstrate ongoing governance monitoring to the regulatory examiner. The CRO
produces an MEA01 scorecard for the quarterly board meeting.

```markdown
# COBIT 2019 MEA01 Governance Scorecard — Northgate Credit Union

# Period: Q1 2026 | Owner: CRO | Audience: Board of Directors + Regulator

| COBIT Objective | Metric                                  | Target  | Actual   | RAG   | Trend | Commentary                                               |
| --------------- | --------------------------------------- | ------- | -------- | ----- | ----- | -------------------------------------------------------- |
| EDM01           | Governance review cycle completed       | Annual  | On track | GREEN | →     | Annual review scheduled for Q3; charter drafted          |
| EDM02           | IT investment benefits realization      | >=80%   | 74%      | AMBER | ↑     | Two projects delayed; portfolio realignment in progress  |
| APO12           | Risk appetite breaches >30 days         | 0       | 1        | AMBER | ↑     | One breach identified; treatment plan approved           |
| APO12           | Risk register coverage                  | >=95%   | 91%      | AMBER | ↑     | Four processes added to register this quarter            |
| BAI06           | Change success rate                     | >=97%   | 99%      | GREEN | ↑     | CAB process fully adopted after Q4 2025 overhaul         |
| BAI06           | Unauthorized changes                    | 0       | 0        | GREEN | →     | CMDB drift detection deployed; zero violations           |
| DSS05           | Critical vulnerability remediation <30d | >=95%   | 88%      | AMBER | ↓     | Patch backlog growing; resourcing review requested       |
| DSS05           | Security incident count (P1/P2)         | <=2/qtr | 1        | GREEN | →     | One P2 (phishing attempt, contained)                     |
| MEA02           | Internal audit findings closed on time  | >=90%   | 83%      | AMBER | ↓     | Seven overdue findings; root cause: resource constraints |
| MEA03           | Regulatory obligation compliance rate   | 100%    | 100%     | GREEN | →     | All Q1 regulatory submissions filed on time              |

# --- Scorecard interpretation notes ---

# GREEN = On target; no action required beyond routine monitoring

# AMBER = Off target but within acceptable variance; management action plan required

# RED = Significantly off target; board escalation and immediate remediation required

# Trend arrows: ↑ = improving, → = stable, ↓ = deteriorating

# DSS05 patch backlog (AMBER, ↓) is the highest-priority item this quarter:

# deteriorating trend in a security-critical metric requires board awareness

# MEA02 finding closure rate (AMBER, ↓) is an early warning signal:

# if audit findings accumulate without closure, regulatory risk increases

# --- Board asks ---

# 1. Approve additional resourcing for DSS05 patch remediation ($85K contractor budget)

# 2. Note APO12 appetite breach — treatment plan in place, expected closed Q2

# 3. No RED items this quarter — overall governance posture improving from Q4 2025 baseline
```

**Key Takeaway:** The MEA01 scorecard converts COBIT objectives into board-consumable
governance intelligence — the two AMBER/deteriorating metrics (DSS05 patch backlog and MEA02
finding closure) demand board attention precisely because trends matter as much as point-in-time
status.

**Why It Matters:** Monitoring without action is theater. COBIT MEA01 is only valuable if the
scorecard drives decisions: resource allocations, escalations, and corrective actions. NCU's
board can see from the RAG dashboard that governance is generally improving while two specific
areas require intervention. This transparency satisfies regulatory expectations and gives the
board the information needed to fulfill its oversight duty rather than relying on management
assurances alone.

---

## Example 33: ITIL 4 — Change Enablement Practice

**What this covers:** ITIL 4 Change Enablement defines three change types (normal, standard,
emergency), the change model each type follows, CAB quorum requirements, and the success
criteria used to evaluate whether a change achieved its intended outcome without adverse
side effects.

**Scenario:** Harborview Logistics (HVL), an 800-person distribution company, is adopting
ITIL 4 after migrating from a legacy ITSM tool. The IT Service Manager designs the change
enablement practice to integrate with the new ServiceNow deployment.

```yaml
# ITIL 4 Change Enablement Practice Design — Harborview Logistics (HVL)
# Owner: IT Service Manager | ITSM Tool: ServiceNow

change_types:
  standard:
    definition: "Low-risk, pre-authorized, well-understood change following a documented procedure"
    # => Standard changes are pre-authorized at procedure approval time, not at execution time;
    # => this eliminates CAB overhead for routine, repeatable work like monthly patching
    authorization: "Pre-authorized (no CAB review per execution)"
    change_model: "Standard Change Procedure (documented in ServiceNow catalog)"
    examples:
      - "Monthly OS patching (Windows/Linux — tested in staging)"
      - "SSL certificate renewal (automated via Let's Encrypt)"
      - "User access provisioning (via approved role templates)"
    success_criteria:
      - "Change executed within defined maintenance window"
      - "Post-implementation smoke test passed"
      - "No P1/P2 incidents raised within 24 hours attributable to change"
    cab_review: false
    record_required: true
    # => Records are required even for standard changes — the record proves authorization
    # => and provides evidence for audit; absence of records is an audit finding

  normal:
    definition: "Change requiring individual assessment, authorization, and scheduling"
    authorization: "CAB approval required"
    # => CAB authorization for normal changes ensures risk is assessed by multiple stakeholders
    # => before implementation; it is not a bureaucratic gate but a risk management control
    change_model:
      stages: ["Request", "Assess", "Authorize", "Schedule", "Implement", "Review", "Close"]
      # => Seven-stage lifecycle ensures no step is skipped; ServiceNow workflow enforces sequence
    lead_time_minimum_days: 5
    cab_quorum:
      required_members:
        - "IT Service Manager (chair)"
        - "At least one: Operations Lead, Security Lead, Application Owner"
        # => Quorum requires the IT Service Manager as chair — decisions without the chair
        # => are invalid; this prevents informal email approvals bypassing the formal record
      optional_members:
        - "Business Relationship Manager (for user-impacting changes)"
        - "Vendor representative (for vendor-managed component changes)"
    success_criteria:
      - "Change implemented within approved window (tolerance: +/- 15 minutes)"
      - "All acceptance tests defined in RFC passed"
      - "No unplanned rollback required"
      - "CMDB updated within 24 hours of successful implementation"
      # => CMDB update is a success criterion, not an afterthought — stale CMDB data cascades
      # => into incident and problem management failures downstream
    cab_meeting_cadence: "Weekly (Tuesdays 14:00); emergency sessions as needed"

  emergency:
    definition: "Urgent change needed to restore service or address critical security risk"
    authorization: "Emergency CAB (ECAB) — IT Service Manager + on-call Operations Lead"
    # => ECAB is a two-person authorization mechanism designed for speed;
    # => full CAB review happens post-implementation to validate the emergency was genuine
    change_model:
      stages: ["Identify", "Rapid Authorize (ECAB)", "Implement", "Post-Hoc CAB Review", "Close"]
    authorization_sla_minutes: 30
    # => 30-minute ECAB authorization SLA — longer than this and the emergency process
    # => is not meeting its purpose; if authorization takes hours, ECAB is under-resourced
    post_hoc_cab_review_sla_hours: 48
    success_criteria:
      - "Service restored or security risk mitigated within agreed RTO"
      - "Post-hoc CAB review completed within 48 hours"
      - "Root cause of emergency identified (to prevent recurrence)"
      - "Emergency RFC fully documented within 4 hours of implementation"
    misuse_detection:
      threshold: "Emergency changes >5% of monthly change volume triggers review"
      # => High emergency change rates indicate teams are bypassing normal process;
      # => the IT Service Manager reviews each emergency declaration for validity at monthly CAB

metrics:
  change_success_rate:
    target: ">=97%"
    measurement: "Changes with no P1/P2 incident within 48 hours as percentage of all changes"
  emergency_change_ratio:
    target: "<=5% of monthly volume"
  cab_lead_time_compliance:
    target: ">=90% of normal changes submitted with >=5 days lead time"
    # => Lead time compliance measures planning discipline — teams that consistently
    # => miss lead time requirements are candidates for change enablement coaching
```

**Key Takeaway:** ITIL 4 Change Enablement's three-type model is designed to match
authorization overhead to risk level — standard changes get pre-authorization, normal changes
get planned CAB review, and emergency changes get expedited authorization with post-hoc
validation to prevent process bypass.

**Why It Matters:** Change management is the single highest-leverage practice for reducing
IT service disruptions. Harborview Logistics' challenge — like most organizations migrating
to ITIL 4 — is cultural adoption: teams bypass formal change processes when they perceive the
process as slower than the risk it prevents. The 5% emergency change threshold is a behavioral
governance control: it makes bypass visible and triggers management intervention before it
becomes habitual.

---

## Example 34: ITIL 4 — Incident Management Practice

**What this covers:** ITIL 4 Incident Management classifies incidents by priority (P1–P4)
using impact and urgency criteria, defines response SLAs, escalation paths, and stakeholder
communication requirements for each priority level. The classification matrix is the operational
backbone of service restoration.

**Scenario:** Harborview Logistics (HVL) from Example 33 needs to define its incident
classification matrix for the new ServiceNow deployment. The IT Service Manager designs a
P1–P4 matrix aligned with business criticality and contractual SLAs.

```markdown
# ITIL 4 Incident Classification Matrix — Harborview Logistics (HVL)

# Owner: IT Service Manager | Effective: June 2026

| Priority | Criteria                                                                                   | Response SLA | Resolution SLA   | Escalation Path                                         | Stakeholder Communication                            |
| -------- | ------------------------------------------------------------------------------------------ | ------------ | ---------------- | ------------------------------------------------------- | ---------------------------------------------------- |
| P1       | Complete outage of business-critical service OR data breach in progress                    | 15 minutes   | 4 hours          | On-call Operations Lead → CIO → CEO (at 1 hour)         | SMS + email to affected VPs every 30 minutes         |
| P2       | Significant degradation of business-critical service OR partial outage affecting >50 users | 30 minutes   | 8 hours          | On-call Operations Lead → IT Service Manager (at 1 hr)  | Email to affected managers at open and every 2 hours |
| P3       | Non-critical service impacted OR <50 users affected; workaround available                  | 2 hours      | 3 business days  | IT Service Desk → Operations Lead (if unresolved >4 hr) | Email to requester at open and on resolution         |
| P4       | Minor issue; cosmetic or informational; no service impact                                  | 8 hours      | 10 business days | IT Service Desk                                         | Email to requester at open and on resolution         |

# --- Priority assignment notes ---

# Impact axis: How many users affected? Which business processes disrupted?

# Urgency axis: How quickly will impact worsen without intervention?

# Priority = f(Impact, Urgency) — use the matrix below for borderline cases:

# Impact \ Urgency | High Urgency | Low Urgency

# High Impact | P1 | P2

# Low Impact | P3 | P4

# P1 examples at HVL:

# - Warehouse Management System (WMS) unavailable — dispatch operations halted

# - ERP finance module down during month-end close

# - Security Operations alerting on active intrusion

# P2 examples:

# - WMS slow (>10 second response times) affecting pick rates

# - Email gateway degraded — outbound email queued >30 minutes

# - VPN connectivity failures affecting >50 remote workers

# --- Escalation rules ---

# Automatic P1 escalation to CIO at T+60 minutes if not resolved

# Automatic P1 escalation to CEO at T+60 minutes if business operations halted

# P2 unresolved at T+4 hours: escalate to IT Service Manager with updated ETA

# --- Major Incident process (P1 only) ---

# Declare Major Incident → Activate Major Incident Commander (Senior Operations Lead)

# Dedicated bridge call open for duration of incident

# Post-Incident Review (PIR) mandatory within 5 business days of P1 resolution

# PIR output: timeline, root cause, preventive actions, owner, due dates

# PIR report shared with CIO and affected business unit heads

# --- SLA exceptions ---

# Public holidays: P3 and P4 SLAs suspended; P1 and P2 SLAs unchanged

# Planned maintenance windows: incidents during maintenance assessed for maintenance-causation
```

**Key Takeaway:** The P1–P4 classification matrix is only useful if the escalation paths and
communication requirements are followed consistently — the Harborview matrix makes stakeholder
communication mandatory at defined intervals, removing the discretion that leads to business
stakeholders discovering major incidents from end users rather than IT.

**Why It Matters:** Incident classification without communication standards creates a gap
between IT resolution activity and business awareness. When business stakeholders learn about
P1 incidents through operations floor disruption rather than IT notification, trust erodes and
pressure for informal workarounds increases. The mandatory 30-minute update cadence for P1
incidents is a governance requirement, not a suggestion — it keeps the business informed and
creates a documented communication audit trail for post-incident review.

---

## Example 35: ITIL 4 — Service Level Management Practice

**What this covers:** ITIL 4 Service Level Management (SLM) covers the full lifecycle of
service level agreements: SLA negotiation with customers, Operational Level Agreement (OLA)
alignment with internal teams, underpinning contracts with vendors, and the remediation workflow
triggered when SLA breaches occur.

**Scenario:** Harborview Logistics (HVL) is establishing formal SLAs for its three
business-critical services after a year of informal support commitments. The IT Service Manager
leads the SLM design in consultation with business unit heads.

```yaml
# ITIL 4 Service Level Management — Harborview Logistics (HVL)
# Owner: IT Service Manager | Effective: Q3 2026

services:
  - service_name: "Warehouse Management System (WMS)"
    business_owner: "Head of Operations"
    criticality: CRITICAL
    # => Criticality CRITICAL means WMS outage directly stops revenue-generating operations;
    # => SLAs for critical services must be tighter and have more aggressive remediation

    sla:
      availability_target: "99.5% monthly"
      # => 99.5% monthly allows approximately 3.6 hours of downtime per month;
      # => 24/7 warehouse operations make this the minimum acceptable target
      performance_target: "Page response time <3 seconds for 95th percentile requests"
      incident_response_sla:
        P1: "15 minutes response / 4 hours resolution"
        P2: "30 minutes response / 8 hours resolution"
      service_window: "24x7x365"
      review_cycle: "Quarterly"
      breach_credit: "Service credit of 5% of monthly fee per hour of unplanned downtime beyond target"
      # => Service credits create financial accountability for the IT department;
      # => internal IT departments use notional credits to make SLA breaches visible to budget owners

    olas:
      - team: "Infrastructure Operations"
        commitment: "Respond to WMS infrastructure alerts within 10 minutes; 24x7 on-call"
        # => OLA response time must be shorter than SLA response time — 10 min OLA supports 15 min SLA
      - team: "Application Support"
        commitment: "Application-layer triage within 20 minutes; code fix deployment within 2 hours"
      - team: "Database Administration"
        commitment: "Database alert response within 15 minutes; performance tuning SLA: 48 hours"

    underpinning_contracts:
      - vendor: "WMS Software Vendor (CloudLogix)"
        contract_type: "Vendor SLA"
        uptime_commitment: "99.9% monthly for SaaS platform"
        support_tier: "Enterprise (24x7 P1 support)"
        annual_review_date: "2027-01-15"
        # => Vendor UC at 99.9% is stronger than HVL's internal SLA of 99.5% — the gap
        # => provides buffer for HVL infrastructure and integration failures outside vendor control

  - service_name: "ERP Financial Module"
    business_owner: "CFO"
    criticality: HIGH
    sla:
      availability_target: "99.0% during business hours (07:00-20:00 Mon-Fri)"
      # => Business-hours availability target reflects that ERP is not a 24x7 operational need;
      # => scoping the window reduces SLA breach risk without reducing business value
      performance_target: "Report generation <30 seconds for standard reports"
      service_window: "Business hours only; extended hours during month-end (last 3 business days)"
      review_cycle: "Semi-annual"
    olas:
      - team: "ERP Application Team"
        commitment: "Business hours support; P1 on-call during month-end window"

sla_breach_remediation_workflow:
  trigger: "SLA metric breaches target threshold"
  steps:
    - step: 1
      action: "IT Service Manager generates SLA breach report within 24 hours of breach identification"
      # => 24-hour report generation SLA ensures breaches are acknowledged quickly,
      # => preventing accumulation of unacknowledged failures
    - step: 2
      action: "Root cause analysis completed within 5 business days"
    - step: 3
      action: "Remediation plan with owner and due date approved by IT Service Manager"
    - step: 4
      action: "Breach and remediation plan reported to business owner at next monthly service review"
      # => Business owner involvement ensures SLA management is a joint accountability,
      # => not purely an IT operational concern
    - step: 5
      action: "Remediation tracked in service improvement register; closure confirmed by business owner"

reporting:
  cadence: "Monthly service report to business owners; quarterly SLA trend review"
  metrics:
    - "Availability actual vs. target (by service)"
    - "SLA breach count and duration (by service)"
    - "OLA compliance rate (by team)"
    # => OLA compliance rate reveals whether internal teams are meeting their commitments —
    # => SLA breaches caused by OLA failures identify the accountable internal team
    - "Customer satisfaction score (post-incident survey)"
```

**Key Takeaway:** The OLA/SLA/underpinning contract stack ensures that every SLA commitment
to the business is backed by explicit internal and vendor commitments — when a breach occurs,
the accountability chain is traceable rather than diffused across anonymous team failures.

**Why It Matters:** Service Level Management fails when SLAs exist on paper but OLAs do not.
Internal teams that have no formal commitments aligned to customer-facing SLAs will not
prioritize SLA-related work over other demands. At Harborview Logistics, establishing OLAs
for each supporting team transforms SLA management from a reporting exercise into a shared
accountability system. The breach remediation workflow ensures that failures drive process
improvement rather than just apology emails.

---

## Example 36: ITIL 4 vs ITIL V5 — What Changed in February 2026

**What this covers:** ITIL V5 launched on February 12, 2026, introducing an 8-stage Product
and Service Lifecycle to replace ITIL 4's 6-activity Service Value Chain. This comparison
annotates the structural differences, terminology shifts, and migration considerations for
organizations already certified or trained on ITIL 4.

**Scenario:** Harborview Logistics (HVL) IT Service Manager received the ITIL V5 announcement
and must advise the CIO on whether to migrate training programs and tooling immediately or
maintain ITIL 4 practice while monitoring V5 adoption. The comparison informs that decision.

```markdown
# ITIL 4 vs ITIL V5 — Structural Comparison

# Purpose: Migration advisory for Harborview Logistics | Date: May 2026

## Service Value Chain (ITIL 4) vs Product and Service Lifecycle (ITIL V5)

| Dimension                | ITIL 4 (Current Certification Basis) | ITIL V5 (Launched Feb 12, 2026)                    | Migration Consideration                                                   |
| ------------------------ | ------------------------------------ | -------------------------------------------------- | ------------------------------------------------------------------------- |
| Core model name          | Service Value Chain (SVC)            | Product and Service Lifecycle (PSL)                | Rename is structural — the underlying logic of value co-creation persists |
| Number of stages         | 6 activities                         | 8 stages                                           | Two new stages reflect product thinking and lifecycle retirement          |
| SVC Activity: Plan       | Plan (strategy alignment)            | PSL Stage 1: Strategy and Direction                | Expanded — V5 explicitly connects IT strategy to product portfolio        |
| SVC Activity: Improve    | Improve (continual improvement)      | PSL Stage 8: Continual Improvement and Retirement  | Retirement is new — V5 formally closes the product lifecycle              |
| SVC Activity: Engage     | Engage (demand and relationship)     | PSL Stage 2: Demand and Portfolio Management       | Demand management elevated; portfolio management integrated               |
| SVC Activity: Design     | Design and Transition (combined)     | PSL Stage 3: Design (separate stage)               | V5 separates design from transition for clarity                           |
| SVC Activity: Transition | Design and Transition (combined)     | PSL Stage 4: Build and Transition (separate stage) | Build activity now explicit — V5 acknowledges custom development          |
| SVC Activity: Obtain     | Obtain/Build (combined)              | PSL Stage 5: Deploy and Operate                    | Deployment and operations unified in V5                                   |
| SVC Activity: Deliver    | Deliver and Support (combined)       | PSL Stages 6-7: Value Realization + Support        | Value realization is a new explicit stage — outcomes tracked formally     |
| Practices count          | 34 practices                         | 34 practices (refined, not replaced)               | Practice names and content updated; core practices remain                 |
| Guiding principles       | 7 guiding principles                 | 7 guiding principles (unchanged)                   | No change — principles are stable across versions                         |
| Certification path       | Foundation → Specialist → Leader     | New V5 certification path (mid-2026 rollout)       | Dual certification valid during transition period; confirm with Axelos    |

# --- Key V5 additions ---

# Product thinking: V5 treats services as products with full lifecycles including retirement;

# organizations that accumulate legacy services without formal retirement pay technical debt

# Value Realization stage: V5 makes benefits tracking an explicit PSL stage, not an afterthought;

# this aligns with IT governance expectation that investments demonstrate measurable outcomes

# Retirement: First ITIL version to formally address service decommissioning;

# HVL has 7 legacy applications with no decommission plan — V5 provides the framework

# --- Migration advisory for HVL ---

# Recommendation: Maintain ITIL 4 practice for next 12 months; adopt V5 in FY2027 planning cycle

# Rationale: ServiceNow ITIL 4 workflows are stable; V5 tooling integrations not yet mature

# Near-term action: Register one IT Service Manager for V5 Foundation pilot certification (Q3 2026)

# Risk: Competitors who adopt V5 value realization stage earlier gain benefits-tracking advantage
```

**Key Takeaway:** ITIL V5's most significant addition is the Product and Service Lifecycle's
formal retirement stage and value realization stage — both address gaps that ITIL 4
practitioners have worked around informally, and organizations with mature ITIL 4 programs
will find the transition more evolutionary than revolutionary.

**Why It Matters:** ITIL V5 represents a maturation of the framework toward product management
thinking, reflecting how IT organizations increasingly operate. The retirement stage alone
addresses a persistent governance gap: organizations accumulate services without formal
decommission processes, creating technical debt, security exposure from unpatched legacy
systems, and inflated support costs. HVL's seven legacy applications without a decommission
plan represent exactly the problem V5 was designed to address. The February 2026 launch makes
V5 awareness a current obligation for IT governance practitioners.

---

## Example 37: ISO/IEC 38500:2024 — Applied to Cloud Adoption Decision

**What this covers:** ISO/IEC 38500 defines six principles for governing IT: Responsibility,
Strategy, Acquisition, Performance, Conformance, and Human Behaviour. A governance decision
record applies all six principles to a major IT decision — in this case, a cloud adoption
proposal — producing a board-level recommendation with documented rationale.

**Scenario:** Pinnacle Healthcare Network (PHN), a 1,200-person regional hospital network,
is considering migrating its clinical applications to a public cloud platform. The CIO must
present a governance decision record to the board using ISO/IEC 38500 as the assessment
framework.

```markdown
# ISO/IEC 38500:2024 Governance Decision Record

# Organization: Pinnacle Healthcare Network (PHN)

# Decision: Cloud Adoption for Clinical Applications

# Date: May 2026 | Presenter: CIO | Audience: Board of Directors

## Proposal Summary

Migrate 12 clinical applications from on-premises data center to AWS GovCloud (US)
over 18 months. Estimated capital avoidance: $3.2M over 5 years.
Estimated migration investment: $1.8M.

## ISO/IEC 38500:2024 Principle Assessment

| Principle       | Assessment Question                                                           | Finding                                                                                               | Board Recommendation                                                            |
| --------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Responsibility  | Are accountabilities for cloud governance clearly assigned?                   | Current IT org has no cloud architect role; vendor management capability is limited                   | CONDITION: Approve contingent on hiring Cloud Architect before migration begins |
| Strategy        | Does cloud adoption align with PHN's 5-year digital health strategy?          | Strategy explicitly calls for "infrastructure modernization by 2028" — proposal is aligned            | SUPPORT: Strategic alignment confirmed                                          |
| Acquisition     | Is the cloud provider selection process sound and competitive?                | RFP conducted; AWS GovCloud selected; HIPAA BAA in place; 3-year pricing negotiated                   | SUPPORT: Acquisition process is adequate                                        |
| Performance     | Are performance requirements defined and measurable in the cloud model?       | SLA targets defined for 10 of 12 applications; 2 applications lack baseline performance metrics       | CONDITION: Approve contingent on baseline metrics established before migration  |
| Conformance     | Does cloud deployment meet HIPAA, HITECH, and state privacy law requirements? | AWS GovCloud is HIPAA-eligible; BAA executed; data residency confirmed US-only; legal review complete | SUPPORT: Conformance requirements met                                           |
| Human Behaviour | Are staff prepared for cloud operations model? Is change management planned?  | No cloud training program exists; staff AWS certification budget not in proposal                      | CONDITION: Approve contingent on training budget ($120K) added to business case |

# --- Governance assessment summary ---

# SUPPORT on 3 of 6 principles (Strategy, Acquisition, Conformance)

# CONDITION on 3 of 6 principles (Responsibility, Performance, Human Behaviour)

# No REJECT findings — proposal is fundamentally sound but underprepared on organizational readiness

# The three conditions must be satisfied before board approval is converted to a project mandate:

# 1. Cloud Architect role funded and posted (Responsibility)

# 2. Baseline performance metrics for all 12 applications documented (Performance)

# 3. $120K staff training budget added to business case (Human Behaviour)

# --- Board recommendation ---

# CONDITIONAL APPROVAL: CIO to return to board with evidence of three conditions met (Q3 2026)

# Board authorizes CIO to begin RFP for Cloud Architect role immediately
```

**Key Takeaway:** The ISO/IEC 38500 framework surfaces organizational readiness gaps that
financial and technical assessments miss — PHN's cloud proposal has strong strategic alignment
and conformance but fails on responsibility and human behaviour, which are the factors most
likely to cause cloud migrations to underperform.

**Why It Matters:** Cloud adoption decisions are among the highest-stakes IT governance choices
a healthcare organization makes, involving patient data privacy, operational continuity, and
multi-year financial commitments. Boards that evaluate cloud proposals through a purely financial
lens miss the governance dimensions that ISO/IEC 38500 structures. PHN's conditional approval
outcome — rather than blanket rejection or unconditioned approval — represents mature governance:
the board supports the strategic direction while demanding organizational readiness before
committing capital.

---

## Example 38: ISO 31000:2018 — Risk Treatment Plan

**What this covers:** ISO 31000:2018 defines risk treatment as the process of selecting and
implementing options to modify risk. A compliant treatment plan documents the risk description,
selected treatment option (treat/tolerate/transfer/terminate), controls to implement, residual
risk assessment, owner, timeline, and review date.

**Scenario:** Meridian Capital Partners (MCP) from Example 30 has identified a high-priority
risk in its APO12 register: inadequate controls around privileged access management for its
trading platform. The CIO must produce an ISO 31000:2018 risk treatment plan for the risk
committee.

```yaml
# ISO 31000:2018 Risk Treatment Plan
# Organization: Meridian Capital Partners (MCP)
# Risk ID: IT-RISK-2026-007
# Owner: CIO | Status: Approved | Version: 1.0

risk_description:
  risk_id: "IT-RISK-2026-007"
  risk_title: "Inadequate privileged access controls on trading platform"
  risk_statement: >
    Privileged accounts on the trading platform are not managed through a Privileged
    Access Management (PAM) solution. Shared credentials are used for database
    administration. Privileged session recording is absent.
  # => Risk statement follows ISO 31000 format: condition + absence of control + implication;
  # => this structure prevents ambiguous risk descriptions that cannot be acted upon
  risk_category: "Information Security / Operational Risk"
  affected_assets: ["Trading platform (revenue-critical)", "Client portfolio data", "Regulatory reporting database"]
  current_likelihood: HIGH
  current_impact: CRITICAL
  # => CRITICAL impact because trading platform compromise would trigger SEC breach notification,
  # => client notification, and potential regulatory action — existential financial exposure
  inherent_risk_rating: "CRITICAL (5x5 matrix score: 20/25)"

treatment_option_selected: TREAT
# => TREAT selected (not tolerate/transfer/terminate) because the risk exceeds MCP's risk appetite
# => and the controls required are technically feasible within the organization's budget authority;
# => transfer (cyber insurance) supplements but does not replace treatment

treatment_controls:
  - control_id: "PAM-01"
    control_name: "Deploy PAM solution for all privileged accounts"
    control_description: "Implement CyberArk Privileged Access Manager for all administrative accounts on trading platform and supporting infrastructure"
    implementation_steps:
      - "Complete PAM vendor selection (already done: CyberArk selected)"
      - "Deploy PAM vault for trading platform privileged accounts (Month 1-2)"
      - "Onboard all 23 privileged accounts into PAM (Month 2-3)"
      - "Enable session recording for all privileged sessions (Month 3)"
      - "Eliminate all shared credentials; enforce individual accountability (Month 3)"
    # => Session recording is the governance control that makes privileged access auditable;
    # => without recording, investigations into trading anomalies cannot attribute actions to individuals
    owner: CISO
    target_completion: "2026-08-31"
    estimated_cost_usd: 185000
    # => $185K includes license, implementation, and first-year support;
    # => cost is proportionate to CRITICAL risk rating — toleration would be far more expensive

  - control_id: "PAM-02"
    control_name: "Implement Just-In-Time (JIT) access for production databases"
    control_description: "Privileged access to production databases granted on-demand with time-limited sessions; no standing privileged access"
    owner: IT Operations Lead
    target_completion: "2026-09-30"
    estimated_cost_usd: 0
    # => JIT access is a configuration of the PAM solution (PAM-01), not a separate tool cost;
    # => implementation effort is internal — approximately 40 hours of IT operations time

  - control_id: "PAM-03"
    control_name: "Quarterly privileged access recertification"
    control_description: "All privileged accounts reviewed and recertified by business and IT owners every 90 days; unused accounts disabled within 5 days"
    owner: IT Risk Analyst
    target_completion: "2026-10-31"
    estimated_cost_usd: 0
    # => Recertification is a process control, not a technology cost;
    # => the PAM solution generates the recertification report; review is a governance obligation

residual_risk_assessment:
  residual_likelihood: LOW
  residual_impact: HIGH
  # => Impact remains HIGH after treatment because a PAM solution reduces breach probability
  # => but cannot eliminate the impact if trading platform data is compromised —
  # => residual impact reflects inherent business value of the protected asset
  residual_risk_rating: "MEDIUM (3x4 matrix score: 12/25)"
  within_risk_appetite: true
  # => MEDIUM residual risk is within MCP's defined risk appetite threshold of <=MEDIUM
  # => for IT operational risks; this treatment plan achieves the governance objective

treatment_plan_governance:
  risk_owner: CIO
  treatment_owner: CISO
  risk_committee_approval_date: "2026-05-15"
  next_review_date: "2026-09-30"
  # => Review date set to September 30 to coincide with PAM-02 completion;
  # => risk register updated after each control implementation to track residual risk reduction
  reporting_cadence: "Monthly status to CIO; quarterly update to risk committee"
  escalation_trigger: "Any control milestone delayed >30 days triggers CIO escalation to CEO"
```

**Key Takeaway:** The ISO 31000:2018 treatment plan at MCP demonstrates that "treat" means
implementing specific controls with owners, timelines, and costs — not a generic commitment
to "improve security" — and that residual risk must be explicitly assessed against the
organization's defined risk appetite to confirm the treatment is sufficient.

**Why It Matters:** Risk treatment plans that lack specificity fail at implementation. The
controls-with-owners model ensures accountability: when PAM-01 misses its August deadline,
the CISO is accountable, not "the IT team." The $185,000 PAM investment is justified against
a CRITICAL risk rating — organizations that delay PAM implementations due to cost typically
discover the cost of a privileged account compromise far exceeds the control investment. The
JIT access control (PAM-02) at zero marginal cost represents the governance principle of
maximum risk reduction per dollar of treatment investment.

---

## Example 39: ISO 27001:2022 as a Governance Instrument

**What this covers:** ISO 27001:2022 Annex A contains 93 controls organized in 4 clauses
(Organizational, People, Physical, Technological). A Statement of Applicability (SoA) excerpt
demonstrates how individual controls are used as governance instruments — each with an
applicability decision, justification, implementation status, and named governance owner.

**Scenario:** Apex Data Processing Ltd. (a cloud payroll processor from Example 31's reference
context) is building a governance-focused SoA excerpt. The CISO presents 10 Annex A controls
to the audit committee, emphasizing governance ownership as a certification readiness indicator.

```markdown
# ISO 27001:2022 Statement of Applicability — Governance Excerpt

# Organization: Apex Data Processing Ltd. | Version: 2.1 | Date: May 2026

# CISO Approval: Signed | Senior Management Approval: Signed

| Control ID | Control Name                               | Applicable? | Governance Owner      | Implementation Status | Justification                                                                               |
| ---------- | ------------------------------------------ | ----------- | --------------------- | --------------------- | ------------------------------------------------------------------------------------------- |
| 5.1        | Policies for information security          | YES         | CISO                  | Implemented           | Mandatory governance foundation; policy suite reviewed annually by CISO and approved by CEO |
| 5.2        | Information security roles and resp.       | YES         | CISO + HR Director    | Implemented           | RACI matrix defined; security responsibilities in all job descriptions >access to PII       |
| 5.4        | Management responsibilities                | YES         | CEO                   | Implemented           | CEO sign-off on ISMS scope; management review meetings quarterly                            |
| 5.10       | Acceptable use of information              | YES         | CISO                  | Implemented           | Acceptable use policy signed by all staff at onboarding and annually thereafter             |
| 5.19       | Information security in supplier rel.      | YES         | Procurement + CISO    | Partially implemented | Tier 1 vendor assessments complete; Tier 2 assessment process under development             |
| 5.23       | Information security for cloud services    | YES         | CTO + CISO            | Partially implemented | AWS BAA and Azure BAA executed; CSP shared responsibility matrix documented                 |
| 5.29       | Information security during disruption     | YES         | CTO + BC Coordinator  | Implemented           | ISMS controls maintained during BCP activation; DR tested annually                          |
| 5.33       | Protection of records                      | YES         | Legal + CISO          | Implemented           | Retention schedule aligned to GDPR Art.5(1)(e) and payroll regulatory obligations           |
| 5.35       | Independent review of information security | YES         | Board Audit Committee | Implemented           | Annual third-party ISMS audit; results reported to board audit committee                    |
| 8.8        | Management of technical vulnerabilities    | YES         | IT Operations + CISO  | Implemented           | Monthly vulnerability scans; patching SLA enforced; exception process documented            |

# --- Governance owner assignment notes ---

# Control 5.1 (Policies): CISO owns the control; CEO approves — separation of ownership

# and approval ensures policy legitimacy beyond the security function

# Control 5.4 (Management responsibilities): Assigned to CEO, not CISO — ISO 27001

# requires top management accountability, not delegation to security function

# Control 5.35 (Independent review): Assigned to Board Audit Committee — independence

# requires oversight outside the management chain that operates the ISMS

# Control 5.19 (Supplier relations): PARTIALLY IMPLEMENTED — Tier 2 vendors process

# gap is a known risk; remediation timeline: Q3 2026; noted in risk register

# Control 5.23 (Cloud services): PARTIALLY IMPLEMENTED — new in ISO 27001:2022;

# shared responsibility matrix complete but cloud security posture management (CSPM) tooling

# not yet deployed; CSPM implementation planned Q4 2026

# --- Governance accountability principles applied ---

# Each control has exactly one accountable governance owner (not "IT" generically)

# Partially implemented controls have explicit timelines and risk register entries

# Board-level controls (5.4, 5.35) assigned outside IT to preserve independence
```

**Key Takeaway:** Assigning governance owners at the named-role level (not "IT department")
transforms the SoA from a compliance checklist into an accountability instrument — and the
board audit committee ownership of 5.35 signals that independent review operates above the
management chain that runs the ISMS.

**Why It Matters:** ISO 27001:2022 certification without governance ownership assignment is
a documentation exercise that passes Stage 1 audit but fails during Stage 2 evidence testing.
When an auditor asks "who approved this policy?" the answer must be a named role with a
documented decision, not a vague departmental reference. Apex Data Processing's governance-first
SoA approach — with CEO ownership of management responsibilities and board audit committee
ownership of independent review — demonstrates the mature separation of roles that enterprise
customers and regulators expect from a cloud payroll processor handling sensitive employee data.

---

## Example 40: NIST CSF 2.0 Govern Function

**What this covers:** NIST CSF 2.0 added the Govern (GV) function as a new sixth function in
2024, encompassing six categories: Organizational Context (GV.OC), Risk Management Strategy
(GV.RM), Roles and Responsibilities (GV.RR), Policy (GV.PO), Oversight (GV.OV), and
Cybersecurity Supply Chain Risk Management (GV.SC). This example annotates practical
implementation actions for each category.

**Scenario:** Meridian Financial Services (MFS), the regional bank from Example 29's reference
context, is implementing NIST CSF 2.0 to satisfy a regulatory examination expectation.
The CISO maps the Govern function to concrete actions in the bank's operating environment.

```yaml
# NIST CSF 2.0 Govern Function Implementation
# Organization: Meridian Financial Services (MFS)
# Owner: CISO | Regulatory Context: FFIEC, SOX, state banking regulations

govern_function:
  GV_OC:
    category: "Organizational Context"
    subcategories:
      GV.OC-01:
        description: "Mission, stakeholder expectations, and legal/regulatory requirements identified"
        mfs_action: "Document MFS mission statement's information security implications; map to FFIEC Cybersecurity Assessment Tool requirements"
        # => Financial institutions must connect cybersecurity to mission — "protect depositor funds"
        # => is the mission context that makes data integrity controls non-negotiable for MFS
        current_status: "Implemented"
        evidence: "Mission-aligned security charter signed by CEO (Jan 2026)"
      GV.OC-05:
        description: "Outcomes, capabilities, and services that the organization depends on are understood"
        mfs_action: "Complete business impact analysis for all 18 IT services; identify critical dependencies on third-party payment processors"
        current_status: "Partially implemented"
        gap: "Payment processor dependency mapping incomplete"
        # => Payment processor dependency is a systemic risk for banks — a single processor
        # => outage can halt all card transactions; dependency mapping is a governance prerequisite

  GV_RM:
    category: "Risk Management Strategy"
    subcategories:
      GV.RM-01:
        description: "Risk management objectives established and agreed to by organizational stakeholders"
        mfs_action: "Board-approved risk appetite statement with quantitative thresholds (e.g., maximum acceptable annualized loss exposure per risk category)"
        current_status: "Partially implemented"
        gap: "Risk appetite statement exists but lacks quantitative thresholds"
        # => Qualitative risk appetite ("low tolerance for operational risk") is insufficient
        # => for NIST CSF 2.0 compliance — MFS must define dollar thresholds boards can vote on
      GV.RM-06:
        description: "Policies, processes, procedures, and practices to manage cybersecurity risks established"
        mfs_action: "Consolidate 14 disparate security policies into integrated risk management framework aligned to CSF 2.0"
        current_status: "In progress"
        target_date: "2026-Q3"
        # => 14 separate policies without framework alignment create gaps and overlaps;
        # => CSF 2.0 adoption is the forcing function to rationalize the policy architecture

  GV_RR:
    category: "Roles, Responsibilities, and Authorities"
    subcategories:
      GV.RR-01:
        description: "Organizational leadership responsible and accountable for cybersecurity risk"
        mfs_action: "Board resolution assigning cybersecurity risk accountability to CEO with CISO as designated senior officer"
        current_status: "Implemented"
        evidence: "Board resolution 2026-001 (January 2026)"
        # => Board resolution is stronger than job description — it creates governance record
        # => of explicit board-level assignment that examination teams can verify
      GV.RR-02:
        description: "Roles, responsibilities, and authorities for cybersecurity risk management established"
        mfs_action: "Publish RACI matrix for all 34 NIST CSF 2.0 practices; integrate into job descriptions during next review cycle"
        current_status: "In progress"
        target_date: "2026-Q4"

  GV_PO:
    category: "Policy"
    subcategories:
      GV.PO-01:
        description: "Policy for managing cybersecurity risks established and communicated"
        mfs_action: "Publish consolidated cybersecurity risk management policy; all-staff communication and annual attestation"
        current_status: "Partially implemented"
        gap: "Annual attestation process not yet established"
        # => Annual attestation creates an evidence trail that staff acknowledged policy obligations;
        # => without attestation, "policy communicated" is an unverifiable assertion at audit
      GV.PO-02:
        description: "Policy aligned to regulations, legal requirements, contractual obligations"
        mfs_action: "Conduct annual policy-to-regulation mapping review; document alignment gaps in compliance register"
        current_status: "Implemented"

  GV_OV:
    category: "Oversight"
    subcategories:
      GV.OV-01:
        description: "Cybersecurity risk management strategy outcomes reviewed to inform and adjust strategy"
        mfs_action: "Quarterly board cybersecurity report with KPI performance vs. risk appetite; strategy adjustment documented in board minutes"
        current_status: "Implemented"
        # => Board minutes documenting strategy adjustments are examination evidence —
        # => they prove the board is actively governing, not passively receiving reports
      GV.OV-03:
        description: "Organizational cybersecurity risk management performance is evaluated and reviewed"
        mfs_action: "Annual independent assessment of CSF 2.0 Govern function maturity by external advisor"
        current_status: "Planned"
        target_date: "2026-Q4"

  GV_SC:
    category: "Cybersecurity Supply Chain Risk Management"
    subcategories:
      GV.SC-01:
        description: "Cybersecurity supply chain risk management program established, approved, and communicated"
        mfs_action: "Establish vendor risk management program with tiered due diligence (see Example 46); integrate with procurement onboarding workflow"
        current_status: "Partially implemented"
        # => Supply chain risk management is the most common CSF 2.0 Govern gap for mid-sized
        # => financial institutions — vendor oversight programs exist but are not systematized
      GV.SC-06:
        description: "Planning and due diligence performed to better understand and communicate risks from suppliers"
        mfs_action: "Annual security questionnaire for Tier 1 vendors; right-to-audit clause in all new vendor contracts"
        current_status: "In progress"
        target_date: "2026-Q3"
```

**Key Takeaway:** The NIST CSF 2.0 Govern function is architecturally foundational — it
ensures that the Identify, Protect, Detect, Respond, and Recover functions operate within
a defined strategy, with clear accountability and board oversight, rather than as
independently managed technical programs.

**Why It Matters:** Organizations that implement CSF 2.0 without prioritizing the Govern
function build technically capable security programs that lack strategic coherence. The Govern
function's six categories address the governance gaps that regulators — particularly FFIEC
examiners at financial institutions — most commonly cite in examination findings: undefined
risk appetite, unclear board accountability, inconsistent policy structures, and unmanaged
third-party risk. MFS's partial implementation status on GV.RM-01 (risk appetite thresholds)
is the single highest-priority remediation item because every other governance decision depends
on quantitative risk appetite definitions.

---

## Example 41: SOC 2 Governance Requirements

**What this covers:** SOC 2 defines five Trust Services Criteria (TSC): Security (CC — Common
Criteria), Availability (A), Processing Integrity (PI), Confidentiality (C), and Privacy (P).
A governance control mapping documents the controls satisfying each criterion, names the
evidence owner, and specifies evidence collection frequency for audit readiness.

**Scenario:** Apex Data Processing Ltd. (cloud payroll processor) is preparing for its annual
SOC 2 Type II audit. The CISO maps governance controls to all five TSC categories, with
evidence collection responsibilities assigned to named owners.

```markdown
# SOC 2 Governance Control Mapping — Apex Data Processing Ltd.

# Audit Period: June 2025 – May 2026 | Auditor: External CPA Firm

# Owner: CISO | Status: Pre-audit readiness review

## Trust Services Criteria Control Mapping

| TSC Category         | Control                                                       | Governance Owner      | Evidence Type                                  | Collection Frequency    | Status      |
| -------------------- | ------------------------------------------------------------- | --------------------- | ---------------------------------------------- | ----------------------- | ----------- |
| CC (Security)        | Access control: RBAC enforced for all payroll system users    | CISO                  | Access control matrix; quarterly access review | Quarterly               | Implemented |
| CC (Security)        | MFA enforced for all administrative access                    | IT Operations Lead    | MFA enrollment report from IdP                 | Monthly snapshot        | Implemented |
| CC (Security)        | Security awareness training ≥95% completion annually          | CISO + HR             | LMS completion report                          | Annual                  | Implemented |
| CC (Security)        | Penetration test conducted annually by independent firm       | CISO                  | Pentest report + remediation tracking          | Annual                  | Implemented |
| CC (Security)        | Change management process: all changes via approved CAB       | IT Service Manager    | CAB meeting minutes; change ticket log         | Per change + monthly    | Implemented |
| A (Availability)     | System availability monitored 24x7 with alerting              | IT Operations Lead    | Uptime monitoring dashboard; alert log         | Continuous              | Implemented |
| A (Availability)     | RTO and RPO defined and tested annually for critical systems  | BC Coordinator        | DR test results; RTO/RPO documentation         | Annual                  | Implemented |
| A (Availability)     | Redundant infrastructure (N+1) for payroll processing         | CTO                   | Architecture diagram; failover test results    | Annual review           | Implemented |
| PI (Proc. Integrity) | Payroll calculation validation controls with exception log    | Application Lead      | Exception log; reconciliation reports          | Per processing cycle    | Implemented |
| PI (Proc. Integrity) | Input data validation rules documented and tested             | QA Lead               | Test case results; validation rule inventory   | Per release             | Implemented |
| C (Confidentiality)  | Data classification policy enforced; payroll data classified  | CISO + Legal          | Classification policy; DLP configuration       | Annual review           | Implemented |
| C (Confidentiality)  | Encryption at rest (AES-256) and in transit (TLS 1.3)         | CTO                   | Encryption configuration evidence              | Annual audit            | Implemented |
| P (Privacy)          | Privacy notice published and current                          | Legal + CISO          | Privacy notice with publication date           | Annual review           | Implemented |
| P (Privacy)          | GDPR/CCPA data subject request process documented             | Legal                 | DSAR procedure; response log                   | Per request + quarterly | Implemented |
| P (Privacy)          | Data retention schedule enforced; deletion records maintained | Legal + IT Operations | Retention schedule; deletion certificates      | Annual + per deletion   | Implemented |

# --- Audit readiness notes ---

# TYPE II audit covers operating effectiveness over the full 12-month period:

# point-in-time evidence (e.g., a single access review) is insufficient;

# auditors will sample multiple periods — quarterly evidence must exist for all quarterly controls

# Highest audit failure risk: CC-Security access review evidence

# Required: four quarterly access reviews for the June 2025–May 2026 period

# Current status: three completed; Q4 (March 2026) review evidence archived

# Processing Integrity (PI) criterion is selected (not all SOC 2 audits include PI):

# Apex selected PI because payroll calculation errors are a material business risk

# and customer contracts require PI attestation

# Privacy (P) criterion is included because Apex processes EU employee data (GDPR scope):

# P criterion provides additional assurance to European employer customers
```

**Key Takeaway:** SOC 2 governance control mapping reveals that the highest audit risk is
not absent controls but incomplete evidence trails — quarterly controls with only three of
four periods documented will generate qualified findings despite fully operational controls.

**Why It Matters:** SOC 2 Type II audits assess operating effectiveness over time, not just
design adequacy. Organizations that implement strong controls but fail to collect and retain
evidence systematically will fail Type II audits on controls that are technically functioning.
For Apex Data Processing, whose enterprise clients contractually require SOC 2 attestation,
a qualified audit report creates customer notification obligations and contract renewal risk.
The evidence collection frequency column in this mapping is not administrative overhead — it
is the governance cadence that makes Type II attestation achievable.

---

## Example 42: GDPR Data Governance Obligations

**What this covers:** The GDPR requires data controllers to maintain a Record of Processing
Activities (ROPA) documenting each processing activity with controller identity, purpose, legal
basis, data subject categories, retention period, and third-party transfer mechanisms. The ROPA
is both a compliance obligation and a data governance instrument.

**Scenario:** Apex Data Processing Ltd. processes payroll data for European employer clients
as a data processor, and also operates its own HR systems as a data controller. The DPO
produces a ROPA excerpt covering four processing activities with governance accountability
assignments.

```markdown
# Record of Processing Activities (ROPA) — Apex Data Processing Ltd.

# Role: Data Controller (own HR) + Data Processor (client payroll)

# DPO: Data Protection Officer | Last Updated: May 2026

## ROPA Entries

### Activity 1: Employee Payroll Processing (Controller Role — own employees)

| Field                 | Value                                                                                           |
| --------------------- | ----------------------------------------------------------------------------------------------- |
| Processing Activity   | Employee payroll calculation and payment                                                        |
| Data Controller       | Apex Data Processing Ltd. (registered: UK)                                                      |
| Purpose               | Fulfillment of employment contract; legal payroll obligations under UK Employment Rights Act    |
| Legal Basis           | Art. 6(1)(b) — necessary for performance of employment contract                                 |
| Data Subjects         | All Apex employees (current and within retention period)                                        |
| Data Categories       | Name, national insurance number, bank account, salary, tax code, pension contribution           |
| Retention Period      | 6 years post-employment (UK tax law obligation)                                                 |
| Third-Party Transfers | HMRC (legal obligation); pension provider (contractual); payroll software vendor (DPA in place) |
| Transfer Mechanism    | UK-only for HMRC; Standard Contractual Clauses for pension provider (EU server)                 |
| Governance Owner      | HR Director (processing accountability) + CISO (security of processing)                         |

# => Legal basis Art. 6(1)(b) — contract performance — is correct for employee payroll;

# => consent would be inappropriate here as employees cannot meaningfully withhold consent

# => for processing required to pay them

### Activity 2: Client Payroll Processing (Processor Role)

| Field               | Value                                                                                        |
| ------------------- | -------------------------------------------------------------------------------------------- |
| Processing Activity | Payroll calculation and disbursement on behalf of employer clients                           |
| Data Controller     | Employer clients (each client is the controller; Apex acts as processor)                     |
| Data Processor      | Apex Data Processing Ltd.                                                                    |
| Purpose             | Fulfillment of Data Processing Agreement (DPA) with each client controller                   |
| Legal Basis         | Art. 6(1)(b) — as determined by each controller; Apex processes under controller instruction |
| Data Subjects       | Client employer's employees (EU residents where GDPR applies)                                |
| Data Categories     | Employee PII, salary, banking, tax — per client DPA schedule                                 |
| Retention Period    | Per client DPA; default 7 years; earlier deletion on client instruction                      |
| Sub-processors      | AWS (infrastructure — SCCs executed); Salesforce (CRM — SCCs executed)                       |
| Governance Owner    | CTO (sub-processor management) + Legal (DPA compliance)                                      |

# => As a processor, Apex does not set the legal basis — the controller does;

# => Apex's obligation is to process only per controller instructions (Art. 29)

# => and to notify the controller of any sub-processor changes (Art. 28(2))

### Activity 3: Website Analytics

| Field                 | Value                                                                     |
| --------------------- | ------------------------------------------------------------------------- |
| Processing Activity   | Website visitor behaviour analytics                                       |
| Data Controller       | Apex Data Processing Ltd.                                                 |
| Purpose               | Improve website usability; measure marketing campaign effectiveness       |
| Legal Basis           | Art. 6(1)(a) — consent via cookie banner                                  |
| Data Subjects         | Website visitors who consent to analytics cookies                         |
| Data Categories       | IP address, browser type, pages visited, session duration (pseudonymised) |
| Retention Period      | 13 months (Google Analytics default; configured in GA4 settings)          |
| Third-Party Transfers | Google LLC (US) — Google Analytics 4                                      |
| Transfer Mechanism    | Standard Contractual Clauses (Google's EU SCCs)                           |
| Governance Owner      | Marketing Director (purpose) + CISO (consent management)                  |

# => Consent is required for analytics cookies — legitimate interest is not valid

# => for non-essential tracking under GDPR and UK PECR; consent banner must provide

# => granular choice and record consent with timestamp

# --- ROPA governance requirements ---

# ROPA must be maintained in writing (Art. 30(3)) — email threads do not satisfy this obligation

# ROPA available to supervisory authority on request — completion and accuracy is a compliance obligation

# 72-hour breach notification (Art. 33): ROPA enables rapid identification of affected data categories

# Annual ROPA review: DPO reviews all entries; controllers validate retention periods and legal bases

# New processing activities: ROPA entry required before processing begins (not retrospectively)
```

**Key Takeaway:** The ROPA's governance value extends beyond regulatory compliance — when
a data breach occurs, the ROPA enables the 72-hour notification obligation to be met by
providing an immediate, accurate inventory of affected processing activities, data subjects,
and third-party transfers.

**Why It Matters:** Organizations without a current ROPA discover its importance at the worst
possible moment: during a breach, when the 72-hour clock has already started. Apex Data
Processing's dual role as controller and processor creates ROPA complexity that many mid-sized
SaaS companies mishandle — processor activities are often omitted on the incorrect assumption
that the controller bears all documentation obligations. GDPR Art. 30 requires processors
to maintain their own ROPA for processing on behalf of controllers. The governance ownership
assignments in the ROPA convert documentation into operational accountability.

---

## Example 43: PCI DSS v4.0 Governance Requirements

**What this covers:** PCI DSS v4.0 (mandatory compliance since March 2025) places
board-level governance obligations primarily in Requirement 12 (Information Security Policy).
Requirement 12 mandates a targeted risk analysis methodology, board acknowledgment of the
security policy, and documentation obligations that make information security governance an
explicit board accountability rather than a delegated IT function.

**Scenario:** Crestview Insurance Group (CIG) from Example 31 also accepts payment cards for
premium collections, making it a Level 3 PCI DSS merchant. The CIO must demonstrate
Requirement 12 compliance to the Qualified Security Assessor (QSA) and prepare board
acknowledgment artifacts.

```markdown
# PCI DSS v4.0 Requirement 12 — Board Accountability Obligations

# Organization: Crestview Insurance Group (CIG) | QSA Assessment: Q3 2026

# Merchant Level: Level 3 (20,000–1,000,000 card transactions/year)

## Requirement 12.1 — Information Security Policy

| Sub-Req | Requirement                                                            | CIG Implementation                                                         | Evidence for QSA                                           | Status    |
| ------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------- | --------- |
| 12.1.1  | Overall information security policy established, published, maintained | Consolidated IS Policy v3.2 published on intranet; email notification sent | Policy document with version history; intranet publication | Compliant |
| 12.1.2  | IS policy reviewed at least once every 12 months                       | Annual review cycle; last review February 2026; next due February 2027     | Signed review memo with date; tracked in policy register   | Compliant |
| 12.1.3  | IS policy defines roles and responsibilities for all personnel         | RACI matrix appended to IS Policy; referenced in all job descriptions      | IS Policy Appendix A (RACI); sample job descriptions       | Compliant |

## Requirement 12.2 — Targeted Risk Analysis

| Sub-Req | Requirement                                                                           | CIG Implementation                                                                       | Evidence for QSA                                       | Status    |
| ------- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------ | --------- |
| 12.2.1  | Targeted risk analysis for each PCI DSS requirement allowing flexibility in frequency | TRA documented for 8 flexible-frequency requirements; methodology follows NIST SP 800-30 | TRA document set; methodology documentation            | Compliant |
| 12.2.1a | TRA performed by qualified personnel; approved by senior management                   | TRA performed by IT Risk Analyst; approved by CIO (delegated by Board Risk Committee)    | TRA approval signature page; Board Risk Committee min. | Compliant |

# --- Targeted Risk Analysis methodology notes ---

# PCI DSS v4.0 introduced TRA to replace one-size-fits-all frequencies;

# organizations must now justify frequency decisions with documented risk analysis

# CIG's TRA for requirement 12.6.3 (security awareness training):

# Risk: Phishing is top threat vector for insurance sector; training frequency directly reduces

# susceptibility; TRA conclusion: annual training insufficient; semi-annual training justified

# Board approval: Risk Committee resolution 2026-002

## Requirement 12.4 — Board Accountability for PCI DSS Compliance

| Sub-Req | Requirement                                                                           | CIG Implementation                                                                        | Evidence                                            | Status    |
| ------- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | --------------------------------------------------- | --------- |
| 12.4.1  | Executive management establish responsibility for cardholder data protection          | Board resolution assigning CIO as Responsible Executive for PCI DSS compliance (Jan 2026) | Board minutes; CIO appointment letter               | Compliant |
| 12.4.2  | PCI DSS compliance program reviewed by executive management at least once every 12 mo | Annual PCI DSS compliance review presented to board; last review March 2026               | Board presentation with date; signed acknowledgment | Compliant |

## Requirement 12.5 — PCI DSS Scope Documentation

| Sub-Req | Requirement                                                                         | CIG Implementation                                                   | Evidence                                               | Status    |
| ------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------ | --------- |
| 12.5.1  | Inventory of system components in scope for PCI DSS maintained                      | Cardholder Data Environment (CDE) asset inventory maintained in CMDB | CMDB export with CDE tag; network segmentation diagram | Compliant |
| 12.5.2  | PCI DSS scope confirmed at least once every 12 months and after significant changes | Scope confirmation conducted annually; triggered by network changes  | Scope confirmation report with date; change log        | Compliant |

# --- QSA audit preparation notes ---

# QSA will interview board members to verify 12.4.1 — the board resolution alone

# is insufficient; directors must be able to articulate their oversight role

# Targeted Risk Analysis documents must show genuine risk reasoning, not template text;

# QSAs are trained to identify TRAs that are copies of vendor templates without org-specific analysis

# Requirement 12.1.2 annual review: QSA will check version history — policies

# with no tracked changes suggest review is a formality, not a genuine assessment
```

**Key Takeaway:** PCI DSS v4.0's Requirement 12.4 makes board-level oversight of the PCI
DSS compliance program an explicit, auditable obligation — the board must not only approve
the security policy but acknowledge the compliance program annually through documented review.

**Why It Matters:** PCI DSS v4.0's shift to board accountability signals that payment card
security is now a governance obligation, not just an IT operational matter. The targeted risk
analysis requirement removes the previous regime's prescriptive frequencies, replacing them
with documented, justified, management-approved decisions. Organizations that treat TRA as a
template exercise will fail QSA scrutiny. For Crestview Insurance Group, whose payment card
exposure is limited to premium collections, compliance effort is proportionate — but the board
accountability requirements apply regardless of merchant level or transaction volume.

---

## Example 44: FAIR Risk Quantification

**What this covers:** The FAIR (Factor Analysis of Information Risk) model quantifies IT risk
in financial terms using a two-factor structure: Loss Event Frequency (LEF = Threat Event
Frequency × Vulnerability) and Probable Loss Magnitude (PLM = Primary Loss + Secondary Loss).
The product of LEF and PLM produces Annualized Loss Exposure (ALE) in dollars.

**Scenario:** Meridian Capital Partners (MCP) from Example 30 needs to present the privileged
access risk (IT-RISK-2026-007) to the board risk committee in financial terms. The IT Risk
Analyst applies the FAIR model to produce an ALE estimate that supports the $185,000 PAM
investment case.

```yaml
# FAIR Risk Quantification — IT-RISK-2026-007
# Organization: Meridian Capital Partners (MCP)
# Risk: Inadequate privileged access controls on trading platform
# Analyst: IT Risk Analyst | Review Date: May 2026

fair_model:
  threat_scenario:
    description: "Malicious insider or compromised privileged account exfiltrates client portfolio data from trading platform"
    threat_actor: "Malicious insider (primary) + External attacker with stolen credentials (secondary)"
    # => Two threat actors are modeled separately in full FAIR analysis; for board presentation
    # => the higher-frequency scenario (insider) drives the primary ALE calculation

  loss_event_frequency:
    # => LEF = Threat Event Frequency × Vulnerability
    # => LEF answers: "How often will a loss event occur in a given year?"

    threat_event_frequency:
      value_per_year: 2.0
      basis: >
        MCP operates in asset management sector with elevated insider threat exposure.
        FS-ISAC data: privileged account misuse incidents at peer firms average 1-3 per year
        for organizations of MCP's size and sector profile.
      # => TEF of 2.0/year means MCP expects approximately two privileged access threat
      # => events per year — not necessarily successful, but requiring investigation

    vulnerability:
      value: 0.65
      # => Vulnerability expressed as probability (0-1) that a threat event results in a loss event
      basis: >
        Current controls assessment: no PAM solution, shared credentials, no session recording.
        With these control gaps, 65% of privileged access threat events are estimated to result
        in successful unauthorized access. Industry benchmark for PAM-mature organizations: 15%.
      # => 0.65 vulnerability is high — reflecting the absence of preventive controls;
      # => PAM implementation (PAM-01) is projected to reduce this to approximately 0.15

    loss_event_frequency_result:
      calculation: "TEF (2.0) × Vulnerability (0.65) = 1.3 loss events per year"
      value_per_year: 1.3
      # => 1.3 expected loss events per year is the foundation of the ALE calculation;
      # => this is a probabilistic estimate, not a deterministic prediction

  probable_loss_magnitude:
    # => PLM = Primary Loss Magnitude + Secondary Loss Magnitude
    # => PLM answers: "How much does a single loss event cost?"

    primary_loss_magnitude:
      components:
        - category: "Response costs"
          description: "Incident response, forensics, legal counsel, system restoration"
          estimate_usd: 350000
          # => Forensic investigation for a trading platform breach typically requires
          # => specialized financial services IR firm — $200-400K range based on peer incidents

        - category: "Productivity loss"
          description: "Trading platform downtime, staff time for investigation and remediation"
          estimate_usd: 180000
          # => 3-day trading platform downtime × daily revenue impact; staff time at loaded cost

        - category: "Asset replacement"
          description: "Credential rotation, system rebuild if compromise is extensive"
          estimate_usd: 45000

      primary_total_usd: 575000

    secondary_loss_magnitude:
      components:
        - category: "Regulatory fines"
          description: "SEC Rule 17a-4 and Reg SP notification failures; FINRA examination findings"
          estimate_usd: 500000
          # => SEC and FINRA have fined asset managers $250K-$1M+ for client data breaches
          # => without adequate safeguards; $500K is a conservative mid-range estimate

        - category: "Client notification and remediation"
          description: "Written notification to affected clients; credit monitoring provision if PII exposed"
          estimate_usd: 125000

        - category: "Reputational damage"
          description: "AUM reduction from client withdrawals following publicized breach"
          estimate_usd: 2500000
          # => Asset managers are acutely vulnerable to reputational loss — a single publicized
          # => breach at a 300-person firm can trigger 10-15% AUM reduction; $2.5M represents
          # => lost management fees on estimated $250M AUM outflow over 24 months

      secondary_total_usd: 3125000

    probable_loss_magnitude_result:
      primary_usd: 575000
      secondary_usd: 3125000
      total_plm_usd: 3700000
      # => Total PLM of $3.7M includes both direct costs and consequential losses;
      # => secondary losses (regulatory + reputational) dominate, as is typical for financial sector

  annualized_loss_exposure:
    calculation: "LEF (1.3) × PLM ($3,700,000) = $4,810,000 per year"
    ale_usd: 4810000
    # => ALE of $4.81M/year is the expected annual cost of this risk without additional controls;
    # => this is the economic case for any control investment up to $4.81M annually

  investment_justification:
    control_investment_usd: 185000
    # => PAM-01 investment is $185K one-time + ~$60K/year maintenance
    projected_ale_reduction_pct: 77
    # => PAM reduces vulnerability from 0.65 to ~0.15; recalculated LEF: 2.0 × 0.15 = 0.3;
    # => residual ALE: 0.3 × $3,700,000 = $1,110,000; reduction: $3,700,000 (77% of original ALE)
    projected_ale_post_control_usd: 1110000
    net_benefit_year_1_usd: 3515000
    # => Year 1 net benefit: $3,700,000 ALE reduction - $185,000 investment = $3,515,000
    roi_ratio: "19:1"
    # => 19:1 ROI for the PAM investment — a board-consumable metric that justifies approval
    # => without requiring board members to understand PAM technology
```

**Key Takeaway:** The FAIR model transforms the PAM investment from a security request into
a financial decision: a $185,000 control eliminates $3.7 million of annual expected loss,
delivering a 19:1 return — a calculation that board members can evaluate using the same
logic they apply to any capital investment.

**Why It Matters:** Boards approve capital investments based on financial returns, not
technical risk descriptions. The FAIR model is the governance bridge between IT risk
analysis and board-level investment decisions. At Meridian Capital Partners, the PAM business
case would likely fail without quantification — "we need privileged access management to
reduce insider threat risk" competes poorly for budget against revenue-generating initiatives.
"This $185,000 investment eliminates $4.8 million of annual expected loss" does not. FAIR's
two-factor structure (frequency × magnitude) also reveals where the risk reduction comes from:
reducing vulnerability through controls, not accepting the risk or hoping threat frequency decreases.

---

## Example 45: Enterprise Risk Management Integration

**What this covers:** IT risks that exceed a defined materiality threshold must escalate
to the Enterprise Risk Management (ERM) register where they are evaluated alongside financial,
operational, strategic, and compliance risks. An ERM register row shows how an IT risk is
translated into business impact language, aligned with ERM treatment strategy, and reported
to the board at the appropriate threshold.

**Scenario:** Meridian Capital Partners (MCP) identifies that the privileged access risk
(IT-RISK-2026-007 from Example 44) qualifies for ERM escalation based on its ALE of
$4.81 million. The CRO integrates the risk into the enterprise register for board reporting.

```yaml
# ERM Register — Escalated IT Risk Entry
# Organization: Meridian Capital Partners (MCP)
# Source Risk: IT-RISK-2026-007 (Inadequate PAM on trading platform)
# ERM Entry ID: ERM-2026-014

erm_register_entry:
  entry_id: "ERM-2026-014"
  source_risk_id: "IT-RISK-2026-007"
  # => Source risk ID links the ERM entry back to the IT risk register;
  # => this traceability ensures the CRO and CIO maintain a single source of truth
  # => rather than managing parallel risk descriptions that drift apart over time

  risk_title: "Privileged Account Compromise — Trading Platform"
  risk_category: "Operational Risk (IT sub-category)"
  # => ERM categories are broader than IT risk categories; "Operational Risk" is the
  # => Basel II/III category that most financial sector ERM frameworks use for IT risk

  business_impact_statement: >
    An undetected privileged account compromise on MCP's trading platform could result
    in unauthorized trading activity, client portfolio data exfiltration, regulatory
    sanctions from SEC and FINRA, and reputational damage sufficient to trigger material
    AUM outflows. Estimated annualized loss exposure: $4.81 million (FAIR analysis).
  # => Business impact statement is written for the board, not for IT staff;
  # => "FAIR analysis" is cited to signal the estimate is methodologically grounded

  risk_owner: CIO
  erm_risk_owner: CRO
  # => IT risk owner (CIO) retains accountability for control implementation;
  # => ERM risk owner (CRO) is accountable for enterprise-level reporting and appetite compliance

  inherent_risk_rating:
    likelihood: HIGH
    impact: CRITICAL
    erm_score: 20
    # => ERM score of 20 (on 25-point scale) places this risk in the top quartile;
    # => all risks scoring >=16 are reported to the board risk committee at MCP

  erm_treatment_alignment:
    treatment_option: TREAT
    it_treatment_plan: "IT-RISK-2026-007 treatment plan (PAM deployment, JIT access, recertification)"
    erm_additional_treatment: "Cyber insurance policy review — confirm coverage for insider threat scenario"
    # => ERM treatment adds the cyber insurance dimension that IT risk management alone
    # => would not address; insurance is a transfer mechanism that complements technical controls
    treatment_investment_usd: 185000
    # => The $185K PAM investment is now visible at ERM level; the CRO can evaluate it
    # => against other enterprise risk treatment investments in the same budget cycle
    expected_residual_erm_score: 9
    # => Residual score of 9 (MEDIUM) is within MCP's enterprise risk appetite threshold of <=12

  board_reporting:
    threshold_met: true
    # => Score of 20 exceeds board reporting threshold of >=16
    reporting_vehicle: "Quarterly Board Risk Committee report"
    report_section: "Top 5 Operational Risks"
    last_reported: "Q1 2026 (May Board meeting)"
    next_report_date: "2026-08-01"
    board_communication_summary: >
      Trading platform privileged access risk rated HIGH/CRITICAL. Treatment plan approved:
      $185K PAM deployment underway, expected completion August 2026. Risk will remain on
      board watch list until residual rating confirmed post-implementation.
    # => Board summary is written in three sentences — boards do not read paragraphs of
    # => IT risk detail; the summary must convey rating, treatment, and expected outcome

  escalation_trigger_criteria:
    de_escalation: "Remove from ERM register when residual ERM score sustained <=12 for two consecutive quarters"
    re_escalation: "Re-escalate if PAM implementation delayed >60 days or new control failure identified"
    # => De-escalation criteria prevent ERM registers from accumulating resolved risks;
    # => re-escalation criteria ensure control failures do not go unnoticed at enterprise level
```

**Key Takeaway:** ERM integration adds two dimensions that IT risk management alone misses:
the cyber insurance treatment complement and the board reporting threshold mechanism that
ensures material IT risks receive governance attention proportionate to their enterprise impact.

**Why It Matters:** IT risk registers managed exclusively within IT departments become
invisible to boards and executive leadership. The ERM escalation mechanism at Meridian Capital
Partners ensures that a $4.81 million annualized risk receives board-level visibility and
treatment oversight rather than remaining an IT operational concern. The business impact
statement translation — converting FAIR outputs into language about "unauthorized trading
activity" and "AUM outflows" — is the critical governance communication step that makes
board oversight meaningful rather than ceremonial.

---

## Example 46: Third-Party Governance Program

**What this covers:** A vendor tiering model classifies third-party suppliers by criticality
and risk, then assigns oversight requirements per tier. Tier 1 (critical) vendors receive
comprehensive due diligence, audit rights, and continuous monitoring. Tier 2 (significant)
receives standard due diligence and periodic review. Tier 3 (standard) receives baseline
screening only.

**Scenario:** Meridian Financial Services (MFS), the regional bank, must establish a
third-party governance program to satisfy both NIST CSF 2.0 GV.SC requirements and FFIEC
third-party risk management guidance. The CRO designs the tiering model with the CIO and
Procurement team.

```markdown
# Third-Party Governance Program — Vendor Tiering Table

# Organization: Meridian Financial Services (MFS)

# Owner: CRO (program) + CIO (IT vendor oversight) + Procurement (contract management)

# Effective: Q3 2026

## Vendor Tier Definitions and Oversight Requirements

| Dimension                    | Tier 1 — Critical                                                                 | Tier 2 — Significant                                              | Tier 3 — Standard                                                 |
| ---------------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| Definition                   | Vendor failure causes material service disruption or regulatory breach            | Vendor failure causes significant operational impact              | Vendor failure causes minor inconvenience; no regulatory exposure |
| MFS Examples                 | Core banking platform, payment processor, SWIFT connectivity provider             | HR/payroll system, email platform, backup service                 | Office supplies vendor, cleaning service, low-risk SaaS           |
| Vendor Count (estimated)     | 8                                                                                 | 24                                                                | 150+                                                              |
| Pre-Onboarding Due Diligence | Full: financial health, SOC 2/ISO 27001 report, regulatory standing, pentest      | Standard: SOC 2 or questionnaire, financial viability             | Baseline: registration check, sanctions screening                 |
| Security Questionnaire       | Extended (150 questions, aligned to FFIEC IT Examination Handbook)                | Standard (60 questions, aligned to SIG Lite)                      | Not required                                                      |
| Contract Requirements        | Right-to-audit, incident notification <4 hours, SLA with financial penalties      | Right-to-audit, incident notification <24 hours, SLA              | Standard T&Cs; data handling clause if PII involved               |
| Ongoing Monitoring           | Continuous: real-time financial health monitoring, quarterly security update      | Annual: SOC 2 report review, annual questionnaire refresh         | No ongoing monitoring; re-screen if scope changes                 |
| On-site Audit Rights         | Exercised at least every 2 years; MFS may conduct unannounced inspection          | Exercised at least every 3 years; 30-day notice required          | No audit rights required                                          |
| Subcontractor Requirements   | Must disclose all subcontractors; subcontractors assessed at equivalent tier      | Must notify MFS of material subcontractor changes                 | Not required                                                      |
| Incident Notification SLA    | 4 hours (aligns with DORA major incident reporting for EU-facing services)        | 24 hours                                                          | Best effort; next business day acceptable                         |
| Exit/Concentration Risk      | Business continuity plan for vendor failure required; concentration risk assessed | Exit plan required if vendor is sole provider                     | Not required                                                      |
| Governance Owner             | CIO + CRO (joint oversight); reviewed quarterly by Risk Committee                 | CIO (primary); annual review by CRO                               | Procurement; no executive review required                         |
| Board Reporting              | Top Tier 1 vendors included in board risk report; any Tier 1 incident reported    | Material Tier 2 incidents reported to CIO; escalate if unresolved | No board reporting                                                |

# --- Tiering assignment process ---

# New vendor assessed at pre-onboarding using criticality criteria:

# Q1: Does vendor access, process, or store MFS customer data or funds? → Yes = minimum Tier 2

# Q2: Would vendor failure halt core banking operations for >4 hours? → Yes = minimum Tier 1

# Q3: Is vendor a single-source provider with no readily available alternative? → Yes = +1 tier

# Q4: Does vendor process >$1M of MFS transactions monthly? → Yes = minimum Tier 1

# Annual tier review: all vendors reviewed by CRO; tier may move up (deterioration in risk profile)

# or down (risk reduction, scope change) — tiering is not permanent

# --- DORA alignment note ---

# DORA (Digital Operational Resilience Act, effective January 17, 2025) applies to

# MFS's EU-facing services; Tier 1 vendors supporting EU operations must meet DORA

# ICT third-party risk requirements including contractual provisions per Art. 30

# MFS has 3 Tier 1 vendors in scope for DORA — register maintained separately

# for regulatory reporting purposes
```

**Key Takeaway:** The tiering model's governance value is proportionality — applying Tier 1
oversight rigor to all 180+ vendors would be operationally impossible, while applying Tier 3
baseline to the core banking platform would be a regulatory finding. Tier assignment is the
governance decision that makes the program sustainable.

**Why It Matters:** Third-party risk is consistently cited as a top governance gap in
financial sector examinations. The FFIEC and DORA have each independently concluded that
organizations must apply risk-proportionate oversight rather than uniform vendor management.
MFS's tiering model serves as both a compliance instrument and an operational efficiency
tool: the eight Tier 1 vendors receive intensive oversight because their failure is
existential, while the 150+ Tier 3 vendors receive baseline screening that takes minutes
rather than weeks. The governance owner assignments — joint CIO/CRO for Tier 1, CIO for
Tier 2, Procurement for Tier 3 — reflect the escalating decision authority appropriate to
each tier's risk level.

---

## Example 47: IT Audit Program Development — Risk-Based Audit Plan

**What this covers:** A risk-based annual audit plan prioritizes the audit universe using
a risk scoring methodology, allocates audit resources to the highest-risk areas, and receives
audit committee approval as a governance authorization artifact. The plan ensures internal
audit effort is concentrated where organizational risk is greatest.

**Scenario:** Pinnacle Healthcare Network (PHN) from Example 37 has an internal audit
function covering IT and operational areas. The IT Audit Director develops the annual
risk-based audit plan for presentation to the board audit committee.

```markdown
# IT Internal Audit — Annual Risk-Based Audit Plan

# Organization: Pinnacle Healthcare Network (PHN) | Plan Year: FY2027 (July 2026–June 2027)

# IT Audit Director: [Name] | Audit Committee Approval: Requested June 2026

## Audit Universe and Risk Prioritization

| Audit Area                            | Inherent Risk | Control Maturity | Residual Risk Score | Last Audited | Planned FY2027? | Resource (Days) |
| ------------------------------------- | ------------- | ---------------- | ------------------- | ------------ | --------------- | --------------- |
| Privileged Access Management          | CRITICAL      | LOW              | 20/25               | Never        | YES (Q1)        | 15              |
| EHR System Access Controls            | CRITICAL      | MEDIUM           | 15/25               | FY2025       | YES (Q2)        | 20              |
| Medical Device Cybersecurity          | HIGH          | LOW              | 16/25               | Never        | YES (Q1)        | 12              |
| Cloud Security (AWS GovCloud)         | HIGH          | LOW              | 16/25               | Never        | YES (Q3)        | 18              |
| Ransomware Preparedness / BCP Testing | HIGH          | MEDIUM           | 12/25               | FY2025       | YES (Q2)        | 10              |
| Vendor Risk Management (Tier 1)       | HIGH          | LOW              | 15/25               | FY2024       | YES (Q3)        | 12              |
| HIPAA Security Rule Compliance        | HIGH          | MEDIUM           | 12/25               | FY2025       | YES (Q4)        | 15              |
| Change Management Controls (BAI06)    | MEDIUM        | HIGH             | 6/25                | FY2026       | NO (carry-fwd)  | 0               |
| IT Asset Management / CMDB Accuracy   | MEDIUM        | MEDIUM           | 9/25                | FY2025       | NO (advisory)   | 0               |
| IT Project Governance (PPM)           | MEDIUM        | MEDIUM           | 9/25                | FY2024       | YES (Q4)        | 8               |
| Data Loss Prevention Controls         | MEDIUM        | LOW              | 12/25               | Never        | YES (Q3)        | 10              |
| Network Segmentation (CDE / Clinical) | HIGH          | MEDIUM           | 12/25               | FY2025       | YES (Q2)        | 12              |

# --- Residual risk scoring methodology ---

# Residual Risk Score = Inherent Risk Score × (1 - Control Maturity Factor)

# Inherent Risk Scale: CRITICAL=25, HIGH=20, MEDIUM=12, LOW=5

# Control Maturity Factor: HIGH=0.7, MEDIUM=0.5, LOW=0.2, None=0.0

# Score >=16: Must audit; >=12: Recommended; <12: Advisory/carry-forward

# --- Priority audit rationale ---

# Privileged Access (score 20): Never audited; CRITICAL inherent risk; LOW controls;

# PHN has no PAM solution and no session recording — highest-priority Q1 engagement

# Medical Device Cybersecurity (score 16): Never audited; FDA cybersecurity guidance (2023)

# requires medical device inventory and vulnerability management — regulatory exposure

# Cloud Security (score 16): Cloud adoption approved (Example 37) but audit has never

# evaluated AWS GovCloud controls — migration begins Q1; audit should precede production cutover

# --- Resource allocation ---

# Total planned audit days (IT): 132 days

# Available audit days (IT team: 2 FTE): 180 days

# Buffer for unplanned requests and follow-up: 48 days

# Advisory engagements (non-assurance): 20 days

# --- Audit committee presentation notes ---

# Committee will review and approve the plan; any additions require resource trade-off discussion

# Audit Director retains right to re-prioritize plan if material risk event occurs

# Status updates presented to audit committee quarterly; significant findings reported immediately

# CRITICAL findings (material weakness level) reported within 5 business days of conclusion
```

**Key Takeaway:** The risk-based scoring methodology — multiplying inherent risk by the
inverse of control maturity — ensures that "never audited" high-risk areas surface to the
top of the plan, as PHN's privileged access and medical device cybersecurity engagements
demonstrate.

**Why It Matters:** Internal audit functions with fixed annual plans audit the same areas
year after year, providing assurance on mature controls while emerging risk areas accumulate
without scrutiny. The risk-based model at PHN explicitly surfaces three "never audited"
high-risk areas — including medical device cybersecurity, which FDA guidance now requires
healthcare organizations to manage — and concentrates the majority of audit resources on
residual scores above 12. The audit committee approval step converts the plan from a
management document into a governance authorization, ensuring that audit priorities reflect
board expectations rather than auditor convenience.

---

## Example 48: Control Deficiency Classification

**What this covers:** Control deficiencies identified during internal audit or SOX testing
are classified into three levels: Control Deficiency (CD), Significant Deficiency (SD), and
Material Weakness (MW). Each level carries distinct reporting obligations, remediation urgency,
and escalation paths. Classification is a governance judgment that determines whether findings
reach the board and external auditors.

**Scenario:** Crestview Insurance Group (CIG) is completing its SOX IT general controls
testing. The internal audit team identifies five control deficiencies and must classify each
one using the standard framework before reporting to the audit committee.

```markdown
# Control Deficiency Classification Table — Crestview Insurance Group (CIG)

# Context: SOX IT General Controls Testing | Period: Q1–Q2 2026

# Classifier: IT Audit Director | Review: External Auditors (Deloitte)

## Classification Criteria

| Level                       | Definition                                                                                       | Reporting Obligation                                  | Remediation Urgency               | Example at CIG                                                   |
| --------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------- | --------------------------------- | ---------------------------------------------------------------- |
| Control Deficiency (CD)     | Design or operating weakness that could, in a remote scenario, result in a misstatement          | Management only; not reported to audit committee      | Low — address in next cycle       | Patch management SLA missed for 2 of 200 low-risk servers        |
| Significant Deficiency (SD) | Important weakness that is less severe than MW but deserves audit committee attention            | Audit committee; noted to external auditors           | Medium — remediate within 90 days | Access reviews not completed for 3 application owners in Q1      |
| Material Weakness (MW)      | Reasonable possibility that material misstatement of financial statements would not be prevented | Audit committee + external auditors + SEC (if public) | CRITICAL — immediate remediation  | Emergency changes deployed without any post-hoc CAB ratification |

## Deficiency Inventory — Q1/Q2 2026

| Finding ID  | Control Domain            | Finding Description                                                                                     | Classification | Rationale                                                                                                                                           | Remediation Owner  | Due Date   | Status      |
| ----------- | ------------------------- | ------------------------------------------------------------------------------------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ---------- | ----------- |
| CIG-2026-01 | Change Management (BAI06) | 7 emergency changes in Q1 deployed without post-hoc CAB ratification within 48 hours                    | MW             | Emergency changes without CAB ratification cannot be validated as authorized; creates unrestricted change risk affecting financial system integrity | CIO                | 2026-07-15 | Open        |
| CIG-2026-02 | Access Control            | 3 terminated employees retained active ERP access for 15–45 days post-termination                       | SD             | Terminated employee access creates segregation of duties risk; 3 instances over reporting period is significant but not pervasive                   | IT Operations Lead | 2026-07-31 | In progress |
| CIG-2026-03 | Patch Management          | 2 low-risk servers missed monthly patch cycle (patched in following cycle; no exploits observed)        | CD             | Isolated instances; compensating control (network segmentation) effective; remote probability of material impact                                    | IT Operations Lead | 2026-09-30 | In progress |
| CIG-2026-04 | Privileged Access         | Shared DBA account used for production database administration (no individual accountability)           | SD             | Shared credentials prevent audit trail for privileged actions; significant but not pervasive enough for MW absent evidence of misuse                | CISO               | 2026-08-31 | Open        |
| CIG-2026-05 | Backup and Recovery       | Backup restoration test conducted but restoration time exceeded documented RTO by 280% (8 hrs vs 3 hrs) | SD             | RTO failure represents significant control gap in disaster recovery; not MW absent evidence of financial statement impact                           | IT Operations Lead | 2026-09-30 | Open        |

# --- Classification rationale notes ---

# CIG-2026-01 (MW): Emergency change without CAB ratification is a pervasive design failure

# (7 instances, not 1 or 2); the risk is that unauthorized or untested changes could

# affect financial system data integrity — the direct line to financial statement misstatement

# makes this a Material Weakness regardless of whether misstatement actually occurred

# CIG-2026-02 (SD): Terminated employee access is a segregation of duties risk; 3 instances

# in a quarter are significant but the access was not exercised (validated by access log review);

# if any terminated employee had accessed the system, classification would escalate to MW

# CIG-2026-04 (SD): Shared DBA account is a known IT governance failure mode; classification

# is SD rather than MW because the risk is unauthorized privileged access, not financial

# statement integrity — requires CISO remediation (individual accounts + PAM) before next audit

# --- Reporting obligations for this finding set ---

# External auditor notification: MW (CIG-2026-01) must be communicated within 5 business days

# Audit committee: MW + all SDs reported at next scheduled meeting (June 30)

# Board: Notified of MW by CIO at next board meeting with remediation status

# SEC: CIG is private; no SEC disclosure obligation (public companies would file 8-K)
```

**Key Takeaway:** The Material Weakness classification for CIG-2026-01 (emergency changes
without CAB ratification) is not punitive — it reflects the mathematical reality that
uncontrolled changes to financial systems create a "reasonable possibility" of undetected
financial statement misstatement, which is the legal standard for MW classification.

**Why It Matters:** Control deficiency classification is a governance judgment with legal
and reputational consequences. Misclassifying a Material Weakness as a Significant Deficiency
to avoid board disclosure is a SOX compliance failure that external auditors are trained to
challenge. CIG's seven unratified emergency changes are a systemic process failure — not
seven isolated incidents — and the MW classification creates the escalation pressure needed
to fix the root cause. The classification framework provides objective criteria that remove
the temptation to under-classify findings to minimize management embarrassment.

---

## Example 49: Remediation Tracking — Findings Management

**What this covers:** A findings management register tracks audit findings from identification
through closure, recording finding ID, control domain, severity, root cause, management
response commitment, due date, follow-up testing date, and current status. The register
is the primary instrument for demonstrating to auditors and regulators that identified
weaknesses are being remediated systematically.

**Scenario:** Crestview Insurance Group (CIG) combines findings from its internal IT audit,
SOX testing (Example 48), and a recent QSA review into a unified findings register. The
IT Audit Director presents the register to the audit committee quarterly.

```markdown
# IT Audit Findings Register — Crestview Insurance Group (CIG)

# As of: May 31, 2026 | Owner: IT Audit Director | Reviewed by: Audit Committee

| Finding ID  | Source         | Control Domain       | Severity | Root Cause Summary                                                                                    | Management Response                                                                                                                         | Due Date   | Follow-Up Test Date | Status      |
| ----------- | -------------- | -------------------- | -------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------------- | ----------- |
| CIG-2026-01 | SOX Testing    | Change Management    | MW       | No enforcement mechanism to trigger post-hoc CAB ratification for emergency changes                   | Implement automated ServiceNow workflow: emergency change tickets auto-assign post-hoc CAB task within 4 hours of close; CIO reviews weekly | 2026-07-15 | 2026-08-01          | In Progress |
| CIG-2026-02 | SOX Testing    | Access Control       | SD       | Offboarding process does not include automated ERP access revocation                                  | Integrate HR offboarding workflow with ERP IAM; automated disable on last working day; exception process for contractors                    | 2026-07-31 | 2026-08-15          | In Progress |
| CIG-2026-03 | Internal Audit | Patch Management     | CD       | Two servers excluded from monthly patch group due to misconfiguration in SCCM                         | Correct SCCM group membership; add monthly validation report to patch process checklist                                                     | 2026-09-30 | 2026-10-15          | Open        |
| CIG-2026-04 | SOX Testing    | Privileged Access    | SD       | Shared DBA credentials in use since original platform deployment; individual accounts not provisioned | Provision individual DBA accounts; eliminate shared credential; deploy PAM (CyberArk) for session recording                                 | 2026-08-31 | 2026-09-15          | Open        |
| CIG-2026-05 | Internal Audit | Business Continuity  | SD       | DR runbook not updated since infrastructure refresh; restoration steps reference deprecated tooling   | Update DR runbook; conduct full restoration test against current infrastructure; validate RTO ≤3 hours                                      | 2026-09-30 | 2026-10-30          | Open        |
| CIG-2025-14 | QSA Review     | Network Segmentation | SD       | CDE network segment accessible from general office VLAN via legacy firewall rule                      | Remove legacy firewall rule; implement network access control; re-scope CDE inventory                                                       | 2026-06-30 | 2026-07-15          | OVERDUE     |
| CIG-2025-09 | Internal Audit | Vendor Management    | CD       | Tier 1 vendor risk assessment not refreshed for 26 months                                             | Complete vendor risk reassessment; establish annual refresh calendar                                                                        | 2026-04-30 | 2026-05-15          | CLOSED      |

# --- Register governance rules ---

# OVERDUE items (CIG-2025-14): Audit committee notified when finding is >30 days past due date;

# if >60 days overdue, CIO must present remediation recovery plan at next board meeting

# Follow-up testing is mandatory for all MW and SD findings before the finding can be CLOSED;

# management self-attestation of closure is not accepted — audit must independently verify

# CLOSED status requires: (1) management evidence of remediation submitted, (2) audit follow-up

# test completed with passing result, (3) IT Audit Director sign-off

# Root cause documentation is required — "process failure" is not sufficient;

# root cause must identify: Was it a design deficiency? Operating deficiency? Training gap?

# --- Audit committee dashboard (as of May 31, 2026) ---

# Open MW: 1 (CIG-2026-01) — on track for July 15 due date

# Open SD: 4 (CIG-2026-02, 04, 05, 2025-14)

# OVERDUE SD: 1 (CIG-2025-14) — 31 days overdue; escalation triggered

# Open CD: 1 (CIG-2026-03)

# Closed this quarter: 1 (CIG-2025-09)

# Average finding age (open items): 47 days
```

**Key Takeaway:** The OVERDUE status of CIG-2025-14 (network segmentation) and the
mandatory audit follow-up testing requirement illustrate the two governance principles
that separate effective findings management from a status-tracking spreadsheet: escalation
rules that create accountability and independent verification before closure.

**Why It Matters:** Findings registers without escalation triggers and independent closure
verification enable a common governance failure: findings are marked closed by management
when remediation activities begin, not when they are complete and effective. CIG's register
requires audit follow-up testing before closure — a non-negotiable governance control that
prevents premature closure and provides the auditor and audit committee with evidence-based
assurance. The OVERDUE escalation rule for CIG-2025-14 turns a missed due date from an
administrative note into a board-level governance event that demands management explanation.

---

## Example 50: Continuous Control Monitoring Program

**What this covers:** Continuous control monitoring (CCM) automates evidence collection
for selected controls, reducing reliance on periodic manual testing. A CCM program design
specifies which controls are automated, the data source, monitoring frequency, alert
threshold, evidence storage location, and the exception workflow triggered when a threshold
is breached.

**Scenario:** Apex Data Processing Ltd. is investing in CCM to improve SOC 2 audit
readiness and reduce the manual evidence collection burden on the CISO's team. The CCM
program targets the highest-frequency, highest-evidence-demand controls first.

```yaml
# Continuous Control Monitoring Program Design — Apex Data Processing Ltd.
# Owner: CISO | Tool: Drata (GRC automation platform)
# Objective: Automate evidence collection for 12 SOC 2 controls

ccm_program:
  design_principles:
    - "Automate controls where evidence is machine-readable and source systems have API access"
    - "Preserve manual review for controls requiring judgment (e.g., access appropriateness reviews)"
    # => CCM does not replace all manual controls — controls requiring human judgment
    # => (e.g., "is this access appropriate for this role?") cannot be automated;
    # => CCM targets the evidence collection burden, not the control evaluation judgment

    - "Alert thresholds set to detect control drift before it becomes an audit finding"
    - "Evidence stored in immutable audit log accessible to external auditors via read-only portal"
    # => Immutable storage is critical for SOC 2 Type II — auditors must be confident
    # => that evidence has not been modified after the fact; chain of custody matters

  monitored_controls:
    - control_ref: "CC6.1"
      control_name: "Logical access restricted to authorized users"
      data_source: "Okta Identity Provider (IdP) — API integration"
      monitoring_frequency: "Real-time (event-driven)"
      # => Real-time monitoring for access control events enables detection of unauthorized
      # => access attempts within seconds rather than discovering them in quarterly reviews
      alert_threshold: "Any login from unrecognized device or geography outside defined whitelist"
      evidence_collected: ["Login event log", "MFA challenge log", "Failed login attempts"]
      evidence_storage: "Drata evidence vault (immutable, 3-year retention)"
      exception_workflow:
        trigger: "Alert threshold breached"
        notification: "CISO + SOC analyst within 5 minutes via PagerDuty"
        required_action: "SOC analyst investigates within 15 minutes; escalates to CISO if confirmed anomaly"

    - control_ref: "CC6.2"
      control_name: "New user provisioning requires manager approval"
      data_source: "Okta Workflows — provisioning event log"
      monitoring_frequency: "Daily batch check"
      alert_threshold: "Any user account active without corresponding approval workflow completion record"
      # => Alert fires when a user exists in production without an approval record —
      # => this detects both workflow bypass and system provisioning errors
      evidence_collected: ["Provisioning approval records", "Active user count", "Orphaned account detection"]
      evidence_storage: "Drata evidence vault"
      exception_workflow:
        trigger: "Orphaned account detected"
        notification: "IT Operations Lead within 1 hour"
        required_action: "Account suspended within 4 hours pending investigation"

    - control_ref: "CC7.2"
      control_name: "Vulnerability management: critical vulns patched within SLA"
      data_source: "Tenable.io — vulnerability scanner API"
      monitoring_frequency: "Daily"
      alert_threshold: "Any CVSS 9.0+ vulnerability open >7 days; CVSS 7.0-8.9 open >30 days"
      # => SLA thresholds are tighter than the nominal policy (14/30 days) to provide
      # => buffer — alerts at 7/30 days give the team time to remediate before policy breach
      evidence_collected: ["Vulnerability scan reports", "Remediation ticket linkage", "SLA compliance rate"]
      evidence_storage: "Drata evidence vault + Jira ticket archive"
      exception_workflow:
        trigger: "SLA alert threshold breached"
        notification: "IT Operations Lead + CISO within 2 hours"
        required_action: "Patch expedited or formal risk acceptance documented within 24 hours"

    - control_ref: "CC8.1"
      control_name: "Change management: all production changes via approved process"
      data_source: "ServiceNow — change management module API"
      monitoring_frequency: "Daily"
      alert_threshold: "Any production system change detected in infrastructure monitoring without corresponding approved ServiceNow change record"
      # => Unauthorized change detection requires correlation between infrastructure drift
      # => (detected by cloud security posture tool) and approved change records in ServiceNow;
      # => Drata pulls from both and flags mismatches daily
      evidence_collected: ["Approved change records", "Change success rate metric", "Unauthorized change incidents"]
      evidence_storage: "Drata evidence vault"
      exception_workflow:
        trigger: "Unauthorized change detected"
        notification: "IT Service Manager + CISO immediately"
        required_action: "Change reversed or emergency RFC raised within 2 hours"

    - control_ref: "A1.2"
      control_name: "System availability meets SLA target (99.5% monthly)"
      data_source: "Datadog — uptime monitoring API"
      monitoring_frequency: "Continuous (1-minute check interval)"
      alert_threshold: "Availability drops below 99.5% MTD calculation at any point in the month"
      evidence_collected: ["Uptime percentage (daily, monthly)", "Incident log correlated with downtime events"]
      evidence_storage: "Drata evidence vault + Datadog retention"
      exception_workflow:
        trigger: "MTD availability below 99.5%"
        notification: "IT Operations Lead + CTO within 5 minutes"
        required_action: "Incident response activated; SLA breach report generated within 24 hours"

  program_metrics:
    controls_automated: 12
    controls_manual: 22
    # => 12 of 34 SOC 2 controls automated (35%); manual controls are judgment-dependent
    # => or dependent on systems without API access; CCM expands as integrations mature
    evidence_collection_time_reduction: "~70% reduction in manual evidence collection hours"
    # => CCM target: reduce manual SOC 2 evidence prep from ~400 hours to ~120 hours annually
    audit_portal_access: "External auditors receive read-only Drata portal access for evidence review"
    # => Auditor portal access eliminates the evidence request-and-response cycle that
    # => traditionally consumes 2-3 weeks of audit fieldwork time for SOC 2 engagements
```

**Key Takeaway:** CCM's governance value is not just efficiency — the real-time alert
thresholds and exception workflows mean control failures are detected within hours rather
than discovered during the next quarterly review, fundamentally shifting the organization
from reactive to proactive compliance posture.

**Why It Matters:** Manual evidence collection for SOC 2 Type II is both expensive and
inherently backward-looking: quarterly access reviews find problems three months old.
Continuous control monitoring at Apex Data Processing converts SOC 2 preparation from
a periodic sprint into an always-on compliance posture. The unauthorized change detection
control (CC8.1) demonstrates CCM's most powerful application: correlating infrastructure
drift with change management records in real time, catching unauthorized changes that would
otherwise remain invisible until the annual audit samples happen to find them.

---

## Example 51: Board IT Governance Reporting Dashboard

**What this covers:** A quarterly board IT governance report presents the IT risk heat map,
top risks with trend indicators, KPI RAG status, compliance posture summary, IT investment
portfolio status, and explicit board asks — structured to enable governance decisions rather
than inform passively.

**Scenario:** Meridian Capital Partners (MCP) CIO presents the Q1 2026 board IT governance
report to the board risk committee. The report follows a standardized format agreed at the
prior year's governance framework review.

```markdown
# Board IT Governance Report — Meridian Capital Partners (MCP)

# Quarter: Q1 2026 (January – March 2026) | Presenter: CIO

# Audience: Board Risk Committee | Classification: Board Confidential

## Section 1: IT Risk Heat Map (Q1 2026)

# Risk Heat Map: 5×5 matrix (Likelihood × Impact)

# Quadrant I (High/Critical): ERM-2026-014 (Privileged Access — CRITICAL/HIGH)

# Quadrant II (High/Medium): ERM-2026-018 (Cloud migration readiness — HIGH/MEDIUM)

# Quadrant III (Medium): ERM-2026-021 (Third-party concentration — MEDIUM/HIGH)

# Quadrant IV (Low): ERM-2026-009 (Data retention compliance — LOW/MEDIUM)

# Heat map movement since Q4 2025:

# ERM-2026-014: No movement (treatment in progress; PAM deployment begins June 2026)

# ERM-2026-018: NEW — cloud adoption approved (Example 37); inherent risk now tracked

# ERM-2026-021: Moved from Quadrant III to Quadrant II (payment processor concentration risk elevated)

## Section 2: Top 3 IT Risks with Trend

| Rank | Risk                                 | ERM ID       | Rating        | Trend | Treatment Status                                    | Expected Residual  |
| ---- | ------------------------------------ | ------------ | ------------- | ----- | --------------------------------------------------- | ------------------ |
| 1    | Privileged access — trading platform | ERM-2026-014 | CRITICAL/HIGH | →     | PAM deployment June–August 2026; $185K approved     | MEDIUM by Q3 2026  |
| 2    | Payment processor concentration risk | ERM-2026-021 | HIGH/HIGH     | ↑     | Secondary processor RFP initiated; contract Q4 2026 | HIGH until Q4 2026 |
| 3    | Cloud migration execution risk       | ERM-2026-018 | HIGH/MEDIUM   | NEW   | Cloud Architect role posted; hiring in progress     | MEDIUM by Q1 2027  |

# Trend: → Stable | ↑ Deteriorating | ↓ Improving

# ERM-2026-021 deteriorating: single payment processor processes 94% of card volume;

# regulatory guidance expects <=80% concentration in single provider

## Section 3: IT KPI Dashboard

| KPI                               | Target  | Q1 Actual | RAG   | Trend | Commentary                                                    |
| --------------------------------- | ------- | --------- | ----- | ----- | ------------------------------------------------------------- |
| System availability (trading)     | 99.9%   | 99.95%    | GREEN | →     | No P1 incidents in Q1                                         |
| Change success rate               | >=97%   | 98.2%     | GREEN | ↑     | CAB process fully adopted                                     |
| Patch compliance (critical vulns) | >=95%   | 87%       | AMBER | ↓     | Patch backlog from Q4 2025 carry-over; clearing by May        |
| Security incident count (P1/P2)   | <=2/qtr | 1         | GREEN | →     | One P2 phishing attempt; contained within 2 hours             |
| IT staff retention                | >=85%   | 79%       | AMBER | ↓     | Two senior engineers departed; replacement hiring in progress |
| Audit findings closed on time     | >=90%   | 72%       | AMBER | ↓     | Resource constraint; action plan provided in Section 5        |

## Section 4: Compliance Posture

| Regulation/Framework | Status      | Next Milestone                               | Risk                   |
| -------------------- | ----------- | -------------------------------------------- | ---------------------- |
| SOC 2 Type II        | On track    | Annual audit fieldwork: September 2026       | LOW                    |
| NIST CSF 2.0         | In progress | GV.RM-01 (risk appetite thresholds): Q3 2026 | MEDIUM (3 gaps remain) |
| PCI DSS v4.0         | Compliant   | Annual QSA assessment: November 2026         | LOW                    |
| FAIR quantification  | In progress | Top-5 risks quantified: Q2 2026              | LOW                    |

## Section 5: IT Investment Portfolio Status

| Initiative                          | Budget     | Spent Q1 | Status         | Benefits Realization                              |
| ----------------------------------- | ---------- | -------- | -------------- | ------------------------------------------------- |
| PAM Deployment (CyberArk)           | $185,000   | $12,000  | On track       | Risk reduction: $3.7M ALE; completion August 2026 |
| Cloud Migration (AWS GovCloud)      | $1,800,000 | $0       | Pre-initiation | AUM capacity increase; Cloud Architect TBD        |
| SIEM Rule Tuning (MSSP)             | $95,000    | $45,000  | On track       | Alert-to-triage SLA target: 30 minutes            |
| Staff Training (AWS certifications) | $45,000    | $8,000   | On track       | Cloud readiness; 4 certifications planned Q2-Q3   |

## Section 6: Board Asks

# 1. NOTE: ERM-2026-021 payment processor concentration risk elevated to Quadrant II;

# CIO requests board acknowledgment that secondary processor RFP timeline (Q4 2026) is acceptable

# given regulatory guidance expects concentration remediation within 18 months (deadline: July 2027)

# 2. APPROVE: $45,000 additional audit resource budget to address audit finding closure rate

# (current: 72% vs. 90% target); two-quarter engagement to clear backlog

# 3. NOTE: Cloud Architect hiring in progress; CIO will provide update at Q2 board meeting;

# cloud migration mandate remains conditional on hire (per board conditional approval, Example 37)
```

**Key Takeaway:** The board report's "Section 6: Board Asks" converts the dashboard from
a passive information briefing into an active governance instrument — boards that receive
IT reports without explicit asks frequently lack the context to know when a decision or
acknowledgment is required from them.

**Why It Matters:** Board IT governance reporting fails most often at the final step: boards
receive dashboards full of RAG status and risk ratings but are not told what they need to
decide or acknowledge. The three explicit board asks in MCP's report — a timeline acknowledgment,
a budget approval, and a status note — convert the board's oversight role from passive
reception to active governance participation. The payment processor concentration risk
ask is particularly important: without it, the board could not know that the deteriorating
trend has a regulatory deadline implication that warrants their attention beyond the amber
RAG indicator.

---

## Example 52: IT Investment Portfolio Governance

**What this covers:** IT investment portfolio governance applies stage-gate reviews to
active initiatives, evaluating strategic alignment, benefits realization progress, and
go/no-go criteria at defined checkpoints. The governance authority approves continuation,
resets scope, or terminates initiatives based on evidence rather than sunk-cost reasoning.

**Scenario:** Meridian Capital Partners (MCP) CIO presents the Q2 2026 portfolio stage-gate
review to the IT Investment Committee. Three active initiatives are reviewed against their
original business cases and current performance data.

```markdown
# IT Investment Portfolio Stage-Gate Review — Meridian Capital Partners (MCP)

# Period: Q2 2026 Stage-Gate Review | Governance Authority: IT Investment Committee

# Members: CEO, CFO, CIO, CRO | Facilitator: CIO

## Active Initiative Review

### Initiative 1: PAM Deployment (CyberArk)

| Dimension              | At Approval (Q1 2026)             | Q2 2026 Actual                                          |
| ---------------------- | --------------------------------- | ------------------------------------------------------- |
| Strategic Alignment    | Risk reduction — IT-RISK-2026-007 | Unchanged — still aligned                               |
| Total Budget           | $185,000                          | $185,000 (no change request)                            |
| Spend to Date          | $12,000 (Q1)                      | $97,000 (Q1+Q2 combined)                                |
| Schedule Status        | Completion: August 2026           | On track — all 23 accounts onboarded by June 15         |
| Benefits Realization   | ALE reduction: $3.7M projected    | Session recording active; shared credentials eliminated |
| Issues                 | None at approval                  | Minor: JIT access config delayed 3 weeks (resolved)     |
| Go/No-Go Criteria Met? | N/A (pre-initiation)              | YES — all Q2 gate criteria satisfied                    |

# Gate decision: CONTINUE — no remediation required; Q3 gate will confirm residual risk reduction

# => Gate criteria for PAM Deployment Q2: (1) All accounts onboarded; (2) session recording active;

# => (3) no budget variance >10%; all three met — continuation is unambiguous

### Initiative 2: Cloud Migration (AWS GovCloud)

| Dimension              | At Conditional Approval (Q1 2026)                                    | Q2 2026 Actual                                                                                   |
| ---------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Strategic Alignment    | Infrastructure modernization (5-year strategy)                       | Unchanged                                                                                        |
| Total Budget           | $1,800,000                                                           | $1,800,000 (no change request)                                                                   |
| Spend to Date          | $0 (pre-initiation)                                                  | $85,000 (Cloud Architect hiring + design work)                                                   |
| Schedule Status        | Migration begins Q3 2026                                             | AT RISK — Cloud Architect hired June 1; onboarding complete July 15; migration start slips to Q4 |
| Conditions from Board  | 3 conditions: Cloud Architect hire, perf. baselines, training budget | Cloud Architect: DONE; Perf. baselines: IN PROGRESS; Training: DONE                              |
| Go/No-Go Criteria Met? | Conditional approval (board Q1)                                      | PARTIAL — performance baselines not yet complete for 4 of 12 applications                        |

# Gate decision: CONDITIONAL CONTINUE — migration planning may proceed; production cutover

# requires all 12 application performance baselines complete; CIO to report at Q3 board meeting

# => Conditional continue prevents the initiative from stalling entirely due to a partial gap

# => while maintaining the governance control that all baselines must exist before production cutover;

# => this is the stage-gate mechanism working as designed — not a rubber stamp

### Initiative 3: SIEM Rule Tuning (MSSP Engagement)

| Dimension                   | At Approval (Q4 2025)                 | Q2 2026 Actual                                |
| --------------------------- | ------------------------------------- | --------------------------------------------- |
| Strategic Alignment         | Detect function improvement (CSF 2.0) | Unchanged                                     |
| Total Budget                | $95,000                               | $95,000                                       |
| Spend to Date               | $45,000                               | $82,000                                       |
| Schedule Status             | Completion: June 2026                 | COMPLETE — project delivered on time          |
| Benefits Realization Target | Alert-to-triage SLA: <=30 minutes     | Achieved: average 22 minutes (Q2 measurement) |
| Issues                      | None                                  | None                                          |
| Go/No-Go Criteria Met?      | N/A (complete)                        | Project closure approved                      |

# Gate decision: CLOSE — benefits realized; final payment authorized; lessons learned documented

# => Benefits realization confirmation (22-minute average vs. 30-minute target) is documented

# => before project closure; without confirmed realization, the investment rationale is unverified

# => and the portfolio record is incomplete for future benchmarking

## Portfolio Governance Principles Applied

# 1. Sunk-cost discipline: gate decisions based on future value, not past spend

# => If Cloud Migration had shown no path to value, the correct gate decision is TERMINATE

# => regardless of the $85K already spent; the Q2 decision is CONDITIONAL CONTINUE on merit

# 2. Benefits realization before closure: no project closed without measured outcome confirmation

# => SIEM initiative formally closed only after 22-minute SLA measurement validated

# 3. Condition tracking: board conditions from conditional approvals are tracked at every gate

# => Cloud Migration Q2 gate explicitly checks all three board conditions from Q1 approval

# 4. Governance authority: IT Investment Committee — not CIO alone — makes gate decisions

# => CIO presents evidence; committee decides; this separation prevents confirmation bias
```

**Key Takeaway:** The stage-gate model's governance discipline shows at the Cloud Migration
initiative: a conditional continue rather than full go prevents premature production cutover
while avoiding stalled bureaucracy — the gate works because it is tied to specific, measurable
conditions rather than subjective readiness assessments.

**Why It Matters:** IT investment portfolio governance without stage-gate discipline produces
the two most common project failure modes: projects that continue despite evidence of failure
(sunk-cost escalation) and projects that are closed before benefits are confirmed (premature
closure). The MCP Investment Committee's role — reviewing evidence and making gate decisions
rather than receiving CIO progress reports — is the governance structure that maintains
objectivity. The SIEM engagement's formal closure with documented benefits realization
creates the portfolio record that justifies future MSSP investments using actual performance
data rather than vendor proposals.

---

## Example 53: Data Governance Program Basics

**What this covers:** A data stewardship model assigns accountability for data quality,
access, and lifecycle management across data domains by defining data owners (business
accountability), data stewards (operational management), and data custodians (technical
custody). The model links domain-level accountability to a data governance committee with
policy authority.

**Scenario:** Pinnacle Healthcare Network (PHN) is establishing a formal data governance
program to address HIPAA data integrity obligations and support its cloud migration.
The Chief Data Officer (CDO) designs the stewardship model for the five primary data domains.

```markdown
# Data Governance Stewardship Model — Pinnacle Healthcare Network (PHN)

# Owner: Chief Data Officer (CDO) | Governance Body: Data Governance Committee

# Effective: Q3 2026

## Data Stewardship Assignments

| Data Domain            | Data Owner                    | Data Steward                 | Data Custodian            | Key Responsibilities                                                                                                                                        | Governance Committee Linkage                               |
| ---------------------- | ----------------------------- | ---------------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Patient Clinical Data  | Chief Medical Officer (CMO)   | Clinical Informatics Manager | EHR System Administrator  | Owner: approve access policy, define retention; Steward: data quality rules, issue resolution; Custodian: backup, encryption, access control implementation | Reports data quality metrics monthly to Data Gov Committee |
| Patient Financial Data | CFO                           | Revenue Cycle Manager        | Finance Systems DBA       | Owner: approve data sharing with insurers; Steward: billing accuracy rules; Custodian: database security controls                                           | Escalates data breach events to Data Gov Committee         |
| Employee HR Data       | HR Director                   | HR Systems Analyst           | HR Systems Administrator  | Owner: define retention per labor law; Steward: data completeness for payroll; Custodian: IAM for HR system                                                 | Annual data inventory review presented to Committee        |
| Operational/Supply     | Chief Operating Officer (COO) | Supply Chain Analyst         | ERP Administrator         | Owner: approve vendor data sharing; Steward: inventory data accuracy; Custodian: ERP access control                                                         | No standing committee reporting; escalation as needed      |
| Research Data          | Chief Research Officer (CRO)  | Research Data Manager        | Research IT Administrator | Owner: IRB compliance, consent management; Steward: data quality for publications; Custodian: data lake security                                            | IRB approval status reported quarterly to Committee        |

## Role Definitions

# DATA OWNER — Senior business executive accountable for the data domain

# => Owner decisions include: who may access, how long retained, who may share externally;

# => ownership cannot be delegated to IT — data is a business asset, not a technology asset

# DATA STEWARD — Operational manager responsible for data quality and policy compliance

# => Steward is the day-to-day accountable role: they resolve data quality issues,

# => maintain data dictionaries, and ensure business rules are applied consistently

# DATA CUSTODIAN — Technical role responsible for data storage, security, and availability

# => Custodian implements controls defined by the owner and steward; they do not define policy;

# => separation of custodian from owner/steward prevents technical teams from self-governing data

## Data Governance Committee

# Membership: CDO (chair), all Data Owners, CIO, CISO, Legal/Privacy Officer

# Meeting cadence: Monthly (standing); ad hoc for breach events or policy changes

# Authority:

# - Approve enterprise data policies (retention, classification, access)

# - Resolve cross-domain data conflicts (e.g., research access to patient clinical data)

# - Approve data sharing agreements with external parties

# - Receive data quality metrics and direct remediation

# => Committee authority over cross-domain conflicts is the governance mechanism that

# => prevents individual data owners from making unilateral decisions affecting other domains;

# => patient clinical data shared with research without CMO+CRO+CDO alignment is a HIPAA risk

## HIPAA Alignment

# Minimum Necessary Standard (45 CFR 164.514(d)):

# => Data stewards are responsible for applying minimum necessary standard to access requests;

# => "all clinical data" is not an acceptable access request — stewards define the minimum

# => data elements needed for each use case and document the determination

# Data Use Agreements (DUAs):

# => Research domain: all external research data sharing requires DUA approved by CDO and Legal;

# => DUA inventory maintained by Research Data Manager and reported to Committee quarterly

# Breach Notification:

# => Any custodian detecting a potential PHI breach notifies CISO + CDO within 1 hour;

# => CDO activates breach response; committee convened within 24 hours if PHI confirmed
```

**Key Takeaway:** The separation of data owner (business accountability), data steward
(operational management), and data custodian (technical implementation) prevents the most
common data governance failure: IT departments making data policy decisions that should
belong to business executives who understand data's business and regulatory context.

**Why It Matters:** Healthcare data governance is a HIPAA compliance obligation and a
patient safety issue. Pinnacle Healthcare Network's stewardship model makes the Chief Medical
Officer accountable for patient clinical data policy — not the EHR administrator — because
clinical data decisions have clinical implications that IT staff are not positioned to evaluate.
The Data Governance Committee's authority to resolve cross-domain conflicts is the mechanism
that prevents the research team from independently accessing patient data without CMO oversight,
which is precisely the type of unauthorized secondary use that triggers HIPAA enforcement actions.

---

## Example 54: Architecture Governance Review

**What this covers:** An Architecture Review Board (ARB) intake form structures the
evaluation of proposed IT solutions against architectural standards, assesses risk,
and produces a formal ARB decision (approve, conditionally approve, or reject) with
documented rationale. The ARB is the governance control that prevents architectural
debt accumulation from unreviewed technology decisions.

**Scenario:** Pinnacle Healthcare Network (PHN) is proposing to deploy a new AI-assisted
clinical decision support tool. The solution architect submits an ARB intake form before
the vendor contract is signed, ensuring governance review occurs before commitment.

```markdown
# Architecture Review Board (ARB) Intake Form — Pinnacle Healthcare Network (PHN)

# Submission Date: May 15, 2026 | ARB Meeting: June 3, 2026

# Solution Architect: [Name] | ARB Chair: CTO

## Section 1: Solution Description

Project Name: AI Clinical Decision Support (AI-CDS) Tool
Vendor: NeuralPath Health Inc. (SaaS)
Description: AI-powered differential diagnosis support tool integrated with PHN's EHR system;
provides clinicians with evidence-based treatment suggestions at point of care.
Business Sponsor: Chief Medical Officer (CMO)
Estimated Contract Value: $420,000/year (3-year term)
Go-Live Target: Q1 2027

## Section 2: Architectural Standards Compliance

| Standard                             | Compliant? | Assessment Notes                                                                                        |
| ------------------------------------ | ---------- | ------------------------------------------------------------------------------------------------------- |
| API integration standard (REST/FHIR) | YES        | NeuralPath uses FHIR R4 API — aligns with PHN's EHR integration standard                                |
| Data residency (US-only for PHI)     | YES        | NeuralPath hosts on AWS us-east-1 and us-west-2 only; BAA executed                                      |
| SSO/SAML integration with Okta       | PARTIAL    | SAML integration available but requires custom configuration; estimated 40 hours additional setup       |
| Data encryption at rest (AES-256)    | YES        | Confirmed in vendor security questionnaire; SOC 2 Type II report reviewed                               |
| Availability SLA >=99.5%             | YES        | Vendor SLA: 99.9%; PHN requires 99.5% minimum for clinical tools                                        |
| Architecture review before contract  | YES        | This intake submitted before contract signing — governance process followed correctly                   |
| AI/ML model governance policy        | NO         | PHN does not yet have an AI governance policy; this deployment would be the first AI tool in production |
| Third-party risk assessment (Tier 1) | PARTIAL    | Initial assessment complete; on-site audit rights not yet negotiated in vendor contract                 |

# => AI/ML governance policy gap is the most significant architectural non-compliance:

# => deploying an AI clinical decision support tool without an AI governance framework

# => creates unmanaged risk around model bias, explainability, and clinical liability

# => ARB cannot approve deployment into a governance vacuum — the AI policy gap must be

# => addressed before or concurrent with deployment; this is a condition, not a rejection

## Section 3: Risk Assessment

| Risk                                      | Likelihood | Impact   | Mitigation                                                                            |
| ----------------------------------------- | ---------- | -------- | ------------------------------------------------------------------------------------- |
| AI model bias affecting clinical outcomes | MEDIUM     | CRITICAL | Require vendor to provide bias audit results; PHN clinicians validate recommendations |
| PHI exposure via AI training data         | LOW        | CRITICAL | Contractual prohibition on using PHN patient data for model training; audit annually  |
| EHR integration failure at go-live        | MEDIUM     | HIGH     | Phased rollout (2 pilot departments before full deployment); rollback plan required   |
| Clinician over-reliance on AI             | HIGH       | HIGH     | Training program mandatory; tool positioned as "support" not "decision-maker"         |
| Vendor lock-in (3-year term)              | HIGH       | MEDIUM   | Data export capability confirmed; contract includes data portability clause           |

# => Clinician over-reliance risk is rated HIGH likelihood — evidence from clinical AI

# => implementations shows automation bias is common; governance must address through

# => mandatory training and clear tool positioning in clinical workflows

## Section 4: ARB Decision

Decision: CONDITIONAL APPROVE
Date: June 3, 2026

Conditions:

1. PHN AI Governance Policy must be drafted, reviewed by CMO and CISO, and approved by
   Data Governance Committee before go-live (target: Q3 2026)

   # => AI governance policy is a prerequisite, not a parallel workstream — no production

   # => deployment of AI tools in clinical settings without a governance framework

2. Vendor contract must include: on-site audit rights (annual), prohibition on PHN data
   use in model training, model change notification >=30 days before deployment, and
   bias audit results shared annually with PHN CMO

3. Pilot deployment limited to 2 departments (Cardiology, Internal Medicine) with
   30-day observation period before full rollout; pilot metrics reported to ARB

4. SSO/SAML integration must be complete and tested before pilot go-live (not deferred
   to post-pilot)

Rationale: The solution is technically sound and strategically aligned. Conditional approval
preserves momentum while ensuring PHN's governance maturity keeps pace with the technology.

ARB Chair: CTO | Business Sponsor: CMO | Security Sign-off: CISO
```

**Key Takeaway:** The ARB's conditional approval for the AI-CDS tool demonstrates
the governance body's most important function: enabling innovation while requiring
the governance structures (AI policy, vendor contract terms, phased rollout) to
exist before production commitment rather than after a problem emerges.

**Why It Matters:** Architecture governance reviews conducted after contract signing are
retrospective compliance exercises with no practical authority to change the decision.
PHN's ARB review before contract signature gives the board real leverage: the AI governance
policy condition and vendor contract requirements become contractual obligations rather than
aspirational post-implementation improvements. The clinician over-reliance risk — rated HIGH
likelihood — is the kind of organizational and behavioral risk that technical architecture
reviews miss but ARB governance frameworks are designed to surface.

---

## Example 55: Business Continuity Governance

**What this covers:** Business continuity governance defines the BC policy, the BC steering
committee structure, the BC coordinator role, annual testing obligations, and the board
reporting requirement for BC posture. Governance ensures that BC is an organizational
discipline with accountability at the executive level, not a technology backup plan owned
by IT operations.

**Scenario:** Pinnacle Healthcare Network (PHN) formalizes its BC governance structure
following an incident where a ransomware attack at a peer hospital network caused patient
diversion for 11 days. The CEO commissions a governance-first BC program review.

```yaml
# Business Continuity Governance Structure — Pinnacle Healthcare Network (PHN)
# Owner: Chief Operating Officer (COO) | Program Sponsor: CEO
# Effective: Q3 2026

bc_governance:
  bc_policy:
    title: "Business Continuity and Disaster Recovery Policy"
    policy_owner: COO
    # => COO owns BC policy, not CIO — clinical operations continuity is a business obligation,
    # => not a technology obligation; CIO owns the DR technical components as a subordinate plan
    approved_by: CEO
    approval_date: "2026-07-01"
    review_cycle: "Annual (before Q3 board meeting)"
    policy_scope: "All PHN clinical operations, administrative functions, and supporting IT systems"
    policy_objectives:
      - "Ensure patient care continuity during any disruptive event"
      - "Define RTO and RPO for all critical systems and clinical processes"
      - "Establish crisis communication protocols for patients, staff, and regulators"
      - "Comply with CMS Conditions of Participation (42 CFR 482.41) emergency preparedness"
    # => CMS Conditions of Participation require hospitals to have emergency preparedness programs;
    # => BC policy is a regulatory compliance obligation for PHN, not a discretionary governance choice

  bc_steering_committee:
    purpose: "Executive oversight of BC program strategy, investment, and annual testing"
    chair: CEO
    # => CEO chairs the BC steering committee — this signals organizational priority and ensures
    # => resource allocation decisions are made at the level of authority required to execute them
    members:
      - COO
      - CFO
      - CMO
      - CIO
      - CISO
      - Chief Nursing Officer (CNO)
      - Legal Counsel
      - Head of Facilities
    # => Clinical leadership (CMO, CNO) membership is essential — BC for a hospital is primarily
    # => a patient care continuity program; technical recovery without clinical planning fails
    meeting_cadence: "Quarterly (standing); within 48 hours of any declared disaster"
    authority:
      - "Approve BC plan updates and scenario assumptions"
      - "Authorize BC testing schedules and resource allocation"
      - "Declare internal disaster and activate BC plan"
      - "Approve communications to patients, media, and regulators during crisis"

  bc_coordinator:
    title: "Business Continuity Coordinator"
    reports_to: COO
    role_description: >
      Day-to-day program manager for BC: maintains BC plans, coordinates department-level
      BIA updates, schedules and facilitates annual tests, manages BC documentation library,
      and serves as liaison between BC steering committee and department BC leads.
    # => BC Coordinator is not a senior executive — it is a dedicated program management role;
    # => the governance is provided by the steering committee; the coordinator provides continuity
    # => of institutional knowledge and administrative discipline
    qualifications: "CBCP (Certified Business Continuity Professional) or equivalent; minimum 3 years BC experience"
    department_bc_leads:
      - "Each department with critical operations designates a BC Lead responsible for departmental BIA and plan maintenance"
      # => Department BC Leads distribute the program's operational burden across the organization
      # => and ensure departmental expertise is embedded in the BC plans, not only in central IT

  annual_testing_obligations:
    tabletop_exercise:
      frequency: "Annual (minimum)"
      scope: "Full scenario covering top 3 risk scenarios (ransomware, pandemic, facilities failure)"
      participants: "BC Steering Committee + all Department BC Leads"
      facilitator: "BC Coordinator + external BC specialist (every other year)"
      output: "After-Action Report with findings and improvement actions"
      # => After-Action Report is a governance deliverable — it is not filed and forgotten;
      # => steering committee reviews and approves improvement actions at next quarterly meeting
    functional_exercise:
      frequency: "Annual"
      scope: "IT disaster recovery — full failover test of top 3 critical clinical systems"
      participants: "IT Operations, CISO, CMO representative"
      success_criteria: "RTO and RPO targets achieved for all in-scope systems"
      output: "DR Test Report; RTO/RPO actuals vs. targets; remediation plan for gaps"
    communication_drill:
      frequency: "Semi-annual"
      scope: "Crisis communication — test notification cascade to all staff within 30 minutes"
      output: "Drill report with timing results and gap identification"

  board_reporting:
    cadence: "Annual BC posture report to board of directors; event-driven for any declared disaster"
    board_report_content:
      - "BC program maturity assessment (current year vs. prior year)"
      - "Annual test results: tabletop findings summary, DR test RTO/RPO actuals"
      - "Top 3 BC risks with treatment status"
      - "Regulatory compliance status (CMS, Joint Commission)"
      - "Investment requirements for program gaps"
    # => Board BC report is separate from the IT risk report — BC is a board fiduciary obligation
    # => for a healthcare organization; the board must understand whether PHN can care for patients
    # => during a disruption, not just whether IT systems will recover within RTO
    reporting_owner: COO
    board_ask_format: "Specific approvals requested; no passive information dumps"
```

**Key Takeaway:** PHN's BC governance structure places the CEO as steering committee chair
and the COO as policy owner — not the CIO — because business continuity for a hospital is
a patient care and regulatory obligation that must be owned at the operational executive level,
with IT disaster recovery as a supporting component rather than the primary program.

**Why It Matters:** Healthcare organizations that treat business continuity as an IT backup
and recovery function discover their error when a ransomware attack forces patient diversion:
IT restores systems, but clinical workflows, paper-based fallback procedures, staff communications,
and regulatory notifications all fail because no one owned them. PHN's governance structure —
CEO-chaired steering committee, COO-owned policy, department BC leads — distributes continuity
ownership across the organization. The CMS regulatory obligation makes board reporting on BC
posture a compliance requirement, not a governance aspiration.

---

## Example 56: Regulatory Compliance Calendar

**What this covers:** A regulatory compliance calendar tracks annual obligations (report
filings, audit submissions, license renewals, training attestations) across all applicable
regulations and jurisdictions. Each obligation has a named owner, next due date, and current
status — making compliance management proactive rather than reactive.

**Scenario:** Apex Data Processing Ltd. operates across the UK, EU, and US, creating a
multi-regulatory compliance environment. The Compliance Officer maintains a unified
obligations calendar reported to the audit committee quarterly.

```markdown
# Regulatory Compliance Calendar — Apex Data Processing Ltd.

# Owner: Compliance Officer | Reviewed: Audit Committee (quarterly)

# Jurisdictions: UK, EU (GDPR), US (state privacy laws), global (ISO 27001)

| Regulation / Framework   | Jurisdiction   | Obligation                                                | Frequency   | Owner              | Next Due Date | Status      |
| ------------------------ | -------------- | --------------------------------------------------------- | ----------- | ------------------ | ------------- | ----------- |
| GDPR (EU) 2016/679       | EU             | Annual ROPA review and update                             | Annual      | DPO + Legal        | 2026-12-31    | On track    |
| GDPR (EU) 2016/679       | EU             | Data Processing Agreement review (all Tier 1 processors)  | Annual      | Legal              | 2026-09-30    | On track    |
| GDPR (EU) 2016/679       | EU             | Privacy notice review and publication                     | Annual      | Legal + Marketing  | 2026-11-30    | On track    |
| UK GDPR / DPA 2018       | UK             | ICO registration renewal                                  | Annual      | DPO                | 2027-02-28    | On track    |
| UK GDPR / DPA 2018       | UK             | Subject Access Request response SLA (30 days per request) | Per request | Legal              | Ongoing       | Compliant   |
| ISO 27001:2022           | Global (cert.) | Surveillance audit (external auditor)                     | Annual      | CISO               | 2026-09-15    | On track    |
| ISO 27001:2022           | Global (cert.) | Internal audit (ISMS)                                     | Annual      | IT Audit Lead      | 2026-07-31    | On track    |
| ISO 27001:2022           | Global (cert.) | Management review meeting                                 | Annual      | CISO + CEO         | 2026-10-31    | Scheduled   |
| SOC 2 Type II            | US (customers) | Annual SOC 2 audit (CPA firm)                             | Annual      | CISO               | 2026-09-30    | On track    |
| PCI DSS v4.0             | Global (cards) | Self-Assessment Questionnaire (SAQ-D) submission          | Annual      | CTO + CISO         | 2026-11-30    | Not started |
| PCI DSS v4.0             | Global (cards) | Quarterly network vulnerability scan (ASV)                | Quarterly   | IT Operations Lead | 2026-06-30    | Compliant   |
| CCPA (California)        | US (CA)        | Privacy policy update for California residents            | Annual      | Legal              | 2026-12-31    | On track    |
| CCPA (California)        | US (CA)        | Do Not Sell/Share opt-out mechanism review                | Annual      | Legal + Product    | 2026-12-31    | On track    |
| UK Cyber Essentials      | UK             | Cyber Essentials Plus certification renewal               | Annual      | CISO               | 2026-08-31    | In progress |
| Employment law (UK)      | UK             | Right to Work checks audit (Home Office compliance)       | Annual      | HR Director        | 2026-10-31    | Scheduled   |
| Information Commissioner | UK             | Annual data protection fee payment                        | Annual      | Finance + DPO      | 2027-02-01    | On track    |

# --- Calendar governance rules ---

# "Not started" status with due date >90 days: AMBER flag; owner must present start plan

# "Not started" status with due date <90 days: RED flag; immediate escalation to Compliance Officer

# PCI DSS SAQ-D (not started, due Nov 30): at 6 months out, AMBER — start plan required by July 1

# Ownership rule: every obligation has exactly one primary owner (not "IT" or "Legal" generically);

# named individual accountability prevents obligation slippage during personnel transitions

# New regulation tracking: Compliance Officer reviews regulatory horizon quarterly;

# EU AI Act obligations (effective August 2026) to be added in Q3 calendar update

# Breach notification obligations (not in calendar — event-driven):

# GDPR: 72 hours to supervisory authority (ICO for UK data subjects)

# PCI DSS: Card brand notification within 24 hours of suspected breach

# These are activated by CISO via incident response plan, not managed through calendar cadence
```

**Key Takeaway:** The calendar's governance discipline is in the "Not started" escalation
rules — a PCI DSS SAQ-D that is six months out and not started is an AMBER flag requiring
a start plan, not a green status, because SAQ-D preparation typically requires eight to
twelve weeks of evidence gathering.

**Why It Matters:** Regulatory compliance failures in multi-jurisdictional organizations
almost always trace to obligations that existed in policy but were not tracked operationally.
Apex Data Processing's compliance calendar converts abstract regulatory requirements into
named-owner, dated obligations with status tracking and escalation thresholds. The EU AI
Act addition in Q3 — acknowledging that the regulatory landscape evolves — reflects the
governance principle that compliance calendars must be living documents, not static annual
artifacts. The separation of event-driven obligations (breach notification) from calendar
obligations prevents the calendar from becoming unwieldy while ensuring event-driven
obligations are addressed through the correct operational mechanism.

---

## Example 57: GRC Tool Selection Criteria

**What this covers:** A GRC tool selection scorecard evaluates vendor platforms across
eight governance-relevant dimensions using weighted scores. The structured evaluation
produces a defensible selection decision that the audit committee can review, replacing
informal vendor preference with documented criteria-based governance.

**Scenario:** Meridian Financial Services (MFS) is selecting a GRC platform to replace
its current spreadsheet-based risk register and audit tracking system. The CRO leads
the evaluation with the CIO, Compliance Officer, and IT Audit Director as evaluation team
members.

```markdown
# GRC Tool Selection Scorecard — Meridian Financial Services (MFS)

# Evaluation Team: CRO (lead), CIO, Compliance Officer, IT Audit Director

# Vendors Evaluated: Archer (RSA), ServiceNow GRC, LogicGate, Vanta

# Scoring: 1 (Poor) → 5 (Excellent) | Weight reflects MFS governance priorities

## Evaluation Scorecard

| Dimension                | Weight | Archer (RSA) | ServiceNow GRC | LogicGate | Vanta | Weight Rationale                                                                                 |
| ------------------------ | ------ | ------------ | -------------- | --------- | ----- | ------------------------------------------------------------------------------------------------ |
| Risk Management          | 25%    | 5            | 4              | 4         | 3     | Core capability — risk register, appetite tracking, FAIR integration; highest weight             |
| Control Library          | 15%    | 5            | 4              | 3         | 4     | Pre-built frameworks (NIST CSF, ISO 27001, PCI DSS) reduce implementation time                   |
| Audit Management         | 20%    | 4            | 5              | 3         | 2     | Finding tracking, evidence collection, audit committee reporting are critical for MFS            |
| Reporting and Dashboards | 15%    | 4            | 5              | 4         | 4     | Board-quality reporting is non-negotiable; MFS needs quarterly board dashboards out-of-box       |
| Integration Capabilities | 10%    | 3            | 5              | 3         | 4     | ServiceNow integration ecosystem advantages; MFS already uses ServiceNow ITSM                    |
| Vendor Support           | 5%     | 3            | 4              | 4         | 4     | Support quality verified via reference calls; weight low relative to capability dimensions       |
| Total Cost of Ownership  | 5%     | 2            | 3              | 5         | 4     | 3-year TCO including license, implementation, training; lower weight reflects strategic priority |
| Scalability              | 5%     | 5            | 5              | 3         | 3     | MFS expects 2x growth in regulatory obligations over 5 years; platform must scale                |

## Weighted Score Calculation

| Vendor         | Risk Mgmt (25%) | Control Lib (15%) | Audit Mgmt (20%) | Reporting (15%) | Integration (10%) | Support (5%) | TCO (5%) | Scalability (5%) | Weighted Total |
| -------------- | --------------- | ----------------- | ---------------- | --------------- | ----------------- | ------------ | -------- | ---------------- | -------------- |
| Archer (RSA)   | 1.25            | 0.75              | 0.80             | 0.60            | 0.30              | 0.15         | 0.10     | 0.25             | 4.20           |
| ServiceNow GRC | 1.00            | 0.60              | 1.00             | 0.75            | 0.50              | 0.20         | 0.15     | 0.25             | 4.45           |
| LogicGate      | 1.00            | 0.45              | 0.60             | 0.60            | 0.30              | 0.20         | 0.25     | 0.15             | 3.55           |
| Vanta          | 0.75            | 0.60              | 0.40             | 0.60            | 0.40              | 0.20         | 0.20     | 0.15             | 3.30           |

# => ServiceNow GRC scores highest (4.45) driven by audit management (5/5) and integration (5/5);

# => MFS's existing ServiceNow ITSM deployment makes integration weight more impactful in practice

# => than the 10% formal weight suggests — change management effort for a second platform would add

# => unscored implementation risk

# => Archer scores second (4.20) with best-in-class risk management and scalability;

# => Archer's lower integration score reflects its standalone nature — meaningful for MFS given

# => existing ServiceNow environment

# --- Governance considerations beyond the scorecard ---

# Reference calls conducted: 3 references per vendor; all Tier 1 financial services customers

# => Reference call findings: ServiceNow GRC implementation typically 6-9 months for financial sector;

# => Archer implementation: 9-12 months; both require dedicated project manager

# Vendor financial health: All four vendors assessed; Archer acquired by RSA (private equity);

# confirm roadmap commitment before contracting

# => Private equity ownership introduces concentration risk on product roadmap and pricing;

# => MFS contract should include data portability clause and migration support obligation

# Recommended decision: ServiceNow GRC

# Rationale: Highest weighted score; integration with existing ServiceNow ITSM eliminates

# dual-platform complexity; audit management capability (highest-weight gap area) is strongest;

# financial sector references confirm implementation feasibility

# Decision authority: CRO presents recommendation to Audit Committee for approval;

# Audit Committee approval required for technology contracts >$250K (per MFS procurement policy)

# => Audit committee approval ensures the GRC tool selection is a governance decision,

# => not a unilateral CRO procurement action — the committee that uses GRC audit outputs

# => should have visibility into the tool selection that produces those outputs
```

**Key Takeaway:** ServiceNow GRC's selection over the higher-scoring Archer risk management
module reflects the governance principle that integration context matters: MFS's existing
ServiceNow ITSM investment makes a unified platform superior to a higher-scoring standalone
tool whose integration costs and change management burden are not captured in the formal scorecard.

**Why It Matters:** GRC tool selection decisions made without structured criteria produce
vendor selections based on sales relationships, demo quality, or price alone — none of which
correlate reliably with governance program outcomes. The MFS scorecard creates a documented,
criteria-based decision record that the audit committee can review and that future program
managers can reference to understand the trade-offs accepted at selection. The private equity
ownership note on Archer and the data portability contract clause reflect the governance
principle that GRC tool lock-in is itself a risk: organizations that cannot migrate away
from a GRC tool without losing historical risk and audit data are operationally dependent
on their vendor's continued investment in the product.
