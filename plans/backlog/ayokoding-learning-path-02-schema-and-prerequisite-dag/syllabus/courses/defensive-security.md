# Defensive Security (By Example, Python + shell)

**Course ID**: `defensive-security` · **Format**: By Example · **Language**: Python + shell.

**Short summary**: Detection, monitoring, incident response (concept)

**Scope note**: detecting, responding to, and recovering from the attacks the red-team topic produced —
logging/monitoring, detection engineering (Sigma rules, MITRE ATT&CK mapping), the incident-response
lifecycle, and hardening. `†`: Python + shell driving a log/SIEM stack (ELK/OpenSearch) against
lab-generated data. The direct counterpart to [`59-offensive-security`](./offensive-security.md);
applies [`58-it-and-application-security`](./it-and-application-security.md). This topic **closes Pass 3** and anchors **three
inter-topic capstones** (Pass-3 boundary + two cross-cutting), specified at the end of this file.

## Why this exists · the big idea

- **The problem before the solution**: attacks that succeed unseen are total losses — without detection and
  a rehearsed response, a breach is found months later by someone else, and every red-team finding without a
  matching detection is a blind spot.
- **Keep-this-if-you-forget-everything**: assume you will be attacked and instrument for it — centralize
  telemetry, write detections mapped to known techniques, and rehearse the incident-response loop, tuning
  the false-positive/false-negative balance that keeps the signal usable.
- **Big ideas touched**: `layering-and-leaks` (detection spans every layer the attacker crosses),
  `correctness-vs-pragmatism` (detection engineering is a false-positive/false-negative trade-off, never
  perfect).

## Prerequisites

- **Prior topics**: [topic 59 Offensive Security](./offensive-security.md) (the attacks to detect),
  [topic 58 IT / Application Security](./it-and-application-security.md) (threats, OWASP, crypto), and
  [topic 5 Just Enough Bash](./just-enough-bash.md) (log wrangling).
- **Tools & environment**: a macOS/Linux terminal; the **same isolated local lab** from topic 59
  (attacks generate the telemetry); a local log/SIEM stack (ELK/OpenSearch or an equivalent) + Python for
  detection logic; sample attack logs. Self-owned lab only.
- **Assumed knowledge**: the attack lifecycle + how a web attack looks on the wire (topic 59); the OWASP
  Top 10 + threat modeling (topic 58); shell + log filtering (topic 05).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified (CORRECTION, recent): **MITRE ATT&CK v19 (2026-04-28)** restructured the Enterprise
  matrix — the "Defense Evasion" tactic **split into "Stealth" (keeps TA0005) + new "Defense Impairment"
  (TA0112)**; Enterprise now has **15 tactics** (was 14). Do NOT name "Defense Evasion" as a current tactic —
  reference Stealth/Defense Impairment or teach generically. (attack.mitre.org/tactics/TA0112)
- 2026-07-12 — verified (CORRECTION): the classic 6-phase IR lifecycle (prep → detect/analyze → contain →
  eradicate → recover → lessons-learned) is SANS **PICERL** / NIST SP 800-61 **Rev. 2 (2012)** framing —
  NIST **superseded it with SP 800-61 Rev. 3 (April 2025)**, which drops the standalone lifecycle and maps
  IR onto CSF 2.0 functions (Govern/Identify/Protect/Detect/Respond/Recover). Either teach the classic model
  cited as SANS/industry-standard, or teach the current CSF-2.0-mapped Rev. 3 — do not attribute the 6-phase
  model to "current NIST." (csrc.nist.gov/pubs/sp/800/61/r3/final)
- 2026-07-12 — verified: Sigma rule format current (SigmaHQ YAML, `pySigma` → 40+ query langs). ELK/OpenSearch
  (DD-21 flag): **OpenSearch is cleanly Apache-2.0** (OpenSearch Software Foundation) and satisfies DD-21;
  Elasticsearch's default distribution ships under **Elastic License 2.0 (not OSI-approved)** despite the
  AGPLv3 option added 2024 — default to OpenSearch, or be explicit about the AGPLv3 self-managed Elastic
  build. (sigmahq.io / elastic.co/pricing/faq/licensing / opensearch.org)

### DD-35 primary-source citations (fetched-and-read)

> Every framework name, phase count, tenet, and standard below traces to a primary source the author fetched
> and READ. Unverifiable specifics carry `[Needs Verification]`.

