# Agentic AI (By Example, Python)

**Course ID**: `agentic-ai` · **Format**: By Example · **Language**: Python.

**Short summary**: Autonomous agents with tools, memory, planning

**Scope note**: building agents, not just calling models — tool/function calling, the agentic loop,
the Model Context Protocol (MCP), memory and context management, and evals as the test suite for
non-deterministic systems. It follows [`56-creating-ai-powered-apps`](./creating-ai-powered-apps.md)
and turns a single model call into a system that reasons, acts, observes, and iterates toward a goal.
`†`: Python, fully type-annotated (DD-39) — every snippet carries type hints in the pyright-clean spirit.

## Why this exists · the big idea

- **The problem before the solution**: a single prompt-and-response can't do multi-step work — it
  can't look something up, run a tool, check the result, and adjust. Wiring that by hand as brittle
  string-parsing gives you a fragile chatbot, not an agent; and because the model is
  non-deterministic, the usual "run the test, it's green" safety net doesn't apply.
- **Keep-this-if-you-forget-everything**: an agent is a loop — the model decides an action, a tool
  executes it, the result feeds back as an observation, and it repeats until a goal or a stop
  condition. Give it tools, a memory, and a way to know it's done; then _evaluate_ it, because you
  can't unit-test a probabilistic thing the old way.
- **Big ideas touched**: `determinism-vs-emergence` (useful behaviour _emerges_ from a model looping
  over tools rather than from a coded-out control flow — powerful, but you trade predictability),
  `correctness-vs-pragmatism` ("provably correct" is off the table for a stochastic system, so you
  ship with evals, guardrails, and human checkpoints — disciplined compromise, not proof).

## Prerequisites

