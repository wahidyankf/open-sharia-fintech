# 95 · Detection Engineering & SIEM Operations (By Example, XML/rules + config + Python)

**Mapping row** (frozen [tech-docs §Canonical Mapping Table](../tech-docs.md#canonical-mapping-table)):
N=95 · Phase 3 · Deepening (security suite) · By Example · XML/rules + config + Python · folder weight
1050 / learn 195 / drill 295. **NEW (Addition 4)** — detection-engineering **principles**; Wazuh's XML
ruleset is the worked example, not the subject. **Prereq: [N=94 `defensive-security`](./README.md).
Difficulty: intermediate** (per DN-15). Distinct from the concept-level N=94 (two altitudes, never
merged — RD-14).

**Scope note**: the **hands-on** craft of turning raw logs into reliable alerts — **decoders/parsers**
(extracting fields from log lines), **correlation/detection rules** (matching + chaining events),
**false-positive tuning**, **dashboards**, and **alert triage**. Where [N=94 Defensive
Security](./README.md) teaches detection _as a concept_ (blue-team, monitoring, IR at the idea level),
this module has the reader _operate a SIEM and write rules_. A Wazuh XML ruleset + decoders are the
concrete worked example; the transferable skill is detection engineering, applicable to any SIEM.

## Why this exists · the big idea

- **The problem before the solution**: raw logs are a firehose of noise; an attack is a faint signal
  buried in millions of benign lines. Detection engineering is the discipline of writing the parsers and
  rules that surface the signal reliably — too loose and analysts drown in false positives, too tight
  and real attacks slip through.
- **Keep-this-if-you-forget-everything**: a detection is a testable hypothesis about attacker behavior —
  parse the log into fields, write a rule that fires on the pattern, then tune it against real traffic
  until the true-positive-to-false-positive ratio is workable.
- **Big ideas touched**: `correctness-vs-pragmatism` (a perfect detection that never ships loses to a
  good one that is tuned and running), `security-by-design` (detection is a first-class engineering
  artifact — versioned, tested, reviewed).

## Prerequisites

- **Prior topics**: [N=94 Defensive Security](./README.md) (blue-team concepts, monitoring, IR),
  [N=91 Security Essentials](./README.md), [N=93 Offensive Security](./README.md) (to know what attacks
  look like), and [N=4 Just Enough Python](./README.md) (for log-processing + rule-testing scripts).
- **Tools & environment**: a macOS/Linux terminal; a SIEM to operate (Wazuh as the worked example,
  self-hostable per [N=24](./24-self-hosting-essentials.md)) — pinned CVE-clean at authoring; sample log
  datasets (free, teachable); Python for parsing/testing; Neovim/VSCode.
- **Assumed knowledge**: reading logs; regular expressions; XML basics; the attacker techniques from
  N=93; blue-team concepts from N=94.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (DD-28 convention).

- 2026-07-19 — detection-engineering principles (decoders/parsing, signature vs anomaly rules,
  correlation, FP tuning, the detection-as-code lifecycle, MITRE ATT&CK mapping) are **stable, vendor-
  independent**; frameworks like Sigma (portable rule format) and MITRE ATT&CK are established.
- 2026-07-19 — `[Needs Verification]`: exact Wazuh version + its decoder/rule XML schema + ruleset paths
  — pin at authoring; the XML surface evolves across Wazuh versions.
- 2026-07-19 — `[Needs Verification]`: any sample dataset's license (must be free-to-use-and-teachable) —
  verify before use; do not reproduce proprietary rule content.

## Concepts

1. **co-01 · what-detection-engineering-is** — the disciplined practice of building, testing, and tuning
   detections that turn logs into reliable alerts.
2. **co-02 · logs-as-telemetry** — logs, events, and telemetry are the raw material; detection quality is
   bounded by the telemetry available.
3. **co-03 · log-ingestion** — a SIEM ingests logs from many sources into a normalized pipeline.
4. **co-04 · decoders-and-parsing** — a decoder extracts structured fields (user, ip, action) from an
   unstructured log line.
5. **co-05 · field-normalization** — mapping heterogeneous source fields to a common schema lets rules
   generalize across sources.
6. **co-06 · signature-vs-anomaly-detection** — signature rules match known-bad patterns; anomaly
   detection flags deviations from a baseline.
7. **co-07 · writing-a-detection-rule** — a rule specifies the condition (fields, thresholds, patterns)
   that fires an alert.
8. **co-08 · rule-severity-levels** — rules carry a severity so triage can prioritize.
9. **co-09 · correlation-rules** — a correlation rule chains multiple events (e.g. failed logins → then
   a success) into one higher-fidelity alert.
10. **co-10 · thresholding-and-frequency** — firing on N events in a time window (brute-force, scanning)
    is a core correlation primitive.
11. **co-11 · false-positives-and-tuning** — most raw rules over-fire; tuning against real traffic is the
    bulk of the work.
12. **co-12 · true-positive-vs-false-positive-tradeoff** — every threshold trades missed attacks against
    analyst noise; the ratio is the design decision.
13. **co-13 · allow-listing-and-exceptions** — excluding known-benign sources/behaviors reduces false
    positives without blinding the rule.
14. **co-14 · mitre-attack-mapping** — mapping detections to MITRE ATT&CK techniques gives coverage a
    shared, gap-analyzable framework.
15. **co-15 · detection-as-code** — rules are version-controlled, reviewed, and tested like software, not
    edited live in production.
16. **co-16 · testing-a-detection** — replaying known-malicious + known-benign logs verifies a rule fires
    correctly and does not over-fire.
17. **co-17 · sigma-and-portable-rules** — a portable rule format (Sigma) expresses detections
    independent of a specific SIEM.
18. **co-18 · dashboards-and-visualization** — dashboards summarize alert volume, severity, and trends
    for situational awareness.
19. **co-19 · alert-triage** — triage assesses each alert (true/false positive, severity, scope) and
    routes it.
20. **co-20 · enrichment** — enriching an alert with context (geoip, asset criticality, threat intel)
    speeds triage.
21. **co-21 · incident-escalation** — a triaged true positive escalates into the incident-response
    process (from N=94).
22. **co-22 · detection-lifecycle** — detections are created, tuned, measured, and retired; coverage is
    maintained continuously, not once.
23. **co-23 · metrics-and-coverage** — measuring detection coverage, FP rate, and time-to-detect drives
    improvement.
24. **co-24 · adversary-emulation-for-detection** — replaying attacker techniques (from N=93) validates
    that detections actually catch them.

## Tensions & trade-offs — when NOT to reach for this

- **Sensitivity vs noise**: the central tension of the field. A rule tuned to catch everything buries
  analysts in false positives until they ignore alerts (alert fatigue); a rule tuned for silence misses
  real attacks. The FP/TP ratio is a deliberate, measured decision per detection, not a default.
- **Signature vs anomaly**: signatures are precise but only catch known patterns; anomaly detection
  catches novel behavior but is noisy and hard to tune. Mature coverage uses both, matched to the threat.
- **When NOT to write a new detection**: if the telemetry to detect a technique does not exist, a rule
  is theater — fix the logging first. And a detection with no plan to tune and maintain it is worse than
  none, because it will rot into noise.

## Lineage — why it beat the alternative

- Security monitoring evolved from grepping logs by hand, to static signature IDS, to SIEMs correlating
  many sources, to modern **detection-as-code**: rules authored, tested, reviewed, and versioned like
  software, mapped to MITRE ATT&CK for coverage analysis, and expressed portably (Sigma) so they survive
  a SIEM change. This won because ad-hoc, live-edited rules do not scale, cannot be tested, and rot into
  noise. Wazuh's decoder+rule XML is one concrete instance of the pattern; the transferable skill —
  parse, detect, correlate, tune, measure — applies to any SIEM. This module operationalizes the
  concept-level [N=94 Defensive Security](./README.md) and feeds the
  [pentest-engine capstone](./97c-capstone-build-your-own-pentest-engine.md) (which must evade + be
  caught by detections).

## Worked examples

Colocated under `detection-engineering-and-siem-operations/learning/code/` (decoder/rule XML, config,
and Python test/replay harnesses). Each writes or tunes a detection and verifies it against replayed
logs. Wazuh XML is the worked example; each also notes the portable (Sigma-style) equivalent. Contiguous
`ex-01..ex-52`. Every example cites the `co-NN` it exercises.

> **Volume-target floor**: this syllabus lists **52** of the required **≥75** (the 75–85 By-Example/
> Primer band, floor not cap — see
> [prd.md §Volume-target bands](../prd.md#volume-target-bands-inherited-from-sibling-dd-34-floor-not-cap-dd-8)).
> The maker adds **≥23** more `ex-NN` entries at authoring time, continuing the numbering and pattern
> taxonomy below, before this topic passes its by-example quality gate.

### Beginner (ex 01–18)

1. **ex-01 · ingest-a-log-source** — configure the SIEM to ingest a sample log file — verify events
   appear. (co-03)
2. **ex-02 · read-a-raw-log** — inspect an unstructured log line and identify its fields — verify the
   fields by hand. (co-02)
3. **ex-03 · first-decoder** — write a decoder extracting user + ip from a log line — verify the parsed
   fields. (co-04)
4. **ex-04 · decoder-regex** — a regex-based decoder for a custom format — verify field extraction.
   (co-04)
5. **ex-05 · field-normalization** — map two sources' fields to a common schema — verify normalized
   output. (co-05)
6. **ex-06 · first-detection-rule** — a rule firing on a specific event (e.g. a failed login) — verify it
   fires on a matching log. (co-07)
7. **ex-07 · rule-severity** — assign a severity to a rule — verify it appears on the alert. (co-08)
8. **ex-08 · rule-does-not-overfire** — verify the rule does NOT fire on a benign log. (co-07, co-11)
9. **ex-09 · match-a-field-value** — a rule matching a specific field value — verify precise matching.
   (co-07, co-04)
10. **ex-10 · replay-a-log-to-test** — a Python harness replaying a log file through the SIEM — verify
    the expected alerts. (co-16)
11. **ex-11 · known-bad-vs-known-good** — replay a malicious + a benign sample — verify one fires, one
    does not. (co-16, co-12)
12. **ex-12 · signature-rule** — a signature rule for a known-bad string — verify the match. (co-06)
13. **ex-13 · map-to-mitre** — tag a detection with a MITRE ATT&CK technique id — verify the mapping.
    (co-14)
14. **ex-14 · sigma-equivalent** — express the same detection in Sigma (portable) — verify parity with
    the SIEM rule. (co-17)
15. **ex-15 · basic-dashboard** — a dashboard panel of alerts by severity — verify it reflects the
    alerts. (co-18)
16. **ex-16 · triage-an-alert** — triage one alert as TP/FP with a reason — verify the disposition.
    (co-19)
17. **ex-17 · enrich-with-geoip** — enrich an alert with geoip on the source IP — verify the added
    context. (co-20)
18. **ex-18 · version-control-a-rule** — commit a rule to a repo with a message — verify detection-as-code
    hygiene. (co-15)

### Intermediate (ex 19–36)

1. **ex-19 · correlation-failed-then-success** — a correlation rule: N failed logins then a success —
   verify it fires on the chain. (co-09)
2. **ex-20 · brute-force-threshold** — fire on N failures in a time window — verify the threshold.
   (co-10)
3. **ex-21 · port-scan-detection** — detect many-ports-one-source in a window — verify the correlation.
   (co-10, co-09)
4. **ex-22 · tune-a-noisy-rule** — take an over-firing rule and reduce FPs — verify the FP rate drops
   without missing the TP. (co-11, co-12)
5. **ex-23 · allow-list-exception** — add a benign-source exception to a rule — verify FPs drop, TPs
   retained. (co-13)
6. **ex-24 · anomaly-baseline** — establish a baseline + flag a deviation — verify the anomaly fires.
   (co-06)
7. **ex-25 · multi-source-correlation** — correlate events across two log sources — verify the joined
   alert. (co-09, co-05)
8. **ex-26 · severity-escalation-on-chain** — a correlation that raises severity when events chain —
   verify the escalation. (co-08, co-09)
9. **ex-27 · detection-test-suite** — a Python suite replaying TP + FP corpora against a rule set —
   verify pass/fail per rule. (co-16, co-15)
10. **ex-28 · fp-rate-measurement** — measure a rule's FP rate over a benign corpus — verify the metric.
    (co-11, co-23)
11. **ex-29 · coverage-gap-analysis** — map current detections to ATT&CK + find a gap — verify the
    uncovered technique. (co-14, co-23)
12. **ex-30 · write-detection-for-a-technique** — author a detection for a specific ATT&CK technique —
    verify it fires on an emulation of it. (co-07, co-14, co-24)
13. **ex-31 · enrich-with-asset-criticality** — enrich alerts with asset criticality for triage priority
    — verify prioritization. (co-20, co-19)
14. **ex-32 · dashboard-trend** — a dashboard showing alert volume trend over time — verify the trend
    updates. (co-18)
15. **ex-33 · triage-workflow** — a triage workflow (assess → disposition → escalate/close) on a batch —
    verify each alert routed. (co-19, co-21)
16. **ex-34 · escalate-to-incident** — escalate a triaged TP into the IR process (from N=94) — verify the
    handoff. (co-21)
17. **ex-35 · rule-review-pr** — review a detection rule as a PR for correctness + FP risk — verify the
    review catches an over-broad match. (co-15)
18. **ex-36 · sigma-to-siem-conversion** — convert a Sigma rule to the SIEM's native format — verify
    equivalent firing. (co-17)

### Advanced (ex 37–52)

1. **ex-37 · adversary-emulation-replay** — replay an attack sequence (from N=93) + confirm the
   detections catch it — verify the kill-chain alerts. (co-24, co-09)
2. **ex-38 · tune-under-real-traffic** — tune a rule against a large mixed corpus to a target FP rate —
   verify the ratio. (co-11, co-12, co-23)
3. **ex-39 · low-and-slow-detection** — detect a low-and-slow attack spread over a long window — verify
   the long-window correlation. (co-10, co-09)
4. **ex-40 · lateral-movement-chain** — a multi-stage correlation for lateral movement — verify the
   chained alert. (co-09, co-14)
5. **ex-41 · enrichment-with-threat-intel** — enrich alerts with a (free) threat-intel feed — verify
   matched IOCs. (co-20)
6. **ex-42 · detection-lifecycle-retire** — measure a stale rule + retire it with rationale — verify the
   lifecycle step. (co-22, co-23)
7. **ex-43 · coverage-dashboard** — a dashboard of ATT&CK coverage + FP rate + time-to-detect — verify
   the metrics. (co-23, co-18)
8. **ex-44 · full-decoder-plus-ruleset** — a complete decoder + rule set for one log source, tested —
   verify parse → detect → alert end to end. (co-04, co-07, co-16)
9. **ex-45 · regression-test-detections** — re-run the detection suite after a change to catch a
   regression — verify a broken rule is caught. (co-16, co-15)
10. **ex-46 · false-negative-hunt** — find a missed attack (false negative) + write the detection — verify
    it now fires. (co-11, co-24)
11. **ex-47 · portable-ruleset-export** — export a tuned detection set as Sigma for SIEM portability —
    verify it converts cleanly. (co-17)
12. **ex-48 · triage-automation** — auto-triage low-severity alerts with enrichment rules — verify the
    automation dispositions correctly. (co-19, co-20)
13. **ex-49 · incident-from-detection-to-response** — a full flow: detection fires → triage → enrich →
    escalate → IR (N=94) — verify each stage. (co-19, co-20, co-21)
14. **ex-50 · measure-and-improve** — measure coverage + FP + MTTD, then improve one metric — verify the
    improvement. (co-23, co-22)
15. **ex-51 · detection-as-code-pipeline** — a CI pipeline testing detections on every change — verify a
    bad rule fails CI. (co-15, co-16)
16. **ex-52 · capstone-detection-pack** — a versioned, tested, ATT&CK-mapped detection pack (decoders +
    rules + correlations) for one log source, tuned to a target FP rate, with a dashboard, caught against
    an emulated attack — verify parse → detect → correlate → alert → triage end to end. (co-01–co-24)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a complete, tested **detection pack** for one log source — decoders that parse it,
  signature + correlation rules mapped to MITRE ATT&CK, tuned against a benign corpus to a target
  false-positive rate, with a dashboard — and prove it catches an emulated attack while staying quiet on
  benign traffic, all versioned as detection-as-code with a test harness.
- **Concepts exercised**: [ ] decoders + normalization (co-04, co-05) [ ] signature + correlation +
  threshold rules (co-06, co-07, co-09, co-10) [ ] FP tuning + allow-lists (co-11, co-12, co-13)
  [ ] ATT&CK mapping (co-14) [ ] detection-as-code + testing (co-15, co-16) [ ] dashboard + triage
  (co-18, co-19) [ ] adversary-emulation validation (co-24).
- **Ordered steps**:
  1. `detection-engineering-and-siem-operations/learning/capstone/decoders/` + `rules/` — decoders +
     signature/correlation rules for one source, versioned in a repo. Verify a replay parses + fires.
  2. Tune the rules against a benign corpus to a target FP rate with allow-list exceptions. Verify the
     measured FP rate meets the target.
  3. Map each detection to an ATT&CK technique + build a coverage/alert dashboard. Verify the mapping +
     the dashboard.
  4. Emulate an attack (from N=93) + replay it through the pack; verify the kill-chain alerts fire and
     benign traffic stays quiet, via the test harness in CI.
- **Acceptance criteria**: the detection pack parses the source, fires correct alerts on an emulated
  attack, stays under the target FP rate on benign traffic, is ATT&CK-mapped and dashboarded, and is
  versioned + tested as detection-as-code (a broken rule fails the test harness).
- **Done bar**: runnable end-to-end (replayed attack caught, benign quiet, tests pass) + web-verified.

## Read more

- **MITRE ATT&CK** — the authoritative adversary-technique framework detections are mapped against
  (free). <https://attack.mitre.org/>
- **Sigma** — the portable, vendor-neutral detection-rule format (free/open).
- **The Practice of Network Security Monitoring** — Richard Bejtlich. Foundational on detection + triage
  practice.
- **Wazuh documentation** — the authoritative reference for the worked-example decoders + ruleset XML
  (pin the version at authoring; the transferable skill is SIEM-independent).

---

← Previous: N=94 `defensive-security` ([index](./README.md)) · Next: N=96
`vulnerability-management-and-assessment` ([index](./README.md)) →
