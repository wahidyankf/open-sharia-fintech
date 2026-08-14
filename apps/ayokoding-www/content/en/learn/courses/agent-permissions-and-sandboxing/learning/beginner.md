---
title: "Beginner Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 10
---

Examples 1–16 establish deny/ask/allow policy, scoped tools, planning, reversible work, auditability, least privilege, and fail-safe defaults. Every artifact is credential-free, typed, and simulated: it proves a policy decision without running destructive host commands.

### Example 1: Unconstrained Agent Risk

**Brief explanation.** A raw tool request can name a destructive operation. The example simulates that possibility without executing it. **Diagram.** `agent intent → risky tool`. **Annotated code.** `learning/code/ex-01-unconstrained-agent-risk/example.py`. **Key takeaway.** Capability needs a harness boundary. **Why it matters.** Unconstrained autonomy is a production liability.

### Example 2: Deny A Tool

**Brief explanation.** A policy blocks named tools deterministically. **Diagram.** `tool → deny`. **Annotated code.** `learning/code/ex-02-deny-a-tool/example.py`. **Key takeaway.** Deny is enforced outside the model. **Why it matters.** A model cannot override harness policy.

### Example 3: Allow A Tool

**Brief explanation.** A policy can explicitly allow a read-only tool. **Diagram.** `read → allow`. **Annotated code.** `learning/code/ex-03-allow-a-tool/example.py`. **Key takeaway.** Allow requires a named capability. **Why it matters.** Explicit grants support least privilege.

### Example 4: Ask Gate

**Brief explanation.** Write actions route to an approval decision. **Diagram.** `write → ask → approve`. **Annotated code.** `learning/code/ex-04-ask-gate/example.py`. **Key takeaway.** Human approval is a harness state. **Why it matters.** Destructive work needs accountable consent.

### Example 5: Harness Enforced Check

**Brief explanation.** Model text cannot bypass a denied action. **Diagram.** `model request → harness deny`. **Annotated code.** `learning/code/ex-05-harness-enforced-check/example.py`. **Key takeaway.** Intent is not authority. **Why it matters.** Prompt wording must not change permission.

### Example 6: Read Only Scope

**Brief explanation.** A filesystem profile can permit reads and reject writes. **Diagram.** `write → blocked`. **Annotated code.** `learning/code/ex-06-read-only-scope/example.py`. **Key takeaway.** Scope limits side effects. **Why it matters.** Read-only exploration is safer by default.

### Example 7: Path Allow List

**Brief explanation.** Paths outside a declared root are rejected. **Diagram.** `path → root check`. **Annotated code.** `learning/code/ex-07-path-allow-list/example.py`. **Key takeaway.** Filesystem authority is location-specific. **Why it matters.** Path policy contains blast radius.

### Example 8: Command Allow List

**Brief explanation.** Shell tools admit only named commands. **Diagram.** `command → allow-list`. **Annotated code.** `learning/code/ex-08-command-allow-list/example.py`. **Key takeaway.** Command execution needs a narrow vocabulary. **Why it matters.** Allow-lists block unexpected shell behavior.

### Example 9: Plan Mode First

**Brief explanation.** Planning produces proposed actions without writes. **Diagram.** `plan → no side effect`. **Annotated code.** `learning/code/ex-09-plan-mode-first/example.py`. **Key takeaway.** Plan mode is read-only. **Why it matters.** Review precedes mutation.

### Example 10: Act After Approval

**Brief explanation.** Act mode activates only after approval. **Diagram.** `approval → write`. **Annotated code.** `learning/code/ex-10-act-after-approval/example.py`. **Key takeaway.** State transition gates edits. **Why it matters.** It prevents accidental execution.

### Example 11: Dry Run Diff

**Brief explanation.** A dry run shows an edit before applying it. **Diagram.** `preview diff → apply`. **Annotated code.** `learning/code/ex-11-dry-run-diff/example.py`. **Key takeaway.** Preview is evidence. **Why it matters.** Operators can inspect impact first.

### Example 12: Dry Run Command

**Brief explanation.** A command preview records what would run. **Diagram.** `preview → approval → run`. **Annotated code.** `learning/code/ex-12-dry-run-command/example.py`. **Key takeaway.** Commands should be visible before execution. **Why it matters.** Review stops unsafe invocations.

### Example 13: Small Reversible Steps

**Brief explanation.** Small changes retain a rollback path. **Diagram.** `step → revert`. **Annotated code.** `learning/code/ex-13-small-reversible-steps/example.py`. **Key takeaway.** Reversibility limits damage. **Why it matters.** Failure leaves recoverable state.

### Example 14: Audit Log Decisions

**Brief explanation.** Each decision and action is logged. **Diagram.** `request → decision → audit`. **Annotated code.** `learning/code/ex-14-audit-log-decisions/example.py`. **Key takeaway.** Audit trails reconstruct authority. **Why it matters.** Incidents require evidence.

### Example 15: Least Privilege Default

**Brief explanation.** Agents start with minimal capabilities. **Diagram.** `minimal → justified grant`. **Annotated code.** `learning/code/ex-15-least-privilege-default/example.py`. **Key takeaway.** Privilege is added, not assumed. **Why it matters.** Defaults control risk.

### Example 16: Failsafe Default Deny

**Brief explanation.** Ambiguous actions become deny or ask. **Diagram.** `unknown → deny`. **Annotated code.** `learning/code/ex-16-failsafe-default-deny/example.py`. **Key takeaway.** Uncertainty must not auto-allow. **Why it matters.** Fail-safe policy prevents novel bypasses.
