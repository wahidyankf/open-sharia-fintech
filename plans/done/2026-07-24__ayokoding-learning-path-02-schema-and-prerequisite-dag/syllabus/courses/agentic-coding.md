# Agentic Coding (Annotated-concept, polyglot)

**Course ID**: `agentic-coding` · **Format**: Annotated-concept · **Language**: polyglot.

**Short summary**: Driving AI coding agents to plan, generate, verify

**Scope note**: using AI coding agents as a disciplined development-workflow skill — prompting for
code, the review/verification loop, when to trust versus verify, context management, and guardrails.
`‡ polyglot`: the skill is workflow, not syntax, so the target language varies while the loop stays the
same. This is the _user's_ side of agents; the _builder's_ side — how agents are constructed — is
revisited in the AI band at [`57-agentic-ai`](./agentic-ai.md).

## Why this exists · the big idea

- **The problem before the solution**: an agent will produce plausible, confident, wrong code fast;
  used naively it accelerates the creation of bugs and quietly erodes the author's understanding of
  their own codebase.
- **Keep-this-if-you-forget-everything**: the agent drafts, you verify — treat generated code as an
  untrusted contribution that must pass the same tests, review, and reasoning as any other, and keep a
  tight loop where you check before you build on it.
- **Big ideas touched**: `correctness-vs-pragmatism` (agents are a pragmatism engine — enormous
  leverage on the routine, but correctness stays your job via tests and review, not the model's),
  `determinism-vs-emergence` (the same prompt yields different output — you manage a non-deterministic
  collaborator with context, constraints, and verification rather than expecting a repeatable
  function).

## Prerequisites

- **Prior topics**: [topic 15 Software Testing](./software-testing.md) and
  [topic 30 Software Engineering Practices](./software-engineering-practices.md).
- **Tools & environment**: an AI coding agent/assistant (editor-integrated and/or CLI); a
  version-controlled repo for safe, reversible iteration; a fast test suite as the verification
  harness; Neovim/VSCode with the agent integration (DD-17).
- **Assumed knowledge**: writing and running tests to verify a change (topic 15); code review, small
  commits, and working in trunk (topic 30); reading code in more than one language (the earlier
  primers).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the workflow patterns here (draft-then-verify, context management, tight
  review loops, guardrails) are model- and vendor-independent and deliberately not pinned to a specific
  tool or model version, which change rapidly. The named research foundations (the ReAct
  reasoning-and-acting loop, chain-of-thought prompting) are stable published concepts.
- 2026-07-12 — verified (GAP for plan owner): specific agent products, model names, and their
  capabilities move fast — keep the shipped text tool-agnostic and re-verify any named tool at
  authoring time.
- 2026-07-12 — DD-35 primary-source pass (every cited protocol/standard traced to a real source read):
  - **MCP (Model Context Protocol)** — open protocol over JSON-RPC 2.0; architecture is Hosts /
    Clients / Servers exposing Resources, Prompts, and Tools (co-08). Cited spec revision:
    `2025-11-25` (stable, dated schema at spec.modelcontextprotocol.io). Source: modelcontextprotocol.io
    spec + schema.
  - **AGENTS.md standard** (co-06) — the vendor-neutral instruction-file standard (agents.md,
    stewarded under the Agentic AI Foundation / Linux Foundation). This repo's own AGENTS.md conforms.
    Instruction-file precedence and repo-vs-user layering are harness-specific — the example must state
    which harness it demonstrates and cite that harness's documented precedence order, not a universal one.
  - **Claude Code permissions / plan mode / subagents / skills** (co-09, co-10, co-11, co-20) — the
    permission model is deny → ask → allow, harness-enforced (not model-enforced); plan mode is a
    read-only exploration pass; subagents run in isolated contexts returning summaries; skills are
    packaged, named procedures. Named as one concrete harness; keep shipped text tool-agnostic where the
    concept generalizes.
  - **Prompt-injection / guardrails** (co-19) — grounded in the OWASP Top 10 for Agentic Applications
    (2026 cycle).
  - **Spec-driven development** (co-21) — GitHub's Spec Kit is a real, published toolkit for
    spec-driven agent workflows.
  - Copilot/Cursor/other-vendor specifics are deliberately NOT named in concept claims; if an example
    names one at authoring time, its behavior must be re-verified against that vendor's current docs (DD-35).
- 2026-07-18 — verified: a 2026-07-28 MCP spec revision is real — a stateless-transport RC locked
  2026-05-21, targeting finalization 2026-07-28 (drops the `initialize` handshake and sticky sessions
  for per-request `Mcp-Method`/`Mcp-Name` headers). As of this sweep it is unshipped; the current
  stable/published revision remains `2025-11-25`. Shipped text cites `2025-11-25` as the stable spec
  and does not quote RC-only transport details. Sources:
  <https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/>,
  <https://modelcontextprotocol.io/specification/2025-11-25/changelog>.
- 2026-07-18 — verified: agentskills.io confirms SKILL.md is a real, open, Anthropic-originated
  cross-tool file format, with Claude Code and OpenCode both listed as compatible clients
  (<https://code.claude.com/docs/en/skills>, <https://opencode.ai/docs/skills/>); file-format
  portability is real, but per-harness invocation mechanics still differ (this repo's own
  Claude Code fork-mode vs. OpenCode native-read distinction is one example) — shipped text scopes
  the claim to "file-format portable," not "behaviorally identical." Source:
  <https://agentskills.io/home>.
- 2026-07-18 — verified: the top-ranked entry in OWASP's "Top 10 for Agentic Applications for 2026"
  (OWASP GenAI Security Project, published 2025-12-09) is **ASI01: Agent Goal Hijack**. Sources:
  <https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/>,
  corroborated by <https://neuraltrust.ai/blog/owasp-agentic-ai-top-10>.
- 2026-07-18 — verified: GitHub Spec Kit (<https://github.com/github/spec-kit>) is actively
  maintained — latest release `v0.13.0`, published 2026-07-17T18:58Z UTC; installed via
  `uv tool install specify-cli`, driven by `specify init <project>`. Source: spec-kit releases page
  (Atom feed timestamp verified).
- 2026-07-18 — verified: AGENTS.md remains stewarded by the Agentic AI Foundation (AAIF) under the
  Linux Foundation, formed 2025-12-09 with OpenAI donating AGENTS.md alongside Anthropic (MCP) and
  Block (Goose). Sources:
  <https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation>,
  <https://aaif.io/projects/agents-md/>.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Annotated-concept). Each example below cites the co-NN it exercises. -->

- **co-01 · what-is-agentic-coding** — an agent that autonomously reads a repo, plans, edits, runs tools,
  and iterates, distinct from single-shot autocomplete or snippet generation.
- **co-02 · the-perceive-plan-act-observe-loop** — coding agents run an interleaved reasoning-and-acting
  loop (ReAct-style): observe state, reason about the next step, act via a tool, then observe the result
  before reasoning again.
- **co-03 · context-window-fundamentals** — the agent reasons only within a finite context-window budget, so
  what is or is not loaded directly shapes output quality.
- **co-04 · context-management** — deliberately curating what enters the context window (relevant files,
  docs, prior turns) and pruning what does not, since more context is not always better.
- **co-05 · prompting-for-code** — a well-specified prompt states the goal, constraints, examples, and
  acceptance criteria up front rather than leaving them implicit.
- **co-06 · instruction-files** — a persistent, repo-level file (AGENTS.md/CLAUDE.md) the agent reads
  automatically to learn build/test commands and conventions without being re-told each session.
- **co-07 · tool-use-and-function-calling** — the agent acts by invoking discrete named tools (read file,
  run shell, edit) with structured parameters rather than free-form text output.
- **co-08 · mcp-model-context-protocol** — an open, JSON-RPC-based protocol standardizing how a host
  application connects an agent to external tools, resources, and prompts across vendors.
- **co-09 · plan-mode-vs-act-mode** — separating a read-only exploration/planning phase from a write-enabled
  execution phase, with an explicit approval step between them.
- **co-10 · subagents-and-orchestration** — delegating a bounded sub-task to an isolated agent context so its
  exploration detail stays out of the main conversation and only a summary returns.
- **co-11 · permissions-and-guardrails** — explicit allow/deny/ask rules constraining which tools, paths, or
  commands an agent may use, enforced by the harness rather than the model.
- **co-12 · sandboxing-and-reversibility** — isolating risky agent actions (OS-level sandbox, container) and
  preferring small, independently revertable steps over one large change.
- **co-13 · verification-discipline** — reading, running the test suite, and reviewing the diff before
  building on any agent output; never trusting an unverified change.
- **co-14 · test-driven-agent-workflows** — giving the agent a failing test as the acceptance bar and driving
  it to green through a red-green-refactor cycle.
- **co-15 · diff-review** — applying the same code-review scrutiny to an agent-generated diff as to any human
  contribution before accepting it.
- **co-16 · hallucination-awareness** — an agent can generate plausible, confident, and entirely nonexistent
  APIs or behavior, which only verification against a real source catches.
- **co-17 · trust-vs-verify-calibration** — deciding, task by task, which work is safe to delegate lightly
  (boilerplate, mechanical refactors) versus which demands close human review (security, concurrency, novel
  logic).
- **co-18 · cost-and-token-budgeting** — an agent session consumes tokens/cost per turn, so multi-turn
  iterative work needs an explicit budget and stopping condition.
- **co-19 · prompt-injection-risk** — untrusted content the agent reads (a fetched web page, an issue, a
  file) can embed instructions that hijack the agent's goal unless guarded against.
- **co-20 · agent-skills** — a packaged, filesystem-based procedure (frontmatter + instructions) that the
  agent loads on demand instead of re-deriving or re-pasting the same guidance each session.
- **co-21 · spec-driven-development** — writing an executable specification and acceptance criteria first,
  then using the agent to implement against that spec rather than an ad hoc prompt.
- **co-22 · when-not-to-use-agents** — high-stakes, novel, or cheaply-unverifiable work where delegating
  would trade understanding and safety for speed the situation cannot afford.
- **co-23 · iterative-refinement** — treating agent output as a multi-round correction loop (generate,
  review, feed back the gap, regenerate) rather than expecting one-shot correctness.
- **co-24 · human-in-the-loop** — keeping an explicit human decision point at every risky boundary in a
  session rather than granting the agent full autonomy end to end.

## Tensions & trade-offs — when NOT to reach for this

- **Speed vs understanding**: delegating the code you most need to understand — the tricky core —
  trades short-term velocity for long-term ignorance of your own system. Verify most where it matters
  most; delegate most where it matters least.
- **Automation bias is the real risk**: a fluent, confident answer invites you to skip the review it
  most needs — the tool's persuasiveness is inversely correlated with your scrutiny unless you force
  the loop.
- **When NOT**: high-stakes, novel, or security-critical logic, and any situation where you can't
  cheaply verify the output — if you can't test or review it fast, the agent's speed is a liability,
  not an asset.

## Lineage — why it beat the alternative

- Assisted coding evolved from autocomplete to snippet generators to agents that read a repo, plan,
  edit, run tests, and iterate — the ReAct pattern (interleaved reasoning and acting) and
  chain-of-thought prompting are the research lineage that made the tool loop practical. It won over
  pure hand-coding for routine work because the leverage on boilerplate, mechanical refactors, and
  first drafts is large — but only under the discipline this topic teaches, which is exactly why
  testing ([topic 15](./software-testing.md)) and engineering practice
  ([topic 30](./software-engineering-practices.md)) are hard prerequisites. It hands off to
  [`57-agentic-ai`](./agentic-ai.md), which flips the perspective from _using_ agents to _building_
  them — tool calling, the agentic loop, and evals as the test suite for non-deterministic systems.

## Worked examples

Colocated under `agentic-coding/learning/code/` (code-bearing) or `agentic-coding/learning/artifacts/`
(prompt/session/config artifacts with no runnable code) — DD-20/DD-30. Each is a recorded agent session
(prompt + tool-call log + diff + verification) or a config/prompt artifact. Polyglot: the target language
varies; the workflow does not. Contiguous `ex-01..ex-54`. Every example cites the `co-NN` it exercises;
every concept above is exercised by ≥1 example.

### Beginner

- **ex-01 · what-agentic-coding-is-not** — side-by-side an autocomplete suggestion against an agent session
  that reads the repo, edits multiple files, and runs tests — verify the session log shows multiple tool
  invocations the autocomplete case never has. (co-01)
- **ex-02 · trace-the-agent-loop** — annotate one recorded session transcript, labeling each
  perceive/plan/act/observe step — verify all four phases are labeled in the correct order across at least
  two loop iterations. (co-02)
- **ex-03 · context-window-budget-check** — inspect a session's reported context usage (files loaded, token
  count) — verify the reported count against the model's documented context limit. (co-03)
- **ex-04 · prune-irrelevant-context** — start a session with ten loaded files, prune to the three actually
  relevant, rerun the same question — verify the pruned run's answer stays on-topic while the unpruned run
  cites an irrelevant file. (co-04)
- **ex-05 · minimal-well-specified-prompt** — write a prompt with goal, constraints, one example, and
  acceptance criteria for a pure function — verify the first generated diff satisfies every
  acceptance-criteria bullet. (co-05)
- **ex-06 · vague-vs-specific-prompt-contrast** — prompt the same task once vaguely and once specifically —
  verify the specific prompt's first diff passes its test where the vague prompt's first diff does not.
  (co-05)
- **ex-07 · author-a-project-instruction-file** — write a minimal AGENTS.md/CLAUDE.md declaring the
  build/test commands and one convention — verify the agent's next session runs the declared test command
  without being told. (co-06)
- **ex-08 · instruction-file-precedence** — create a repo-level and a user-level instruction file with one
  conflicting rule — verify which rule the agent follows and cite the documented precedence order. (co-06)
- **ex-09 · first-tool-call-is-a-read** — a session whose first logged action is a file-read tool call before
  any write — verify the read precedes any write in the tool-call log. (co-07)
- **ex-10 · tool-call-log-inspection** — inspect a full session's tool-call log (reads, writes, shell runs) —
  verify every entry records a tool name and its parameters. (co-07)
- **ex-11 · plan-mode-first-pass** — run a read-only planning pass on a multi-file task before allowing edits
  — verify no file was modified during the planning pass. (co-09)
- **ex-12 · act-mode-after-plan-approval** — approve the plan from ex-11, then switch to an edit-enabled mode
  — verify edits appear in the log only after the explicit approval step. (co-09)
- **ex-13 · run-the-suite-before-accepting** — after the agent's first diff, run the test suite before
  accepting it — verify a failing test blocks acceptance and is logged as a rejection reason. (co-13)
- **ex-14 · reject-a-diff-on-inspection** — read a generated diff, spot an unrelated change, reject it —
  verify the rejection is written down with a specific reason tied to the unrelated hunk. (co-15)
- **ex-15 · spot-a-hallucinated-api** — an agent's diff calls a method that does not exist on a known
  standard-library type — verify the mismatch against the real API reference before the diff is accepted.
  (co-16)
- **ex-16 · delegate-boilerplate-safely** — delegate a full boilerplate scaffold (e.g. a config file) —
  verify the review log shows only a skim, not a line-by-line read, and states why that was sufficient.
  (co-17)
- **ex-17 · require-close-review-for-sensitive-code** — delegate a small authentication check, mark it
  high-review before generation — verify a documented line-by-line review precedes acceptance. (co-17)
- **ex-18 · token-usage-per-turn-log** — record the token/cost of each turn across a five-turn session —
  verify the running total against a stated budget ceiling. (co-18)

### Intermediate

- **ex-19 · configure-an-mcp-server** — add an MCP server entry (e.g. a filesystem or docs server) to a
  project's config — verify the agent's tool list includes the new server's tools after restart. (co-08)
- **ex-20 · call-a-tool-via-mcp** — invoke a capability exposed by the configured MCP server mid-session —
  verify the tool call and its JSON-RPC result both appear in the transcript. (co-08)
- **ex-21 · delegate-to-a-subagent** — spin off an isolated subagent for a narrow research task — verify only
  a summary returns to the main session's context, not the subagent's raw exploration transcript. (co-10)
- **ex-22 · parallel-subagent-fan-out** — launch two independent subagents for two unrelated subtasks in one
  session — verify both complete and their outputs merge into the main session without cross-contaminating
  each other's context. (co-10)
- **ex-23 · deny-rule-permission-config** — configure a permission rule denying writes outside a named
  subdirectory — verify an attempted out-of-scope write is blocked and logged as denied. (co-11)
- **ex-24 · allow-list-tool-scoping-for-review** — scope a session to read-only tools for a review-only pass
  — verify no write/edit tool call is invocable during that session. (co-11)
- **ex-25 · sandboxed-shell-command** — run an agent-issued shell command inside an OS-level sandbox — verify
  the command's filesystem/network effect stays isolated from the host outside the sandbox boundary. (co-12)
- **ex-26 · small-reversible-commit-steps** — drive a multi-file change as four small commits instead of one
  large diff — verify each commit can be independently reverted without breaking the others. (co-12)
- **ex-27 · failing-test-as-tripwire** — hand the agent a red test and forbid claiming completion until it
  passes — verify the session log shows an explicit red-to-green transition. (co-14)
- **ex-28 · red-green-refactor-with-agent** — drive a full TDD red/green/refactor cycle with the agent
  performing each phase — verify three distinct diffs, one per phase, in the session record. (co-14)
- **ex-29 · diff-review-checklist** — apply a structured review checklist (scope, tests, style) to one agent
  diff — verify every checklist item is explicitly checked before merge. (co-15)
- **ex-30 · catch-silent-scope-creep** — an agent diff edits one file beyond the original ask — verify the
  reviewer flags and trims the out-of-scope hunk before acceptance. (co-15)
- **ex-31 · budget-a-multi-turn-session** — set a token/turn budget before starting a feature session —
  verify the session halts or escalates when the budget is reached. (co-18)
- **ex-32 · compare-cost-of-scoped-vs-open-prompt** — compare the token cost of an open-ended prompt against a
  scoped one for the identical task — verify the scoped prompt's total cost is lower. (co-18)
- **ex-33 · untrusted-content-injection-probe** — feed the agent a fetched document containing an embedded
  instruction ("ignore prior instructions...") — verify the configured guardrail blocks the injected
  instruction from taking effect. (co-19)
- **ex-34 · sanitize-tool-output-before-reuse** — pass a tool's fetched content back into context and inspect
  it for embedded directives before trusting it — verify a flagged suspicious payload is not acted on.
  (co-19)
- **ex-35 · load-an-agent-skill** — attach a packaged skill (e.g. a project-specific lint/format procedure) to
  a session — verify the agent follows the skill's documented steps instead of improvising its own. (co-20)
- **ex-36 · skill-vs-ad-hoc-instruction** — run the same task once with a skill loaded and once without —
  verify the skill-backed run follows a repeatable, named procedure while the ad hoc run varies between
  attempts. (co-20)
- **ex-37 · write-a-spec-before-prompting** — write an acceptance-criteria spec document, then derive the
  prompt from it — verify the resulting review maps each spec bullet to a line in the diff. (co-21)
- **ex-38 · gherkin-spec-driving-agent-implementation** — hand the agent one Gherkin scenario and have it
  implement to satisfy it — verify the scenario's steps pass against the implementation. (co-21)
- **ex-39 · iterate-on-a-failed-first-attempt** — a first generation fails its test; feed back the failure
  message and request a fix — verify the second diff passes where the first did not. (co-23)
- **ex-40 · multi-round-correction-loop** — run three successive feedback rounds tightening one diff toward
  the acceptance bar — verify the diff converges toward passing rather than diverging across rounds. (co-23)

### Advanced

- **ex-41 · escalate-a-security-critical-change** — identify a security-sensitive diff mid-session and route
  it to mandatory human sign-off instead of auto-accepting — verify a documented human approval exists
  before merge. (co-24, co-22)
- **ex-42 · when-not-to-delegate-a-novel-algorithm** — attempt, then abandon, delegating a genuinely novel
  algorithm design and hand-write it instead — verify a written rationale records why delegation was
  declined. (co-22)
- **ex-43 · unverifiable-output-refusal** — the agent proposes a change to code with no test harness; refuse
  to accept until a test exists — verify no diff merges without an accompanying verification path. (co-22,
  co-13)
- **ex-44 · human-decision-gate-mid-session** — insert an explicit human-approval gate before a destructive
  step (e.g. a schema migration) mid-session — verify the session log shows a pause and an explicit recorded
  approval. (co-24)
- **ex-45 · context-managed-feature-loop** — scope a multi-file feature change to only the relevant
  subsystem's files, excluding the rest of the repo from context — verify the agent's diffs touch no file
  outside the scoped set. (co-04, co-10)
- **ex-46 · mechanical-refactor-across-files** — drive a rename-and-refactor across six files, reviewing each
  file's diff individually — verify each file's diff carries a separate, logged approval. (co-15, co-17)
- **ex-47 · reject-a-confidently-wrong-refactor** — the agent's refactor silently changes runtime behavior;
  catch it via a test regression and reject it with a documented reason. (co-16, co-13)
- **ex-48 · trust-verify-decision-log** — produce a written log mapping every change in a session to an
  explicit trust-or-verify decision with a stated rationale — verify every risky change has a matching verify
  entry. (co-17, co-24)
- **ex-49 · mcp-plus-subagent-research-task** — an MCP-connected subagent researches an external API before
  the main agent implements against it — verify the main session receives only a cited summary, not the
  subagent's raw tool-call trace. (co-08, co-10)
- **ex-50 · prompt-injection-guardrail-config** — configure and test a guardrail rule blocking tool
  invocation triggered from fetched content — verify the rule fires against a crafted injection test case.
  (co-19, co-11)
- **ex-51 · spec-driven-tdd-agent-session** — combine a written spec, a failing test suite, and agent
  implementation to green in one session — verify the spec bullets, the initial red run, and the final green
  run are all present in the record. (co-21, co-14)
- **ex-52 · full-verify-first-feature-session** — run a complete feature session: specified prompt, plan-mode
  pass, act-mode diffs, tests run at each step, final review — verify no diff reached the final state without
  being run and reviewed. (co-05, co-09, co-13, co-15)
- **ex-53 · cost-bounded-iterative-refinement** — bound a multi-round correction loop by a token budget,
  escalating to a human when the budget is exceeded — verify the session halts at the budget and flags the
  unresolved item for review. (co-18, co-23, co-24)
- **ex-54 · post-mortem-a-bad-agent-merge** — analyze a constructed incident where an unverified agent diff
  reached the build and broke it, then write the process fix — verify the fix closes the specific
  verification-loop gap that let the diff through. (co-13, co-16, co-22)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: complete one real feature with an agent under a verify-first discipline — a specified
  prompt, tests as the tripwire, reviewed diffs, and a written record of what you trusted versus
  verified — landing a change you fully understand.
- **Concepts exercised**: [ ] a specified prompt with constraints + acceptance criteria (co-05) [ ] a
  tests-as-tripwire verification loop (co-13, co-14) [ ] a trust/verify decision log (co-17, co-24) [ ]
  context management (co-04) [ ] catching + rejecting a wrong generation (co-15, co-16) [ ] small
  reversible steps (co-12).
- **Ordered steps**:
  1. `.../learning/capstone/prompt.md` — the goal, constraints, examples, acceptance criteria, and a
     failing test. Verify the test fails and the prompt states the acceptance bar.
  2. `.../session/` — drive the agent to green in small steps, reviewing each diff. Verify every
     accepted diff was run and reviewed, and at least one bad generation was caught and rejected with a
     reason.
  3. `.../trust-verify-log.md` — record what was delegated vs hand-verified and why. Verify each risky
     change maps to a human verification step.
- **Acceptance criteria**: the feature passes its tests; every accepted change was verified before
  being built on; the log justifies each trust/verify call; no unreviewed agent output reached the
  final diff.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **AI Engineering: Building Applications with Foundation Models** — Chip Huyen (2025). Current standard
  reference for building production applications, including agents, on top of foundation models.

**Papers & articles**

- **ReAct: Synergizing Reasoning and Acting in Language Models** — Shunyu Yao, Jeffrey Zhao, Dian Yu,
  Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao (2022). Foundational paper defining the
  interleaved reasoning-and-acting loop underlying most modern coding agents.
  <https://arxiv.org/abs/2210.03629>
- **Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** — Jason Wei et al. (2022).
  Foundational paper showing intermediate reasoning steps improve LLM performance, underpinning prompt
  and context engineering practice. <https://arxiv.org/abs/2201.11903>
- **Building Effective Agents** — Anthropic (2024). Widely cited engineering guide distinguishing
  workflows from agents and giving practical patterns for agentic systems.
  <https://www.anthropic.com/engineering/building-effective-agents>
- **Best Practices for Claude Code** — Anthropic (documentation, continually updated). Official
  guidance on agentic coding workflows, context management, and tool use for coding agents.
  <https://code.claude.com/docs/en/best-practices>

## In which paths

- `interview-ready/software-engineer` — Go deeper · AI & harness engineering — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · AI & harness engineering (marquee build-your-own track) — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 12 · AI & harness engineering (marquee build-your-own track).

> _Content originated in the now-closed FS-SE plan (topic 31); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
