---
title: "Authorization and Sanctioned Callers"
description: Who may start this gate, the one workflow permitted to invoke it, why propagation is not, and how a grooming invocation's scope differs from a single-rule one.
when_to_use: Use when deciding whether a given trigger may start this gate, or how wide its audit reaches.
---

# Authorization and Sanctioned Callers

This gate is expensive and its verdict is authoritative, so it does not start on inference. It runs
on an explicit human instruction, or on an invocation from a workflow named here — nothing else.

## Who May Start It

- **The user**, by explicitly naming this gate or unambiguously directing its semantic rule audit.
- **[rules-grooming](../rules-grooming.md)**, at its Step 8, in `EFFECTIVE` mode only.

Never infer authorization from a rule change, a review request, a propagation run, or any workflow
this page does not name.

## Why Grooming, and Only Grooming

A grooming run rewrites governance in bulk. Its own preservation proof is mechanical — an
obligation diff and a line-containment check — and mechanical proof cannot tell whether what
survived still coheres. A reduction can preserve every obligation and still move one into a parent
that contradicts it. That gap is what this gate closes, and it is why grooming is gated on every
run rather than only on its riskier classes.

The permission is specific and non-inherited: a workflow that grooming itself composes gains
nothing from this clause, and may not invoke the gate on grooming's behalf.

## Why Not Propagation

[Propagation](../rules-propagation.md) must not call this gate. That edge was removed so the two
form an acyclic pair — a gate running inside its own sole writer would make its verdict circular.
See [propagation's Step 8](../rules-propagation/step-8-verification.md), which states the same rule
from the other side.

The grooming edge does not restore that cycle. Grooming calls the gate; the gate hands findings to
propagation; propagation calls neither. The graph stays acyclic.

## Scope Under a Grooming Invocation

The Procedure's "inspect only the affected rule and its points of use" is scoped to the caller's
subject, not to a fixed count of rules. Under a grooming invocation the affected set is **the run's
manifest** — every surface its approved reductions touched — plus those surfaces' points of use and
relevant higher authority.

That set is wide, and it is still bounded. A surface the run never touched remains unrelated
governance: out of scope for the audit, and if noticed anyway, recorded as next-sweep input rather
than admitted to this run's ledger.

## Related

- [Rules Quality Gate](../rules-quality-gate.md) — the gate itself.
- [Semantic Audit](./semantic-audit.md) — what the audit decides once authorized.
