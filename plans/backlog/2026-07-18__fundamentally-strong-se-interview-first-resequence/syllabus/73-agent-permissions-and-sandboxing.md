# 73 · Agent Permissions & Sandboxing (By Example, Python)

**Mapping row** (frozen [tech-docs §Canonical Mapping Table](../tech-docs.md#canonical-mapping-table)):
N=73 · Phase 3 · Deepening (AI & harness engineering — harness cluster) · By Example · Python · folder
weight 830 / learn 173 / drill 273. **NEW (Addition 2)**. Cluster language **Python** (DN-12).

**Scope note**: keeping an agent that can run shell commands, edit files, and hit the network from doing
harm — **approval models** (allow/deny/ask, enforced by the harness, not the model), **sandboxed
execution** (OS-level isolation, containers, restricted filesystems/network), and **guardrails**
(prompt-injection defense, allow-lists, dry-run/plan mode). Builds on
[N=71 Agent Tools & MCP](./71-agent-tools-and-mcp.md) (the tool boundary is where permissions live) and
draws on [N=91 Security Essentials](./README.md) forward-referenced from Phase 1 fundamentals.

## Why this exists · the big idea

- **The problem before the solution**: an agent with a shell tool and a long leash can delete files,
  exfiltrate secrets, or be hijacked by malicious content it reads — and it will do so confidently and
  fast. Autonomy without constraint is a liability; the safety layer is what makes autonomy usable.
- **Keep-this-if-you-forget-everything**: the model is untrusted and the content it reads is untrusted —
  so permissions and sandboxing are enforced by the **harness around** the model (deny → ask → allow),
  never by asking the model nicely.
- **Big ideas touched**: `security-by-design` (constrain capability at the boundary, assume the model
  and its inputs are hostile), `determinism-vs-emergence` (deterministic guardrails around a
  non-deterministic actor).

## Prerequisites

- **Prior topics**: [N=71 Agent Tools & MCP](./71-agent-tools-and-mcp.md) (the tool boundary),
  [N=70 The Agent Loop](./70-the-agent-loop.md), the security fundamentals from Phase 1/earlier, and
  [N=4 Just Enough Python](./README.md).
- **Tools & environment**: a macOS/Linux terminal; Python 3.x under `uv`; a container runtime (Docker/
  Podman) and/or an OS sandbox mechanism; the agent loop + tools from
  [N=70](./70-the-agent-loop.md)/[N=71](./71-agent-tools-and-mcp.md); `pytest`; Neovim/VSCode.
- **Assumed knowledge**: the agent loop and tool dispatch; basic OS concepts (processes, filesystem
  permissions); the no-secrets-in-git rule.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (DD-28 convention).

- 2026-07-18 — the deny/ask/allow permission model, sandboxing via containers/OS isolation, and
  prompt-injection as a threat class are **stable** security concepts; prompt injection is tracked by
  the OWASP guidance for LLM/agentic applications. `[Needs Verification]`: the exact current OWASP entry
  identifier + title — confirm against the published list at authoring.
- 2026-07-18 — `[Needs Verification]`: the exact container/sandbox runtime versions + flags — pin at
  authoring; sandbox escape surfaces evolve.
- 2026-07-18 — permission-model specifics differ by harness — keep the module principle-based and
  tool-agnostic; name a concrete harness only as an illustration.

## Concepts

1. **co-01 · why-agents-need-guardrails** — an agent takes real actions with real consequences, so
   unconstrained autonomy is a safety and security risk.
2. **co-02 · untrusted-model-and-inputs** — both the model's outputs and the content it reads are
   untrusted; safety cannot depend on the model's goodwill.
3. **co-03 · deny-ask-allow-model** — the permission model resolves each action to deny, ask (human
   approval), or allow — enforced by the harness.
4. **co-04 · harness-enforced-not-model-enforced** — permissions are enforced by the code around the
   model, never by instructing the model to behave.
5. **co-05 · tool-permission-scoping** — each tool is granted the minimum capability it needs (read-only,
   a specific dir, no network).
6. **co-06 · allow-lists-and-deny-lists** — constraining which commands/paths/hosts a tool may touch via
   explicit lists.
7. **co-07 · human-in-the-loop-approval** — routing risky actions to an explicit human approval gate
   before execution.
8. **co-08 · plan-mode-vs-act-mode** — a read-only planning pass separated from a write-enabled execution
   pass, with approval between.
9. **co-09 · dry-run-preview** — previewing an action's effect (the diff, the command) before executing
   it.
10. **co-10 · sandboxing-fundamentals** — isolating risky execution so its effects cannot reach the host
    beyond a boundary.
11. **co-11 · container-isolation** — running tool execution inside a container limits filesystem,
    network, and process reach.
12. **co-12 · filesystem-sandbox** — restricting reads/writes to a working directory prevents touching
    the rest of the machine.
13. **co-13 · network-egress-control** — blocking or allow-listing network egress prevents exfiltration
    and unwanted calls.
14. **co-14 · resource-limits** — CPU/memory/time limits stop a runaway or malicious tool from consuming
    the host.
15. **co-15 · reversibility-and-small-steps** — preferring small, independently revertable actions bounds
    the blast radius of a mistake.
16. **co-16 · prompt-injection-threat** — untrusted content the agent reads can embed instructions that
    hijack its goal.
17. **co-17 · prompt-injection-defense** — treating tool/fetched content as data (not instructions),
    sanitizing it, and guarding tool triggers.
18. **co-18 · secret-handling** — keeping secrets out of the model's context and out of tool outputs;
    the no-secrets rule applies to agents.
19. **co-19 · audit-logging** — logging every permission decision + action for after-the-fact review.
20. **co-20 · least-privilege-by-default** — an agent starts with the minimum capability and is granted
    more only as justified.
21. **co-21 · capability-escalation-control** — controlling how (and whether) an agent can gain more
    capability mid-session.
22. **co-22 · failure-safe-defaults** — when a permission decision is ambiguous, default to deny/ask, not
    allow.

## Tensions & trade-offs — when NOT to reach for this

- **Safety vs autonomy/velocity**: every approval gate and sandbox boundary slows the agent and adds
  friction. Too much and the agent is useless; too little and it is dangerous. Calibrate the gate to the
  action's blast radius — auto-allow reads, ask for writes, deny destructive-by-default.
- **Sandbox strength vs cost**: a full container per tool call is strong but slow and heavy; a
  filesystem+egress restriction is lighter but weaker. Match the isolation to the threat.
- **When NOT to run it at all**: some actions (production writes, irreversible deletes, spending money)
  should not be delegated to an agent without a human at the gate — recognising the actions that must
  stay human is itself the skill.

## Lineage — why it beat the alternative

- Early agents ran tools with the operator's full privileges and trusted the model to behave — until
  prompt injection and confident-but-wrong actions made the risk obvious. The industry converged on the
  same defense the rest of security already knew: least privilege, enforced at a boundary the untrusted
  actor cannot cross, with human approval for high-blast-radius actions and sandboxing for execution.
  This is the safety layer that makes the [agent loop](./70-the-agent-loop.md) and its
  [tools](./71-agent-tools-and-mcp.md) deployable, and it is the security discipline the
  [pentest-engine capstone](./97c-capstone-build-your-own-pentest-engine.md) must itself embody.

## Worked examples

Colocated under `agent-permissions-and-sandboxing/learning/code/`. Each constrains a tool-equipped agent
and proves the constraint holds against a hostile case. Contiguous `ex-01..ex-48`. Every example cites
the `co-NN` it exercises.

> **Volume-target floor**: this syllabus lists **48** of the required **≥75** (the 75–85 By-Example/
> Primer band, floor not cap — see
> [prd.md §Volume-target bands](../prd.md#volume-target-bands-inherited-from-sibling-dd-34-floor-not-cap-dd-8)).
> The maker adds **≥27** more `ex-NN` entries at authoring time, continuing the numbering and pattern
> taxonomy below, before this topic passes its by-example quality gate.

### Beginner (ex 01–16)

1. **ex-01 · unconstrained-agent-risk** — demonstrate (safely) an agent that could delete a file, then
   motivate the guardrail — verify the risky call is possible without constraint. (co-01)
2. **ex-02 · deny-a-tool** — a permission layer that denies a named tool — verify the call is blocked.
   (co-03, co-05)
3. **ex-03 · allow-a-tool** — explicitly allow a read-only tool — verify it runs. (co-03)
4. **ex-04 · ask-gate** — route a write tool to a human-approval gate — verify it waits for approval.
   (co-03, co-07)
5. **ex-05 · harness-enforced-check** — show the model cannot bypass the deny by "asking" — verify
   enforcement is in the harness. (co-04)
6. **ex-06 · read-only-scope** — scope a filesystem tool to read-only — verify a write attempt fails.
   (co-05)
7. **ex-07 · path-allow-list** — restrict a file tool to one directory — verify an out-of-dir path is
   rejected. (co-06, co-12)
8. **ex-08 · command-allow-list** — a shell tool limited to allow-listed commands — verify a disallowed
   command is blocked. (co-06)
9. **ex-09 · plan-mode-first** — a read-only planning pass before edits — verify no write occurs during
   planning. (co-08)
10. **ex-10 · act-after-approval** — switch to act-mode only after approving the plan — verify writes
    appear only after approval. (co-08, co-07)
11. **ex-11 · dry-run-diff** — preview a file edit as a diff before applying — verify the diff matches the
    applied change. (co-09)
12. **ex-12 · dry-run-command** — preview a shell command before running — verify the preview. (co-09)
13. **ex-13 · small-reversible-steps** — drive a change as revertable steps — verify each reverts cleanly.
    (co-15)
14. **ex-14 · audit-log-decisions** — log each permission decision + action — verify a complete audit
    trail. (co-19)
15. **ex-15 · least-privilege-default** — start an agent with minimal tools, add on justification —
    verify the default is minimal. (co-20)
16. **ex-16 · failsafe-default-deny** — an ambiguous action defaults to deny/ask — verify it is not
    auto-allowed. (co-22)

### Intermediate (ex 17–34)

1. **ex-17 · container-sandboxed-shell** — run a shell tool inside a container — verify host files are
   untouched. (co-10, co-11)
2. **ex-18 · filesystem-sandbox** — bind only a working dir into the sandbox — verify no access outside
   it. (co-12)
3. **ex-19 · network-egress-block** — block network egress from a sandboxed tool — verify an outbound
   call fails. (co-13)
4. **ex-20 · network-allow-list** — allow-list one host for egress — verify only that host is
   reachable. (co-13, co-06)
5. **ex-21 · resource-limit-cpu-mem** — cap CPU/memory on a sandboxed tool — verify a runaway is
   stopped. (co-14)
6. **ex-22 · timeout-a-tool** — bound a tool's runtime — verify a hanging tool is killed. (co-14)
7. **ex-23 · prompt-injection-probe** — feed the agent content with "ignore prior instructions" —
   verify the guardrail blocks the injected instruction. (co-16, co-17)
8. **ex-24 · content-as-data** — treat fetched content as data, not instructions — verify embedded
   directives are not executed. (co-17)
9. **ex-25 · sanitize-tool-output** — inspect + sanitize tool output before reuse — verify a suspicious
   payload is flagged. (co-17)
10. **ex-26 · secret-not-in-context** — ensure secrets never enter the model's context — verify the
    context is secret-free. (co-18)
11. **ex-27 · redact-secrets-in-logs** — redact secrets from tool outputs + logs — verify no secret is
    logged. (co-18, co-19)
12. **ex-28 · escalation-request-gate** — an agent requesting more capability must pass a gate — verify
    escalation is controlled. (co-21)
13. **ex-29 · per-tool-sandbox-profile** — different tools get different sandbox profiles — verify each
    profile is enforced. (co-05, co-10)
14. **ex-30 · human-approval-for-destructive** — force approval for a delete/migration — verify it cannot
    run unapproved. (co-07, co-22)
15. **ex-31 · reversible-write-with-backup** — back up before a write so it can be reverted — verify the
    restore. (co-15)
16. **ex-32 · injection-via-tool-result** — a tool result carrying an injection payload — verify it is
    neutralized before the model acts. (co-16, co-17)
17. **ex-33 · audit-trail-review** — reconstruct what an agent did from the audit log — verify every
    action is accounted for. (co-19)
18. **ex-34 · policy-driven-permissions** — a declarative permission policy file — verify swapping
    policies changes what is allowed. (co-03, co-05, co-06)

### Advanced (ex 35–48)

1. **ex-35 · fully-sandboxed-coding-agent** — the [coding agent](./70-the-agent-loop.md) running with
   all tools sandboxed + gated — verify it completes a task without host access. (co-05, co-10–co-14)
2. **ex-36 · injection-resistant-web-agent** — an agent browsing untrusted pages that resists injection
   — verify a crafted page cannot hijack it. (co-16, co-17)
3. **ex-37 · egress-controlled-fleet** — a browser/tool fleet with per-task egress control — verify no
   unexpected outbound call. (co-13, co-11)
4. **ex-38 · escalation-audit** — log + review every capability escalation in a session — verify the
   trail. (co-21, co-19)
5. **ex-39 · defense-in-depth** — combine deny/ask/allow + sandbox + egress control + audit on one agent
   — verify each layer independently blocks its threat. (co-03, co-10, co-13, co-19)
6. **ex-40 · red-team-the-agent** — attempt to make the agent exfiltrate a secret or escape the sandbox
   — verify every attempt is blocked. (co-16, co-18, co-10)
7. **ex-41 · reversibility-under-failure** — a failed multi-step action rolls back cleanly — verify no
   partial state remains. (co-15, co-22)
8. **ex-42 · policy-as-code-review** — review a permission policy for gaps — verify the review finds an
   over-broad grant. (co-06, co-20)
9. **ex-43 · sandbox-escape-awareness** — demonstrate a known weak isolation + the stronger fix — verify
   the fix closes the gap. (co-10, co-11)
10. **ex-44 · human-gate-workflow** — a full approval workflow (request → preview → approve → execute →
    audit) — verify each stage. (co-07, co-09, co-19)
11. **ex-45 · secret-scoped-tool** — a tool needing a secret gets it via a scoped, non-logged channel —
    verify the secret never reaches the model/logs. (co-18)
12. **ex-46 · least-privilege-refactor** — tighten an over-privileged agent to least privilege — verify
    it still completes its task. (co-20, co-05)
13. **ex-47 · injection-guardrail-suite** — a test suite of injection payloads against the guardrails —
    verify all are blocked. (co-16, co-17)
14. **ex-48 · capstone-guarded-agent** — a coding agent with deny/ask/allow permissions, sandboxed +
    egress-controlled execution, injection defenses, secret hygiene, and a full audit log — verify it
    completes a task while every guardrail provably holds against a red-team pass. (co-01–co-22)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: wrap the [coding agent](./70-the-agent-loop.md) in a complete **safety layer** — a
  deny/ask/allow permission model enforced by the harness, sandboxed tool execution (container/OS
  isolation, filesystem + egress restriction, resource limits), prompt-injection defenses, secret
  hygiene, and an audit log — then prove the guardrails hold under a red-team pass.
- **Concepts exercised**: [ ] deny/ask/allow + harness-enforced (co-03, co-04) [ ] tool scoping +
  allow-lists (co-05, co-06) [ ] plan/act + dry-run + human gate (co-07–co-09) [ ] sandbox + filesystem +
  egress + resource limits (co-10–co-14) [ ] injection defense (co-16, co-17) [ ] secret hygiene + audit
  (co-18, co-19) [ ] least privilege + failsafe defaults (co-20, co-22).
- **Ordered steps**:
  1. `agent-permissions-and-sandboxing/learning/capstone/code/` — a deny/ask/allow permission layer over
     the agent's tools with an audit log. Verify a denied tool is blocked and logged.
  2. Sandbox tool execution (container + filesystem + egress + resource limits). Verify host files,
     network, and resources are protected.
  3. Add prompt-injection defenses + secret hygiene. Verify a crafted injection and a secret-exfiltration
     attempt both fail.
  4. Run a red-team pass attempting escape/exfiltration/hijack. Verify every attempt is blocked and
     audited, and the agent still completes a legitimate task.
- **Acceptance criteria**: the agent completes a real coding task; every risky action is denied, gated,
  or sandboxed per policy; a red-team pass cannot escape the sandbox, exfiltrate a secret, or hijack the
  agent via injection; every decision and action is in the audit log.
- **Done bar**: runnable end-to-end (guardrails provably hold under the red-team pass) + web-verified.

## Read more

- **OWASP Top 10 for LLM / Agentic Applications** — the authoritative catalog of agent security risks,
  including prompt injection (cite the exact entry + version at authoring).
- **Building Effective Agents** — Anthropic (2024). On safe agent design and human oversight.
  <https://www.anthropic.com/engineering/building-effective-agents>

---

← Previous: [N=72 · Agent Context & Memory](./72-agent-context-and-memory.md) · Next:
[N=74 · Agent Orchestration, Subagents & Observability](./74-agent-orchestration-subagents-and-observability.md) →