- **NIST SP 800-61 — Rev. 2 WITHDRAWN 2025-04-03** `[Verified/Outdated]` — the withdrawal notice bundled into
  [SP 800-61 Rev. 2 (PDF)](https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-61r2.pdf) reads
  verbatim: "NIST SP 800-61 Rev. 2 is withdrawn and superseded in its entirety by NIST SP 800-61r3." Rev. 2's
  four phases (fetched from its ToC §3): **Preparation → Detection and Analysis → Containment, Eradication,
  and Recovery → Post-Incident Activity**. [Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) re-maps IR
  onto the CSF 2.0 Functions (its internal structure `[Needs Verification]` — PDF text extraction failed).
  Teach the classic model as SANS/industry-canonical and disclose the 2025 withdrawal.
- **NIST CSF 2.0 — six Functions (verbatim)** `[Verified]` — [NIST CSWP 29 (PDF)](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf)
  §2 (2024-02-26): **GOVERN** ("cybersecurity risk management strategy, expectations, and policy are
  established, communicated, and monitored"), **IDENTIFY** ("current cybersecurity risks are understood"),
  **PROTECT** ("Safeguards to manage… risks are used"), **DETECT** ("Possible cybersecurity attacks and
  compromises are found and analyzed"), **RESPOND** ("Actions regarding a detected… incident are taken"),
  **RECOVER** ("Assets and operations affected… are restored"). GOVERN sits at the center and informs the
  other five.
- **MITRE ATT&CK — 15 Enterprise tactics (v19)** `[Verified]` — [attack.mitre.org tactics](https://attack.mitre.org/tactics/enterprise/):
  the former **Defense Evasion (TA0005)** split into **Stealth (TA0005)** + **Defense Impairment (TA0112)** →
  15 tactics. "a globally-accessible knowledge base of adversary tactics and techniques based on real-world
  observations." Tactic = why (goal); technique = how. v19 released 2026-04-28 `[Needs Verification]` (exact
  date search-only; the 15-tactic list is direct-fetch `[Verified]`).
- **Zero Trust — 7 tenets (verbatim)** `[Verified]` — [NIST SP 800-207 (PDF)](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf)
  §2.1: (1) "All data sources and computing services are considered resources." (2) "All communication is
  secured regardless of network location." (3) "Access… granted on a per-session basis." (4) "Access…
  determined by dynamic policy." (5) monitors asset integrity/posture. (6) "All resource authentication and
  authorization are dynamic and strictly enforced before access is allowed." (7) collects state to improve
  posture. PDP/PEP model confirmed (Fig. 1).
- **Sigma spec 2.1.0** `[Verified]` — [sigmahq.io spec](https://sigmahq.io/sigma-specification/specification/sigma-rules-specification.html)
  (v2.1.0, 2025-08-02): required fields `title`, `logsource` (category/product/service), `detection`
  (search-identifiers + mandatory `condition`); UTF-8 / LF / 4-space / lowercase keys.
- **YARA rules** `[Verified]` — [yara.readthedocs.io](https://yara.readthedocs.io/en/stable/writingrules.html):
  minimal `rule name { condition: false }`; a rule has `strings:` ($text/$hex) + `condition:`.
- **IOC (verbatim)** `[Verified]` — [NIST CSRC glossary](https://csrc.nist.gov/glossary/term/indicator_of_compromise):
  "Technical artifacts or observables that suggest that an attack is imminent or is currently underway or that
  a compromise may have already occurred" (sources SP 800-61r3, SP 800-150).
- **CIS Benchmarks** `[Verified]` — [cisecurity.org/cis-benchmarks](https://www.cisecurity.org/cis-benchmarks):
  "prescriptive configuration recommendations for more than 25+ vendor product families… consensus-based
  effort of cybersecurity experts globally."
- **Honeypot (verbatim)** `[Verified]` — [NIST CSRC glossary](https://csrc.nist.gov/glossary/term/honeypot)
  (citing CNSSI 4009 → IETF RFC 4949): "A system… or system resource… designed to be attractive to potential
  crackers and intruders, like honey is attractive to bears."
- **EDR** `[Verified]` — [CrowdStrike EDR 101](https://www.crowdstrike.com/en-us/cybersecurity-101/endpoint-security/endpoint-detection-and-response-edr/):
  "an endpoint security solution that continuously monitors end-user devices to detect and respond to cyber
  threats"; cites Gartner (Chuvakin) EDR definition. IDS/IPS structure from
  [Suricata rules docs](https://docs.suricata.io/en/latest/rules/intro.html) (action + header + rule options).
- **Zero-standard concepts (`[Needs Verification]`)** — SOC-tier (1/2/3) nomenclature, Pyramid of Pain
  (Bianco's original [detect-respond.blogspot.com](http://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html)
  not directly fetched), alert-fatigue, and SOAR (Gartner page returned HTTP 403) rest on industry-consensus /
  search-summarized sources, not a fetched primary. Teach conceptually; flag verbatim quotes until confirmed.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. All work is lab-local. -->

- **co-01 · blue-vs-red-vs-purple** — blue defends, red attacks, purple closes the loop between them (NISTIR 7622 team roles).
- **co-02 · logging-what-to-log** — which events must be logged (auth, access, high-value transactions) to make attacks visible.
- **co-03 · centralized-logging** — shipping logs to one aggregation point so telemetry is searchable together (NIST SP 800-92).
- **co-04 · siem** — a SIEM collects, correlates, and alerts on security telemetry.
- **co-05 · siem-dashboard** — visualizing telemetry so an analyst can see an attack.
- **co-06 · log-parsing** — parsing and normalizing heterogeneous raw logs to a common schema.
- **co-07 · detection-engineering** — writing detections as a maintained, tested discipline (detections-as-code).
- **co-08 · sigma-rules** — Sigma is a portable, SIEM-agnostic detection format (SigmaHQ spec).
- **co-09 · sigma-logsource-detection-condition** — a Sigma rule's structure: logsource + detection + a mandatory condition.
- **co-10 · mitre-attack-mapping** — mapping each detection to a MITRE ATT&CK tactic/technique.
- **co-11 · attack-tactic-vs-technique** — ATT&CK separates tactics (the why) from techniques (the how); Enterprise has 15 tactics (v19).
- **co-12 · false-positive-negative-tuning** — detection is a continuous false-positive/false-negative tuning trade-off.
- **co-13 · ids-ips** — signature- vs anomaly-based intrusion detection/prevention (Suricata/Snort).
- **co-14 · edr-xdr** — endpoint detection & response, extended (XDR) across more data sources.
- **co-15 · ir-lifecycle** — the incident-response lifecycle (NIST SP 800-61 Rev. 2's four phases; disclose the 2025 Rev. 3 CSF-mapping).
- **co-16 · ir-preparation** — preparing to handle incidents (playbooks, tooling, readiness).
- **co-17 · ir-detection-analysis** — detecting and analyzing an incident from telemetry (precursors vs indicators).
- **co-18 · ir-containment-eradication-recovery** — containing spread, eradicating the foothold, recovering to normal operations.
- **co-19 · ir-post-incident** — the post-incident lessons-learned that feed back into defense.
- **co-20 · threat-hunting** — hypothesis-driven searching through telemetry for undetected activity.
- **co-21 · ioc** — indicators of compromise: technical artifacts that suggest an attack (NIST glossary).
- **co-22 · threat-intelligence** — IOCs, TTPs, and feeds that inform detection (NIST SP 800-150).
- **co-23 · pyramid-of-pain** — Bianco's Pyramid of Pain: hashes cost the attacker least, TTPs cost most.
- **co-24 · yara-rules** — YARA rules match malware by strings + a condition.
- **co-25 · malware-analysis-static-dynamic** — static (no execution) vs dynamic (sandboxed execution) malware analysis.
- **co-26 · zero-trust** — never trust, always verify: the seven NIST SP 800-207 tenets (per-session, dynamic policy).
- **co-27 · network-defense** — firewalls and segmentation to limit blast radius.
- **co-28 · hardening-cis-benchmarks** — hardening systems against CIS Benchmarks; attack-surface reduction.
- **co-29 · vuln-patch-management** — the vulnerability/patch-management lifecycle, prioritized by risk (NIST SP 800-40r4).
- **co-30 · honeypot-deception** — decoys that lure and log intruders (RFC 4949 / NIST).
- **co-31 · csf-functions** — NIST CSF 2.0's six Functions: Govern, Identify, Protect, Detect, Respond, Recover.
- **co-32 · purple-team-loop** — every red-team finding should produce a matching blue-team detection.
- **co-33 · alert-fatigue** — too much noise buries real alerts; tuning keeps the signal usable.
- **co-34 · soar** — security orchestration, automation, and response: automating enrichment and response.

## Worked examples

Colocated under `defensive-security/learning/`; Python + shell over lab-generated telemetry (DD-20/DD-30).
Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · blue-red-purple-roles** — annotate blue vs red vs purple team roles — verify the defend-vs-attack distinction. (co-01)
- **ex-02 · what-to-log** — annotate which events must be logged (auth, access, high-value) — verify auditable events listed. (co-02)
- **ex-03 · log-format-parse** — parse a raw log line in Python — verify extracted fields. (co-06)
- **ex-04 · centralized-logging** — annotate shipping logs to a central store — verify one aggregation point. (co-03)
- **ex-05 · siem-concept** — annotate a SIEM's collect→correlate→alert flow — verify the three stages. (co-04)
- **ex-06 · siem-ingest** — ingest lab logs into the SIEM (ELK/OpenSearch) — verify events queryable. (co-04)
- **ex-07 · siem-dashboard** — build a dashboard surfacing the recon scan — verify the scan is visible. (co-05)
- **ex-08 · log-normalize** — normalize heterogeneous logs to a schema — verify a common field set. (co-06)
- **ex-09 · ids-signature** — annotate a signature-based IDS rule (Suricata) — verify the pattern match. (co-13)
- **ex-10 · ids-anomaly** — annotate anomaly-based detection vs signature — verify the difference. (co-13)
- **ex-11 · suricata-rule-structure** — annotate a Suricata rule (action/header/options) — verify the three parts. (co-13)
- **ex-12 · edr-concept** — annotate what EDR monitors on endpoints — verify continuous endpoint telemetry. (co-14)
- **ex-13 · xdr-extend** — annotate XDR extending beyond endpoints — verify the extra data sources. (co-14)
- **ex-14 · detection-engineering-intro** — annotate detection engineering as a discipline — verify detections-as-code. (co-07)
- **ex-15 · sigma-rule-first** — write a first Sigma rule for a failed-login burst — verify it matches the log. (co-08)
- **ex-16 · sigma-structure** — annotate a Sigma rule's logsource + detection + condition — verify each field. (co-09)
- **ex-17 · sigma-portable** — annotate Sigma → multiple SIEM query languages (pySigma) — verify portability. (co-08)
- **ex-18 · attack-tactic-technique** — annotate an ATT&CK tactic vs technique — verify the why-vs-how. (co-11)
- **ex-19 · attack-15-tactics** — annotate the 15 Enterprise tactics (v19) — verify Stealth + Defense Impairment present. (co-11)
- **ex-20 · attack-map-detection** — map a detection to an ATT&CK technique ID — verify the technique ID. (co-10)
- **ex-21 · ioc-types** — annotate IOC types (hash/IP/domain) — verify the artifact examples. (co-21)
- **ex-22 · ioc-match** — match an IOC against the lab logs in Python — verify a hit. (co-21)
- **ex-23 · threat-intel-feed** — annotate consuming a threat-intel feed — verify IOCs ingested. (co-22)
- **ex-24 · ttp-vs-ioc** — annotate TTPs vs atomic IOCs — verify the durability difference. (co-22)
- **ex-25 · csf-functions** — annotate the CSF 2.0 six Functions — verify all six named. (co-31)
- **ex-26 · csf-govern-center** — annotate why GOVERN sits at the center — verify it informs the others. (co-31)

### Intermediate

- **ex-27 · sigma-sqli** — write a Sigma detection for the SQL-injection attempt — verify it fires on the attack log. (co-08)
- **ex-28 · sigma-no-false-positive** — verify the SQLi rule stays quiet on benign traffic — verify low false positives. (co-12)
- **ex-29 · fp-fn-tradeoff** — annotate the false-positive/false-negative tuning trade-off — verify the tuning knob. (co-12)
- **ex-30 · tune-threshold** — tune a detection threshold to cut false positives — verify the reduced noise. (co-12)
- **ex-31 · sigma-xss** — write a Sigma detection for the XSS attempt — verify it fires + maps to a technique. (co-08, co-10)
- **ex-32 · sigma-bruteforce** — write a Sigma detection for the brute-force login — verify a threshold match. (co-08)
- **ex-33 · pyramid-of-pain** — annotate Bianco's Pyramid of Pain tiers — verify the six levels ordered. (co-23)
- **ex-34 · pyramid-ttp-hardest** — annotate why TTPs cost the attacker most — verify the top-of-pyramid reasoning. (co-23)
- **ex-35 · threat-hunt-hypothesis** — form a threat-hunt hypothesis — verify a testable statement. (co-20)
- **ex-36 · threat-hunt-query** — run a hypothesis-driven query over telemetry — verify it surfaces the activity. (co-20)
- **ex-37 · threat-hunt-pivot** — pivot from one IOC to related activity — verify the expanded scope. (co-20)
- **ex-38 · yara-rule-first** — write a YARA rule for a lab sample — verify it matches. (co-24)
- **ex-39 · yara-strings-condition** — annotate a YARA rule's strings + condition — verify the match logic. (co-24)
- **ex-40 · malware-static** — annotate static analysis (no execution) of a lab sample — verify the extracted strings/hashes. (co-25)
- **ex-41 · malware-dynamic** — annotate dynamic analysis (sandboxed execution) — verify the observed behavior. (co-25)
- **ex-42 · ir-lifecycle-phases** — annotate the classic IR lifecycle phases — verify the phase sequence + Rev. 3 note. (co-15)
- **ex-43 · ir-preparation** — annotate IR preparation (playbooks, tooling) — verify the readiness artifacts. (co-16)
- **ex-44 · ir-detection-analysis** — detect + analyze an incident from the lab telemetry — verify the incident scoped. (co-17)
- **ex-45 · ir-triage** — triage precursors vs indicators — verify the classification. (co-17)
- **ex-46 · ir-containment** — annotate a containment strategy — verify the spread is stopped. (co-18)
- **ex-47 · ir-eradication** — annotate eradication of the attacker foothold — verify the artifact removed. (co-18)
- **ex-48 · ir-recovery** — annotate recovery to normal operations — verify service restored. (co-18)
- **ex-49 · ir-evidence-handling** — annotate evidence gathering + chain of custody — verify integrity preserved. (co-18)
- **ex-50 · ir-post-incident** — write a lessons-learned post-incident report — verify improvements captured. (co-19)
- **ex-51 · zero-trust-tenets** — annotate the NIST 800-207 zero-trust tenets — verify per-session dynamic access. (co-26)
- **ex-52 · zero-trust-pdp-pep** — annotate the PDP/PEP model — verify the decision-vs-enforcement split. (co-26)
- **ex-53 · network-segmentation** — annotate network segmentation limiting blast radius — verify the contained zone. (co-27)
- **ex-54 · firewall-rule** — annotate a deny-by-default firewall rule — verify the allowed exceptions. (co-27)

### Advanced

- **ex-55 · cis-benchmark** — annotate applying a CIS Benchmark to harden the lab host — verify a control applied. (co-28)
- **ex-56 · attack-surface-reduction** — annotate reducing attack surface (disable unused services) — verify the closed surface. (co-28)
- **ex-57 · vuln-scan** — run a vulnerability scan of the lab host — verify findings enumerated. (co-29)
- **ex-58 · patch-management-lifecycle** — annotate the vuln/patch-management lifecycle — verify the phases. (co-29)
- **ex-59 · patch-prioritize** — prioritize patches by CVSS + exploitability — verify high-risk first. (co-29)
- **ex-60 · honeypot-deploy** — annotate deploying a honeypot in the lab — verify it lures + logs. (co-30)
- **ex-61 · honeypot-alert** — alert on any honeypot interaction — verify a high-fidelity signal. (co-30)
- **ex-62 · soar-playbook** — annotate a SOAR automated-response playbook — verify the automated action. (co-34)
- **ex-63 · soar-enrich** — annotate automated alert enrichment — verify the added context. (co-34)
- **ex-64 · alert-fatigue** — annotate alert fatigue as a breach cause — verify the noise problem. (co-33)
- **ex-65 · alert-tuning** — tune noisy alerts to reduce fatigue — verify the signal-to-noise gain. (co-33)
- **ex-66 · purple-team-loop** — annotate the red-finding→blue-detection loop — verify each attack has a detection. (co-32)
- **ex-67 · purple-coverage-gap** — find a red-team attack with no detection — verify the coverage gap surfaced. (co-32)
- **ex-68 · detection-coverage-matrix** — build an ATT&CK coverage matrix of detections — verify covered vs gaps. (co-10, co-32)
- **ex-69 · ids-deploy-lab** — deploy Suricata against lab traffic — verify it alerts on the scan. (co-13)
- **ex-70 · correlation-rule** — write a SIEM correlation rule across two log sources — verify the joined signal. (co-04)
- **ex-71 · dashboard-attack-timeline** — build an attack-timeline dashboard — verify the ordered kill-chain view. (co-05)
- **ex-72 · detection-as-code-ci** — annotate detections-as-code tested in CI — verify the rule test gate. (co-07)
- **ex-73 · sigma-to-siem-query** — convert a Sigma rule to the SIEM's query language — verify the translated query runs. (co-08)
- **ex-74 · ioc-sweep** — sweep all lab hosts for an IOC — verify affected hosts identified. (co-21)
- **ex-75 · hunt-to-detection** — promote a successful threat hunt into a standing detection — verify the new rule. (co-20, co-07)
- **ex-76 · ir-tabletop** — run an IR tabletop over one attack end to end — verify each phase executed. (co-15)
- **ex-77 · recovery-backup-restore** — annotate a backup/restore recovery step — verify the clean restore. (co-18)
- **ex-78 · blue-team-capstone** — full blue pipeline: ingest + detections + hunt + IR report — verify each part present + purple loop closed. (co-04, co-08, co-10, co-15, co-32)

## Tensions & trade-offs — when NOT to reach for this

- **False positives vs false negatives**: a detection tuned too tight misses the attack; tuned too loose it
  buries the SOC in noise until real alerts are ignored (alert fatigue is itself a breach cause). Detection
  engineering is continuous tuning of that balance, never a finished ruleset.
- **Detection vs prevention**: you can't detect your way out of a preventable hole — but you also can't
  prevent everything, so over-investing in either extreme fails. The mix depends on what is cheap to prevent
  versus what must be caught in flight.
- **When NOT to build it big**: not every environment needs a full SIEM + 24/7 SOC. A small shop may get more
  safety from patching and least privilege than from a detection pipeline it can't staff. Right-size
  detection to what you can actually triage.

## Lineage — why it beat the alternative

- Blue-team practice matured from ad-hoc log-grepping into detection engineering as attacks industrialized.
  MITRE ATT&CK (2013+) gave a shared language of adversary techniques so detections could map to real
  behavior instead of guesswork; Sigma made detections portable across SIEMs; the SANS/NIST IR lifecycles
  codified how to respond under pressure (NIST SP 800-61 Rev. 3, 2025, re-maps it onto CSF 2.0). The
  purple-team loop closes it: every offense from [`59-offensive-security`](./offensive-security.md) should
  produce a detection here. The invariant — assume breach, instrument, rehearse — is the defensive face of
  the same threat-driven thinking as [`58-it-and-application-security`](./it-and-application-security.md).

## Capstone materials

Colocated under `defensive-security/learning/`; Python + shell over lab-generated telemetry (DD-20/DD-30).

- **beginner** — ingest the lab's attack logs into the SIEM; build a dashboard that surfaces the recon scan
  from topic 59.
- **intermediate** — write a Sigma detection for the SQL-injection attempt + map it to a MITRE ATT&CK
  technique; verify it fires on the attack log and not on benign traffic.
- **advanced** — run a full incident-response tabletop over one attack: detect → contain → eradicate →
  recover → write the post-incident report.

## Capstone spec — intra-topic (subject → full runnable, lab-local)

- **Goal**: stand up a blue-team pipeline over the telemetry the topic-39 red-team capstone generated —
  centralized logging + a SIEM, detection rules (Sigma) for each exploited attack mapped to MITRE ATT&CK,
  a dashboard, and a full incident-response run (detect → contain → eradicate → recover → lessons-learned)
  producing a post-incident report — closing the purple-team loop.
- **Concepts exercised**: [ ] centralized logging + a SIEM dashboard (co-03, co-04, co-05) [ ] a Sigma
  detection per attack (co-08) [ ] MITRE ATT&CK technique mapping (co-10, co-11) [ ] a threat-hunt query
  (co-20) [ ] the IR lifecycle end to end (co-15, co-18) [ ] a post-incident report with lessons-learned
  (co-19, co-32).
- **Ordered steps**:
  1. `.../learning/capstone/ingest/` — pipe the topic-39 attack logs into the SIEM + a dashboard. Verify the
     recon scan and the exploits are visible in the dashboard.
  2. `.../learning/capstone/detections/` — a Sigma rule per exploited vuln, each mapped to a MITRE ATT&CK
     technique. Verify each rule fires on its attack and stays quiet on benign traffic (low false positives).
  3. `.../learning/capstone/hunt.md` — a hypothesis-driven threat-hunt query over the telemetry. Verify it
     surfaces the attacker activity from the raw logs.
  4. `.../learning/capstone/ir-report.md` — an IR run (detect → contain → eradicate → recover) +
     lessons-learned mapped back to the red-team findings. Verify every topic-39 finding has a matching
     detection + remediation (purple-team loop closed).
- **Acceptance criteria**: attacks are visible in the SIEM; each exploited vuln has a firing, low-false-
  positive Sigma detection mapped to ATT&CK; the threat hunt finds the activity; the IR report closes every
  red-team finding with a detection + remediation.
- **Done bar**: runnable end-to-end against the local lab telemetry + web-verified.

---

## Capstone spec — inter-topic: capstone-real-world-delivery (Pass-3 boundary)

**Weight**: `learning/_index.md` and the drilling mirror place this capstone at **705** (Pass-3 boundary,
after topic 60; ahead of Pass 4). Kind: **subject → full runnable** (DD-27). This is the Pass-3 graduation
project — the "Build for the Real World" pass made real.

- **Goal**: take the Pass-2 `capstone-solid-core` application and deliver it the way a real team ships:
  choose and justify a data layer beyond a single SQL DB (NoSQL/graph where it fits — topics 34/35),
  scale the backend (39) with an event-driven slice (45) modeled with DDD (43) under a documented
  architecture (42) and a system-design capacity plan (44), containerize + orchestrate it (50), describe
  its infrastructure as code (51), add a CI/CD pipeline that builds, tests, and deploys it (55), and secure it end to end (58) with red-team validation (59) and
  blue-team detection (60) — a complete, deployed-as-code, secured, observable system.
- **Integrates topics**: 34 NoSQL · 35 Graph (where it fits) · 39 Backend at Scale · 42 Architecture ·
  43 DDD · 44 System Design · 45 Event-Driven · 50 Containers/K8s · 51 Cloud/IaC · 55 CI/CD · 58 IT Security ·
  59 Offensive (validation) · 60 Defensive (detection). (37/53 optional where the domain benefits.)
- **Concepts exercised**: [ ] a justified polyglot-persistence choice [ ] a scaled, event-driven backend
  slice [ ] a DDD-modeled domain under a documented (C4) architecture [ ] a system-design capacity plan
  [ ] containerized + orchestrated deployment [ ] infrastructure described as code [ ] a CI/CD pipeline (build → test → deploy) [ ] a security
  assessment + red-team validation + blue-team detections.
- **Ordered steps**:
  1. `.../capstone-real-world-delivery/design/` — architecture (C4) + a system-design capacity/trade-off
     plan + the persistence-choice rationale. Verify the diagrams match the intended build and the capacity
     numbers are arithmetic-checked.
  2. `.../capstone-real-world-delivery/app/` — the DDD-modeled, scaled backend with an event-driven slice +
     the chosen data layer(s). Verify the domain invariants hold, the event slice is reliable (no lost/
     double messages), and the data-layer choice is exercised.
  3. `.../capstone-real-world-delivery/deploy/` — Dockerfile(s) + K8s manifests + Terraform/OpenTofu (local
     provider) + a CI/CD pipeline (55) that builds, tests, and deploys on push. Verify the app deploys to the local cluster via the IaC + pipeline and self-heals.
  4. `.../capstone-real-world-delivery/security/` — a threat model + red-team validation (lab-local) + a
     blue-team detection set. Verify each identified threat has a mitigation and a firing detection.
- **Acceptance criteria**: the system runs deployed-as-code on a local cluster; the domain + event slice are
  correct; capacity/architecture are documented and matched by the build; the security loop (model →
  red-team → blue-team) is closed. All work stays within self-owned labs.
- **Done bar**: runnable end-to-end (deployed via IaC to the local cluster) + security loop closed +
  web-verified.

## Capstone spec — inter-topic: capstone-secure-service (cross-cutting)

**Weight**: `learning/_index.md` and the drilling mirror place this capstone at **706** (cross-cutting,
just after `capstone-real-world-delivery`). Kind: **subject → full runnable** (DD-27). A focused
security-thread capstone that can be pursued independently of the full Pass-3 project.

- **Goal**: build (or take a prior) HTTP service and make it demonstrably secure end to end — apply the
  OWASP Top 10 (2025) mitigations, do proper identity (OAuth2/OIDC + JWT done right), harden it, then
  **prove** the security by attacking it from the red-team lab (59) and **detecting** those attacks from
  the blue-team stack (60) — a single service where the full security lifecycle is visible.
- **Integrates topics**: 17 Security Essentials · 39 Backend (auth surface) · 58 IT Security (OWASP/crypto/
  identity) · 59 Offensive (validation) · 60 Defensive (detection). (50 for a hardened container image
  where used.)
- **Concepts exercised**: [ ] OWASP Top 10 (2025) mitigations applied [ ] OAuth2/OIDC + JWT done right
  [ ] hardening (headers, least privilege, secrets in env) [ ] red-team validation of the mitigations
  [ ] blue-team detections for the attempted attacks [ ] a before/after security posture writeup.
- **Ordered steps**:
  1. `.../capstone-secure-service/app/` — the service with OWASP-2025 mitigations + OAuth2/OIDC + JWT
     integrity + hardening. Verify each Top-10 category is addressed and auth gates behave correctly.
  2. `.../capstone-secure-service/attack/` — lab-local red-team attempts against the service. Verify the
     mitigations hold (attacks that succeeded pre-hardening now fail) — authorized self-owned target only.
  3. `.../capstone-secure-service/detect/` — blue-team detections (Sigma + ATT&CK mapping) for the attempted
     attacks. Verify each attempt raises a detection with low false positives.
  4. `.../capstone-secure-service/posture.md` — a before/after security-posture writeup. Verify each fixed
     weakness is tied to its mitigation, its failed attack, and its detection.
- **Acceptance criteria**: the OWASP-2025 mitigations demonstrably hold under lab-local attack; identity is
  correct; every attempted attack is detected; the posture writeup ties mitigation → validation → detection.
- **Done bar**: runnable end-to-end + attacks demonstrably mitigated + detected (lab-local) + web-verified.

## Capstone spec — inter-topic: capstone-data-pipeline (cross-cutting)

**Weight**: `learning/_index.md` and the drilling mirror place this capstone at **707** (cross-cutting,
just after `capstone-secure-service`). Kind: **subject → full runnable** (DD-27). A focused data-thread
capstone, independently pursuable.

- **Goal**: build an end-to-end data path — ingest raw data through a medallion pipeline (bronze/silver/
  gold) with data-quality gates (37), model it with advanced SQL for serving (26), optionally serve a
  read-optimized store (34/35 where the access pattern fits), and expose it through an AI-powered,
  RAG-grounded query interface (56) over a backend (39) — a complete "raw data → governed warehouse →
  intelligent interface" slice.
- **Integrates topics**: 10 SQL · 26 Advanced SQL · 34 NoSQL / 35 Graph (where the serving pattern fits) ·
  39 Backend at Scale (serving) · 37 Data Engineering (the pipeline) · 56 AI-Powered Apps (the interface).
- **Concepts exercised**: [ ] a medallion ETL/ELT pipeline (bronze→silver→gold) [ ] data-quality gates
  [ ] a star schema + advanced-SQL serving queries [ ] a fit-for-purpose serving store [ ] a RAG-grounded
  query interface [ ] served over a backend endpoint.
- **Ordered steps**:
  1. `.../capstone-data-pipeline/pipeline/` — raw → bronze → silver → gold with quality gates (37). Verify
     idempotent re-runs, a bad batch caught by the gate, and a reconciling star schema.
  2. `.../capstone-data-pipeline/serve/` — advanced-SQL serving queries (26) + optionally a read-optimized
     store (34/35). Verify serving queries match hand-computed expected results.
  3. `.../capstone-data-pipeline/interface/` — a RAG-grounded (56) query interface over the gold data,
     served via a backend endpoint (39). Verify answers are grounded in the served data + cited.
  4. `.../capstone-data-pipeline/eval.md` — an eval of the interface's answer quality + a data-freshness/
     quality report. Verify the eval is reproducible and the freshness/quality metrics are reported.
- **Acceptance criteria**: the medallion pipeline is idempotent + quality-gated; serving queries are
  correct; the RAG interface answers are grounded in the governed data + cited; the eval is reproducible.
- **Done bar**: runnable end-to-end (raw data → governed warehouse → grounded interface) + web-verified.

## Read more

**Books**

- **Blue Team Handbook: Incident Response Edition** — Don Murdoch (2nd ed., 2014). Widely used field reference for defenders and incident responders.
- **Applied Network Security Monitoring** — Chris Sanders, Jason Smith (2013). Standard reference for building detection and monitoring practice (NSM).

**Papers & articles**

- **SP 800-61 Rev. 2: Computer Security Incident Handling Guide** — NIST (2012). The canonical US government reference framework for incident response process. <https://csrc.nist.gov/pubs/sp/800/61/r2/final>
- **MITRE ATT&CK** — MITRE Corporation (ongoing). Also the standard reference for defenders to map detections and coverage against known adversary techniques. <https://attack.mitre.org/>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Security suite — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Security suite — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 13 · Security suite.

> _Content originated in the now-closed FS-SE plan (topic 60); it now lives here in
> full — this course block is self-contained._

## In which paths — `capstone-real-world-delivery`, `capstone-secure-service`, `capstone-data-pipeline` (DD-20)

All three are placed, in this order, immediately after `defensive-security` and before
`detection-engineering-and-siem-operations` — their latest prerequisite (`defensive-security` itself,
or `capstone-solid-core` for `capstone-real-world-delivery`) always precedes this position:

- `interview-ready/software-engineer` — Go deeper · Security suite, right after `defensive-security`.
- `immediately-effective/software-engineer` — Deepening band · Security suite, right after `defensive-security`.
- `fundamentally-strong/software-engineer` — Stage 13 · Security suite, right after `defensive-security`.

See [DD-20](../../tech-docs.md#design-decisions) for the full reconciliation ruling.

---

← Back to the [course library catalog](./README.md)