- **Prior topics**: [topic 55 CI/CD & Release Engineering](./cicd-and-release-engineering.md)
  (the pipeline that runs your eval suite as a gate) and [topic 15 Software Testing](./software-testing.md)
  (the testing mindset you'll adapt for non-deterministic systems).
- **Tools & environment**: a macOS/Linux terminal; **Python** at a recent stable release with type
  hints and `pyright`; access to an LLM with tool/function-calling (via an API or a local model); an MCP
  client/server library; an eval harness; Neovim/VSCode with the Python LSP (DD-17).
- **Assumed knowledge**: making a model API call and shaping a prompt (topic 56); writing and running
  a test suite and reasoning about coverage (topic 15); running a job in a CI pipeline (topic 55).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the **agentic loop** (reason → act → observe, the ReAct pattern),
  **tool/function calling**, and **evals as the test methodology** for non-deterministic systems are
  the stable, mainstream concepts; left correctly version-unpinned since specific model and SDK
  versions move fast.
- 2026-07-12 — verified (GAP for plan owner): the **Model Context Protocol (MCP)** is an open standard
  for connecting agents to tools/data and is broadly adopted, but its spec and SDKs are actively
  evolving — pin the exact MCP library version and any model/provider SDK at drafting time, and keep
  the teaching centered on the protocol's _role_ (a standard tool/context interface) rather than a
  frozen API. Do not hard-code any specific model's capabilities.

> DD-35 primary-source pass (2026-07-12). Definitions, loop mechanics, patterns, and paper abstracts traced
> to primary sources (anthropic.com/engineering, platform.claude.com, arXiv PDFs, modelcontextprotocol.io,
> framework docs, genai.owasp.org) and fetched/read. Framework identity and OTel conventions flagged as volatile.

- **Agents vs workflows** — Anthropic: "Workflows are systems where LLMs and tools are orchestrated through
  predefined code paths"; "Agents … are systems where LLMs dynamically direct their own processes and tool
  usage, maintaining control over how they accomplish tasks." The "basic building block … is an LLM enhanced
  with augmentations such as retrieval, tools, and memory." Source: [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (fetched, verbatim).
- **Agentic loop** — Anthropic's client-tool loop, verbatim: send `tools` + message → "Claude responds with
  `stop_reason: "tool_use"`" → "Execute each tool. Format the outputs as `tool_result` blocks" → send a new
  request with the results → "Repeat … while `stop_reason` is `"tool_use"`." "The model never executes
  anything on its own." Server tools (`web_search`, `code_execution`) execute on Anthropic's side. Source:
  [Anthropic — How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works) (fetched, verbatim).
- **ReAct** — Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models," arXiv:2210.03629
  (ICLR 2023): "generate both reasoning traces and task-specific actions in an interleaved manner …
  reasoning traces help the model induce, track, and update action plans … actions allow it to interface
  with … external sources." Source: [arXiv:2210.03629](https://arxiv.org/abs/2210.03629) (PDF fetched, verbatim).
- **Chain-of-thought** — Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language
  Models," arXiv:2201.11903 (NeurIPS 2022): "generating a chain of thought—a series of intermediate
  reasoning steps—significantly improves the ability of large language models to perform complex reasoning."
  Source: [arXiv:2201.11903](https://arxiv.org/abs/2201.11903) (PDF fetched, verbatim).
- **Reflexion** — Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning,"
  arXiv:2303.11366: "reinforce language agents not by updating weights, but … through linguistic feedback …
  verbally reflect on task feedback signals, then maintain their own reflective text in an episodic memory
  buffer." Source: [arXiv:2303.11366](https://arxiv.org/abs/2303.11366) (fetched; HTML render, so verbatim quoting `[Needs Verification]` against the PDF).
- **Planning / plan-and-execute** — LangChain: a **planner** "prompts an LLM to generate a multi-step plan"
  - an **executor** that "invoke[s] 1 or more tools to complete that task"; avoids "having to call the large
    planner LLM for each tool invocation" (unlike per-step ReAct). Source: [LangChain — Plan-and-Execute Agents](https://www.langchain.com/blog/planning-agents) (fetched, verbatim).
- **Workflow patterns** — Anthropic, verbatim: **Prompt Chaining** "decomposes a task into a sequence of
  steps, where each LLM call processes the output of the previous one"; **Routing** "classifies an input and
  directs it to a specialized followup task"; **Parallelization** (sectioning / voting); **Orchestrator-
  Workers** "a central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes
  their results"; **Evaluator-Optimizer** "one LLM call generates a response while another provides
  evaluation and feedback in a loop." Source: [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (fetched, verbatim).
- **Multi-agent** — Anthropic's research system uses "an orchestrator-worker pattern, where a lead agent
  coordinates the process while delegating to specialized subagents that operate in parallel"; "Multi-agent
  systems use about 15× more tokens than chats" — a real cost lesson. OpenAI Agents SDK **Handoffs** "Allow
  agents to delegate to other agents for specific tasks." Sources: [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) (fetched, verbatim).
- **MCP** — "an open-source standard for connecting AI applications to external systems"; "Think of MCP like
  a USB-C port for AI applications." Roles: **MCP Host** ("coordinates and manages one or multiple MCP
  clients"), **MCP Client** ("maintains a connection to an MCP server"), **MCP Server** ("provides context to
  MCP clients"); built on JSON-RPC 2.0. Protocol version strings (e.g. `2025-06-18`) are **volatile**.
  Sources: [modelcontextprotocol.io](https://modelcontextprotocol.io/introduction), [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture), [Anthropic MCP announcement](https://www.anthropic.com/news/model-context-protocol) (fetched, verbatim).
- **Memory** — LangGraph: short-term = "thread-level persistence" (a `checkpointer` + `thread_id`);
  long-term = data that persists "across sessions" (a `store`). Source: [LangGraph — Add memory](https://docs.langchain.com/oss/python/langgraph/add-memory) (fetched, verbatim).
- **Human-in-the-loop** — LangGraph interrupts "allow you to pause graph execution … and wait for external
  input"; use cases include "Pause before executing critical actions (API calls, database changes, financial
  transactions)." Source: [LangGraph — Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) (fetched, verbatim).
- **Guardrails** — OpenAI Agents SDK: guardrails "do checks and validations of user input and agent output"
  (input guardrails on initial input, output guardrails on final output); a tool-input guardrail can
  `reject_content`. Anthropic tool-permissioning: "Apply the principle of least privilege so that a
  successful injection can do minimal damage … run tools in sandboxed environments." Sources: [OpenAI Guardrails](https://openai.github.io/openai-agents-python/guardrails/), [Anthropic — Mitigate injections](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks) (fetched, verbatim).
- **Loop control** — OpenAI Agents SDK: "If we exceed the `max_turns` passed, we raise a `MaxTurnsExceeded`
  exception." LangGraph: exceeding steps raises `GraphRecursionError`; override via `recursion_limit` (the
  commonly-cited default of 25 was not on the official page → `[Needs Verification]`). Anthropic server-tool
  iteration limit returns `stop_reason: "pause_turn"`. Sources: [OpenAI — Running agents](https://openai.github.io/openai-agents-python/running_agents/), [LangGraph — recursion limit](https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT) (fetched, verbatim).
- **Evaluation** — LangSmith trajectory evaluation examines "the exact sequence of messages, including tool
  calls" via `create_trajectory_match_evaluator` or an LLM-as-judge across "grounding and context use, user
  experience quality, and security and safety." Source: [LangSmith — Trajectory evals](https://docs.langchain.com/langsmith/trajectory-evals) (fetched, verbatim).
- **Observability** — OpenTelemetry GenAI agent spans (Invoke Agent Client/Internal, Create Agent) with
  `gen_ai.operation.name = invoke_agent`; **Status: Development** (pre-stable) and the conventions moved to a
  dedicated `semantic-conventions-genai` repo — cite with a "may change" caveat. Source: [OTel GenAI agent spans](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/) (fetched; flagged non-stable).
- **Security** — OWASP LLM01:2025 Prompt Injection "occurs when user prompts alter the LLM's behavior … in
  unintended ways" (direct vs indirect); LLM06:2025 **Excessive Agency** root causes "Excessive
  Functionality / Excessive Permissions / Excessive Autonomy." Willison's **lethal trifecta**: private data +
  untrusted content + "the ability to externally communicate" — "an attacker can easily trick it into
  accessing your private data and sending it to that attacker." Sources: [OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/), [OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/), [Simon Willison — Lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) (fetched, verbatim; confirm OWASP edition year at authoring).
- **Frameworks** — LangGraph "a low-level orchestration framework … for … stateful agents"; OpenAI Agents
  SDK primitives Agents/Handoffs/Guardrails/Sessions; CrewAI "orchestrating autonomous AI agents" (Crews +
  Flows). **AutoGen is now in maintenance mode**, superseded by **Microsoft Agent Framework** (GA
  2026-04-02) — teach AutoGen only with that caveat. Sources: [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview), [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/), [CrewAI](https://docs.crewai.com/introduction), [microsoft/autogen](https://github.com/microsoft/autogen) (fetched, verbatim).
- **When NOT to use an agent** — Anthropic: "find the simplest solution possible, and only increasing
  complexity when needed. This might mean not building agentic systems at all"; add complexity "only when it
  demonstrably improves outcomes." Source: [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (fetched, verbatim).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · agent-vs-workflow** — a workflow orchestrates LLMs through predefined code paths; an agent
  dynamically directs its own process and tool use.
- **co-02 · agentic-loop** — the tool_use loop: request → `tool_use` → execute → `tool_result` → repeat
  while `stop_reason` is `tool_use`.
- **co-03 · augmented-llm** — the building block is an LLM enhanced with retrieval, tools, and memory.
- **co-04 · tool-calling** — expose typed tools, let the model choose and invoke one, and parse the
  structured call back into execution.
- **co-05 · client-vs-server-tools** — client tools your code executes vs server tools the provider runs.
- **co-06 · react-pattern** — interleave reasoning traces with actions so reasoning steers acting (Yao
  et al.).
- **co-07 · chain-of-thought** — intermediate reasoning steps improve complex reasoning (Wei et al.).
- **co-08 · planning-decomposition** — plan-and-execute splits a goal into a planner-made multi-step plan run
  by an executor.
- **co-09 · reflection-self-critique** — Reflexion verbally reflects on feedback into episodic memory to
  improve later trials.
- **co-10 · short-term-memory** — thread-level transcript persistence via a checkpointer + thread id.
- **co-11 · long-term-memory** — cross-session storage and retrieval of prior knowledge into context.
- **co-12 · prompt-chaining** — a sequence of steps where each LLM call processes the previous output.
- **co-13 · routing** — classify an input and direct it to a specialized follow-up task.
- **co-14 · parallelization** — run independent subtasks in parallel (sectioning) or the same task N times
  (voting).
- **co-15 · orchestrator-workers** — a central LLM decomposes work, delegates to worker LLMs, and
  synthesizes results.
- **co-16 · evaluator-optimizer** — one LLM generates while another evaluates and gives feedback in a loop.
- **co-17 · multi-agent-orchestration** — a lead agent coordinates parallel subagents at a large token-cost
  multiple.
- **co-18 · agent-handoffs** — an agent delegates a specific task to another agent.
- **co-19 · mcp** — the Model Context Protocol is a standard host/client/server tool-and-context interface
  (JSON-RPC).
- **co-20 · human-in-the-loop** — an interrupt/approval gate pauses the loop before a consequential action.
- **co-21 · guardrails** — input/output and tool-input validation checks bound agent behavior.
- **co-22 · tool-permissioning** — least privilege and sandboxing on tools limit an injection's blast radius.
- **co-23 · loop-control** — a max-turns / recursion limit bounds the loop and prevents runaway iteration.
- **co-24 · cost-control** — a budget cap and the "is an agent even the right tool" question control agent
  cost.
- **co-25 · agent-evaluation** — trajectory evaluation, task success rate, and LLM-as-judge score a
  non-deterministic agent.
- **co-26 · evals-in-ci** — running the eval suite in CI gates regressions in the agent.
- **co-27 · observability-tracing** — agent spans (OTel GenAI conventions, pre-stable) trace the loop.
- **co-28 · prompt-injection-agents** — direct and indirect prompt injection is amplified once an agent has
  tools (OWASP LLM01).
- **co-29 · excessive-agency** — OWASP LLM06: excessive functionality, permissions, or autonomy is a
  first-class agent risk.
- **co-30 · lethal-trifecta** — private data + untrusted content + an exfiltration path together enable
  data theft (Willison).
- **co-31 · agent-frameworks** — LangGraph / OpenAI Agents SDK / CrewAI / Microsoft Agent Framework
  (AutoGen is now maintenance-mode).
- **co-32 · simplest-solution-first** — find the simplest solution and add agency only when it demonstrably
  improves outcomes.

## Tensions & trade-offs — when NOT to reach for this

- **An agent is often the wrong tool**: if the task is a fixed, known sequence, a plain workflow (a
  deterministic pipeline that calls a model at one step) is cheaper, faster, and far more predictable
  than an autonomous loop. Reach for agency only when the path genuinely can't be enumerated in
  advance.
- **Autonomy multiplies cost and blast radius**: every loop iteration is tokens, latency, and a chance
  to take a wrong, possibly irreversible action. Unbounded tool access plus a loop is how an agent
  runs up a bill or deletes the wrong thing — bound the steps, scope the tools, and gate the dangerous
  ones behind a human.
- **No evals means no safety net**: without an eval suite, you can't tell whether a prompt tweak or a
  model upgrade improved or silently broke the agent. Shipping an agent you can't measure is shipping a
  system you can't maintain.

## Lineage — why it beat the alternative

- Agentic AI emerged once models got good enough at tool-use that the bottleneck moved from "can it
  answer" to "can it act". The ReAct pattern (2022) formalized interleaving reasoning with actions;
  Toolformer showed models could learn to call tools; Reflexion added self-critique loops. The
  practical winner over hand-coded orchestration is the constrained loop-with-tools-and-evals: it
  captures the flexibility that makes agents useful while the eval suite and guardrails supply the
  discipline that stochastic systems otherwise lack — and MCP standardized the tool interface so
  integrations stopped being bespoke. This builds directly on the model-application foundations of
  [topic 56 Creating AI-Powered Apps](./creating-ai-powered-apps.md) and uses the pipeline of
  [topic 55 CI/CD & Release Engineering](./cicd-and-release-engineering.md) to run evals as a gate.

## Worked examples

Colocated under `agentic-ai/learning/code/`; each is typed, `pyright`-clean Python runnable from the CLI
against a local/mockable model (DD-20/DD-30/DD-34/DD-39). Contiguous `ex-01..ex-80`. Every example cites the
`co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · agent-vs-workflow** — a decision table agent vs workflow — verify the dynamic-vs-predefined
  distinction. (co-01)
- **ex-02 · workflow-predefined-path** — annotate a fixed workflow pipeline (model at one step) — verify it
  is deterministic. (co-01)
- **ex-03 · augmented-llm** — annotate the LLM + retrieval + tools + memory building block — verify all
  three augmentations. (co-03)
- **ex-04 · tool-definition** — define a typed tool — verify the schema is offered. (co-04)
- **ex-05 · tool-choose-invoke** — the model chooses and invokes a tool — verify the correct tool fires.
  (co-04)
- **ex-06 · parse-tool-call** — parse a structured tool call and dispatch it — verify the dispatch maps to a
  function. (co-04)
- **ex-07 · two-tools-choose** — expose two tools, the model picks one — verify the appropriate choice.
  (co-04)
- **ex-08 · agentic-loop-steps** — annotate the request → tool_use → tool_result → repeat loop — verify the
  cycle. (co-02)
- **ex-09 · loop-stop-reason** — loop while `stop_reason == "tool_use"` — verify termination on `end_turn`.
  (co-02)
- **ex-10 · client-vs-server-tools** — annotate client vs server tools — verify who executes each. (co-05)
- **ex-11 · react-interleave** — annotate ReAct reasoning + acting interleaved — verify the interleaving.
  (co-06)
- **ex-12 · react-trace** — a reason-then-act trace on a QA task — verify a thought precedes an action.
  (co-06)
- **ex-13 · chain-of-thought** — a CoT prompt with intermediate steps — verify the reasoning steps appear.
  (co-07)
- **ex-14 · cot-exemplars** — few-shot CoT exemplars — verify the model mimics the reasoning. (co-07)
- **ex-15 · plan-and-execute** — a planner producing a multi-step plan — verify the plan lists steps.
  (co-08)
- **ex-16 · executor-step** — an executor running one plan step — verify a single step completes. (co-08)
- **ex-17 · planner-vs-react** — annotate plan-and-execute vs per-step ReAct — verify the call-count
  tradeoff. (co-08)
- **ex-18 · reflection-loop** — a self-critique reflection step — verify the critique changes the retry.
  (co-09)
- **ex-19 · reflexion-memory** — annotate reflective text held in episodic memory — verify the memory
  buffer. (co-09)
- **ex-20 · short-term-memory** — a thread-level transcript with a checkpointer — verify multi-turn recall.
  (co-10)
- **ex-21 · thread-id** — a `thread_id` scoping a conversation — verify separate threads don't mix. (co-10)
- **ex-22 · long-term-memory** — a cross-session store — verify data persists across runs. (co-11)
- **ex-23 · memory-retrieval** — retrieve prior knowledge into context — verify the recalled fact is used.
  (co-11)
- **ex-24 · context-relevance** — annotate keeping context relevant not full — verify pruning. (co-11)
- **ex-25 · prompt-chaining** — a sequence of chained LLM calls — verify each call consumes the prior
  output. (co-12)
- **ex-26 · routing** — classify an input and route to a specialized handler — verify the right route fires.
  (co-13)
- **ex-27 · parallelization-sectioning** — parallel independent subtasks — verify concurrent execution.
  (co-14)

### Intermediate

- **ex-28 · parallelization-voting** — run the same task N times and aggregate by vote — verify the majority
  result. (co-14)
- **ex-29 · orchestrator-workers** — a lead LLM delegating to worker LLMs — verify delegation. (co-15)
- **ex-30 · orchestrator-synthesize** — synthesize worker results into one answer — verify the merge.
  (co-15)
- **ex-31 · evaluator-optimizer** — generate + evaluate in a loop — verify the score drives a revision.
  (co-16)
- **ex-32 · multi-agent-lead-subagents** — a lead agent + parallel subagents — verify parallel context
  windows. (co-17)
- **ex-33 · multi-agent-token-cost** — annotate the ~15× token cost of multi-agent — verify the cost
  tradeoff. (co-17)
- **ex-34 · agent-handoff** — one agent delegating to another — verify the handoff transfers control.
  (co-18)
- **ex-35 · mcp-host-client-server** — annotate MCP host/client/server roles — verify each role. (co-19)
- **ex-36 · mcp-usb-c** — annotate the "USB-C for AI" standard-interface analogy — verify the standardization
  point. (co-19)
- **ex-37 · mcp-connect-tool** — connect a tool via an MCP server — verify the agent calls it. (co-19)
- **ex-38 · mcp-json-rpc** — annotate MCP over JSON-RPC 2.0 — verify the transport. (co-19)
- **ex-39 · human-in-the-loop-interrupt** — an interrupt pausing for approval — verify the loop halts.
  (co-20)
- **ex-40 · approval-gate** — a consequential action gated behind human approval — verify it can't fire
  ungated. (co-20)
- **ex-41 · input-guardrail** — validate user input before the agent runs — verify an unsafe input is
  blocked. (co-21)
- **ex-42 · output-guardrail** — validate the final agent output — verify a bad output is caught. (co-21)
- **ex-43 · tool-input-guardrail** — a tool-input guardrail rejecting secrets — verify a secret is
  rejected. (co-21)
- **ex-44 · tool-permissioning** — annotate least-privilege on tools — verify scoped access. (co-22)
- **ex-45 · tool-sandbox** — annotate sandboxing/scoping tool access — verify the containment. (co-22)
- **ex-46 · max-turns** — a `max_turns` cap raising on exceed — verify `MaxTurnsExceeded` is raised. (co-23)
- **ex-47 · recursion-limit** — a recursion/step limit on the loop — verify the limit halts it. (co-23)
- **ex-48 · loop-terminates** — a loop that halts within the budget — verify termination. (co-23)
- **ex-49 · budget-cap** — annotate a cost budget cap — verify a runaway is stopped. (co-24)
- **ex-50 · when-not-agent** — a decision table agent vs plain workflow — verify the simpler choice wins for
  a fixed task. (co-24)
- **ex-51 · pause-turn** — annotate a server-tool iteration limit (`pause_turn`) — verify the caller
  resumes. (co-23)
- **ex-52 · trajectory-eval** — evaluate the sequence of tool calls (trajectory) — verify it matches a
  reference. (co-25)
- **ex-53 · task-success-rate** — score task success on a dataset — verify the pass rate. (co-25)
- **ex-54 · llm-as-judge** — an LLM judge scoring an answer — verify a different model judges. (co-25)
- **ex-55 · exact-match-scoring** — exact-match scoring on a golden set — verify the match count. (co-25)

### Advanced

- **ex-56 · eval-dataset** — a task dataset for the agent — verify each case has an expected outcome.
  (co-26)
- **ex-57 · evals-in-ci** — wire evals into a CI gate — verify the eval runs in the pipeline. (co-26)
- **ex-58 · regression-bar** — fail CI on regression below the bar — verify a drop blocks the merge. (co-26)
- **ex-59 · agent-span** — annotate an `invoke_agent` OTel span — verify the operation name. (co-27)
- **ex-60 · tracing-attributes** — annotate `gen_ai.*` span attributes — verify the recorded fields. (co-27)
- **ex-61 · otel-development-status** — annotate that OTel GenAI conventions are pre-stable — verify the
  "may change" caveat. (co-27)
- **ex-62 · prompt-injection-direct** — annotate a direct prompt injection on an agent — verify the attack
  shape. (co-28)
- **ex-63 · prompt-injection-indirect** — annotate indirect injection via a tool result — verify the
  untrusted-content vector. (co-28)
- **ex-64 · owasp-llm01** — annotate OWASP LLM01 for agents — verify the direct/indirect distinction.
  (co-28)
- **ex-65 · untrusted-tool-results** — put untrusted content only in tool results — verify data isn't obeyed
  as instructions. (co-28)
- **ex-66 · excessive-agency** — annotate OWASP LLM06 Excessive Agency — verify the risk category. (co-29)
- **ex-67 · excessive-functionality** — annotate the excessive-functionality root cause — verify the
  unneeded-function risk. (co-29)
- **ex-68 · excessive-permissions** — annotate the excessive-permissions root cause — verify the
  over-scoped-permission risk. (co-29)
- **ex-69 · lethal-trifecta** — annotate Willison's lethal trifecta — verify the three legs. (co-30)
- **ex-70 · trifecta-mitigation** — break the trifecta by removing one leg — verify the exfiltration path is
  cut. (co-30)
- **ex-71 · langgraph-stateful** — annotate LangGraph stateful orchestration — verify the graph/state model.
  (co-31)
- **ex-72 · openai-agents-sdk** — annotate OpenAI Agents SDK primitives (agents/handoffs/guardrails) —
  verify each primitive. (co-31)
- **ex-73 · crewai-crews-flows** — annotate CrewAI crews + flows — verify the two constructs. (co-31)
- **ex-74 · autogen-maintenance** — annotate AutoGen maintenance-mode → Microsoft Agent Framework — verify
  the currency caveat. (co-31)
- **ex-75 · simplest-solution** — annotate "find the simplest solution; add agency only when it helps" —
  verify the principle. (co-32)
- **ex-76 · not-agentic-at-all** — annotate "this might mean not building agentic systems at all" — verify
  the restraint. (co-32)
- **ex-77 · reason-act-observe** — a full reason → act → observe cycle on a multi-step task — verify the
  three phases per step. (co-02)
- **ex-78 · tool-dispatch-typed** — typed tool dispatch, `pyright`-clean — verify the type-checked dispatch.
  (co-04)
- **ex-79 · memory-plus-loop** — a bounded loop carrying step memory — verify prior steps inform later ones.
  (co-10)
- **ex-80 · agentic-capstone** — an agent: typed tools over MCP + a bounded loop + memory + guardrails/human
  checkpoint + an eval suite in CI — verify tool calling and the bounded loop work, MCP connects a tool, a
  guardrail blocks an ungated action, and the eval gates CI on regression. (co-02, co-04, co-19, co-20,
  co-21, co-26)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a small but real agent that completes a multi-step task using typed tools over MCP,
  with a bounded agentic loop, memory, guardrails on consequential tools, and an eval suite that runs
  in CI — proving you can build, constrain, and _measure_ a non-deterministic system.
- **Concepts exercised**: [ ] typed tool/function calling (co-04) [ ] bounded reason-act-observe loop
  (co-02, co-23) [ ] MCP tool connection (co-19) [ ] memory/context management (co-10, co-11) [ ] guardrails +
  human checkpoint (co-20, co-21) [ ] an eval suite in CI (co-25, co-26).
- **Ordered steps**:
  1. `.../learning/capstone/code/tools.py` — typed tools plus function-call parsing/dispatch. Verify
     the model selects and the runtime executes the correct tool; `pyright` clean.
  2. `.../learning/capstone/code/agent.py` — a bounded reason-act-observe loop with a step budget,
     stop condition, and step memory. Verify it completes a multi-step task and halts within the
     budget.
  3. `.../learning/capstone/code/mcp/` + guardrails — connect a tool via MCP and gate a consequential
     action behind validation/a human checkpoint. Verify the dangerous tool cannot fire without the
     checkpoint.
  4. `.../learning/capstone/evals/` — a task dataset + scoring, wired into CI. Verify the eval reports
     a score and fails the pipeline when the agent regresses below the bar.
- **Acceptance criteria**: tool calling and the bounded loop work; MCP connects a tool; guardrails
  block ungated consequential actions; the eval suite scores the agent and gates CI on regression; all
  Python is type-annotated and `pyright`-clean.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Papers & articles**

- **ReAct: Synergizing Reasoning and Acting in Language Models** — Shunyu Yao et al. (2022). The
  foundational paper defining the reason-plus-act loop that underlies most modern agent frameworks.
  <https://arxiv.org/abs/2210.03629>
- **Toolformer: Language Models Can Teach Themselves to Use Tools** — Timo Schick et al. (2023).
  Canonical early paper on LLM tool-use/function-calling. <https://arxiv.org/abs/2302.04761>
- **Reflexion: Language Agents with Verbal Reinforcement Learning** — Noah Shinn et al. (2023).
  Influential paper on self-reflective agent loops that improve via linguistic feedback rather than
  weight updates. <https://arxiv.org/abs/2303.11366>
- **Generative Agents: Interactive Simulacra of Human Behavior** — Joon Sung Park et al. (2023), UIST.
  Widely cited multi-agent simulation paper demonstrating believable agent memory, planning, and
  social behavior. <https://arxiv.org/abs/2304.03442>
- **A Survey on Large Language Model based Autonomous Agents** — Lei Wang et al. (2023). Widely cited
  survey providing a unifying framework across the fast-moving agentic AI literature.
  <https://arxiv.org/abs/2308.11432>

## In which paths

- `interview-ready/software-engineer` — Go deeper · AI & harness engineering — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · AI & harness engineering (marquee build-your-own track) — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 12 · AI & harness engineering (marquee build-your-own track).

> _Content originated in the now-closed FS-SE plan (topic 57); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
