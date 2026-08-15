---
title: "Intermediate Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 11
---

Examples 17–34 cover sandbox profiles, hostile content, secrets, escalation, reversibility, audit, and policy. All companion artifacts are offline simulations.

### Example 17: Container Sandboxed Shell

**Brief explanation.** Container Sandboxed Shell makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-17-container-sandboxed-shell/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.

### Example 18: Filesystem Sandbox

**Brief explanation.** Filesystem Sandbox makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-18-filesystem-sandbox/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.

### Example 19: Network Egress Block

**Brief explanation.** Network Egress Block makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-19-network-egress-block/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.

### Example 20: Network Allow List

**Brief explanation.** Network Allow List makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-20-network-allow-list/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.

### Example 21: Resource Limit CPU Mem

**Brief explanation.** Resource Limit CPU Mem makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-21-resource-limit-cpu-mem/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.

### Example 22: Timeout A Tool

**Brief explanation.** Timeout A Tool makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-22-timeout-a-tool/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.

### Example 23: Prompt Injection Probe

**Brief explanation.** Prompt Injection Probe makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-23-prompt-injection-probe/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.

### Example 24: Content As Data

**Brief explanation.** Content As Data makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-24-content-as-data/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.

### Example 25: Sanitize Tool Output

**Brief explanation.** Sanitize Tool Output makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-25-sanitize-tool-output/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.

### Example 26: Secret Not In Context

**Brief explanation.** Secret Not In Context makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-26-secret-not-in-context/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.

### Example 27: Redact Secrets In Logs

**Brief explanation.** Redact Secrets In Logs makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-27-redact-secrets-in-logs/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.

### Example 28: Escalation Request Gate

**Brief explanation.** Escalation Request Gate makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-28-escalation-request-gate/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.

### Example 29: Per Tool Sandbox Profile

**Brief explanation.** Per Tool Sandbox Profile makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-29-per-tool-sandbox-profile/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.

### Example 30: Human Approval For Destructive

**Brief explanation.** Human Approval For Destructive makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-30-human-approval-for-destructive/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.

### Example 31: Reversible Write With Backup

**Brief explanation.** Reversible Write With Backup makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-31-reversible-write-with-backup/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.

### Example 32: Injection Via Tool Result

**Brief explanation.** Injection Via Tool Result makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-32-injection-via-tool-result/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.

### Example 33: Audit Trail Review

**Brief explanation.** Audit Trail Review makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-33-audit-trail-review/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.

### Example 34: Policy Driven Permissions

**Brief explanation.** Policy Driven Permissions makes a guardrail explicit without executing a real tool.

**Diagram.** `request → policy → allow | ask | deny`.

**Annotated code.** `learning/code/ex-34-policy-driven-permissions/example.py`.

**Key takeaway.** Enforcement belongs in the harness.

**Why it matters.** A deterministic boundary limits hostile input and side effects.
