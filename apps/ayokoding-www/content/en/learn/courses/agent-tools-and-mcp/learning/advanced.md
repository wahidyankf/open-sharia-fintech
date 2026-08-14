---
title: "Advanced Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 30
---

These advanced examples keep browser and provider integration simulated locally. `remotebrowser` is an
illustrative service shape only, never a dependency.

### Example 35: Build a Browser MCP Server

**Brief explanation**: Wrap a local browser-shaped service as a named MCP tool.

**Code**: Run `python3 code/ex-35-browser-mcp-server/example.py`.

**Expected observation**: The server advertises `navigate`.

**Key takeaway**: A service becomes portable through a tool contract.

**Why it matters**: Clients should not receive a raw browser object.

### Example 36: Drive a Browser through MCP

**Brief explanation**: The loop calls a discovered browser capability.

**Code**: Run `python3 code/ex-36-agent-drives-browser-over-mcp/example.py`.

**Expected observation**: The local task returns a title.

**Key takeaway**: The loop owns dispatch, while MCP owns discovery.

**Why it matters**: This seam keeps an adapter replaceable.

### Example 37: Compose Filesystem, Shell, and Browser Servers

**Brief explanation**: A client composes separately namespaced capabilities.

**Code**: Run `python3 code/ex-37-compose-fs-shell-browser/example.py`.

**Expected observation**: Three local results remain distinct.

**Key takeaway**: Composition does not erase authority boundaries.

**Why it matters**: Mixed providers need clear ownership.

### Example 38: Bound a Browser-Shaped Pool

**Brief explanation**: A bounded pool limits concurrent simulated browser work.

**Code**: Run `python3 code/ex-38-remotebrowser-shaped-pool/example.py`.

**Expected observation**: At most two tasks hold capacity.

**Key takeaway**: Concurrency must be bounded at the provider.

**Why it matters**: A client surge must not create unlimited targets.

### Example 39: Enforce a Tool Permission Boundary

**Brief explanation**: A provider denies an unapproved action before dispatch.

**Code**: Run `python3 code/ex-39-tool-permission-boundary/example.py`.

**Expected observation**: A denied tool returns `DENIED`.

**Key takeaway**: Connection is not permission.

**Why it matters**: Tool authority requires explicit policy.

### Example 40: Stream a Tool Result

**Brief explanation**: A long result can arrive as ordered chunks.

**Code**: Run `python3 code/ex-40-streaming-tool-result/example.py`.

**Expected observation**: Chunks combine into one result.

**Key takeaway**: Streaming preserves result ordering.

**Why it matters**: Clients can render useful progress early.

### Example 41: Assemble a Robust Tool Suite

**Brief explanation**: Validation, bounds, and errors are combined around a local tool.

**Code**: Run `python3 code/ex-41-robust-tool-suite/example.py`.

**Expected observation**: Invalid input returns a typed error.

**Key takeaway**: Reliability is a boundary property.

**Why it matters**: Hostile inputs must not bypass basic controls.

### Example 42: Migrate a Schema Evolution

**Brief explanation**: An adapter accepts an old call and writes the current shape.

**Code**: Run `python3 code/ex-42-schema-evolution-migration/example.py`.

**Expected observation**: Version one becomes version two.

**Key takeaway**: Migrations make evolution intentional.

**Why it matters**: Tool consumers update independently.

### Example 43: Generate a Capability Manifest

**Brief explanation**: A manifest summarizes connected server capabilities.

**Code**: Run `python3 code/ex-43-capability-manifest/example.py`.

**Expected observation**: The manifest includes every provider tool.

**Key takeaway**: Discovery can produce reviewable metadata.

**Why it matters**: Operators need a visible capability surface.

### Example 44: Record Tool Usage Analytics

**Brief explanation**: Count calls by tool name without logging sensitive arguments.

**Code**: Run `python3 code/ex-44-tool-usage-analytics/example.py`.

**Expected observation**: The counter records two `search` calls.

**Key takeaway**: Usage data should be minimal and purposeful.

**Why it matters**: Measurements inform tool-surface design.

### Example 45: Model Sandboxed Tool Execution

**Brief explanation**: A local tool receives an isolated workspace label.

**Code**: Run `python3 code/ex-45-sandboxed-tool-execution/example.py`.

**Expected observation**: The operation reports the sandbox boundary.

**Key takeaway**: Execution location is part of the contract.

**Why it matters**: Isolation limits damage from a mistaken call.

### Example 46: Share a Server Across Agents

**Brief explanation**: Two callers preserve their own correlation ids through one provider.

**Code**: Run `python3 code/ex-46-multi-agent-shared-server/example.py`.

**Expected observation**: Both caller ids remain separate.

**Key takeaway**: Shared infrastructure needs correlation.

**Why it matters**: Cross-talk makes actions and audits unreliable.

### Example 47: Review a Tool API Design

**Brief explanation**: Replace a vague broad tool with focused readable operations.

**Code**: Run `python3 code/ex-47-design-review-a-tool-api/example.py`.

**Expected observation**: The revised surface has explicit names.

**Key takeaway**: Design reviews improve selection and authority clarity.

**Why it matters**: Tool APIs are model-facing product interfaces.

### Example 48: Use a Portable Tool Across Agents

**Brief explanation**: Two loops invoke the same server contract.

**Code**: Run `python3 code/ex-48-portable-tool-across-agents/example.py`.

**Expected observation**: Both loops get the same result.

**Key takeaway**: Protocol contracts outlive a particular agent implementation.

**Why it matters**: Providers should not be tied to one harness.

### Example 49: Complete an End-to-End MCP Agent Task

**Brief explanation**: Discovery, validation, calls, and result composition complete a local goal.

**Code**: Run `python3 code/ex-49-end-to-end-mcp-agent/example.py`.

**Expected observation**: The task returns `done`.

**Key takeaway**: Safe composition remains small and inspectable.

**Why it matters**: A capstone trace reveals missing boundaries.

### Example 50: Measure Tool-Count Degradation

**Brief explanation**: A learner-owned suite measures lower selection scores for larger advertised sets.

**Code**: Run `python3 code/ex-50-tool-count-degradation-curve/example.py`.

**Expected observation**: Scores decline from 5 to 19 to 46 tools.

**Key takeaway**: Tool-count is a measurable design constraint.

**Why it matters**: A registry should be sized to the task, not to maximum possibility.

### Example 51: Filter Tools per Turn

**Brief explanation**: Advertise the relevant subset instead of the whole registry.

**Code**: Run `python3 code/ex-51-filter-tools-per-turn/example.py`.

**Expected observation**: Filtering leaves only the task-relevant tool.

**Key takeaway**: Discovery can be contextual.

**Why it matters**: A smaller surface improves selection conditions.

### Example 52: Split a Tool Surface Across Subagents

**Brief explanation**: Specialists receive their own small provider surfaces.

**Code**: Run `python3 code/ex-52-split-tool-surface-across-subagents/example.py`.

**Expected observation**: Each agent receives two tools rather than four.

**Key takeaway**: Partitioning reduces each selector's burden.

**Why it matters**: Capability growth need not become one giant prompt.

### Example 53: Trim a Tool Result

**Brief explanation**: Return the fields needed for the next decision, not the full service payload.

**Code**: Run `python3 code/ex-53-trim-a-tool-result/example.py`.

**Expected observation**: The compact result omits unneeded metadata.

**Key takeaway**: Token efficiency is a recurring context decision.

**Why it matters**: Every later turn re-reads retained results.

### Example 54: Build a Capstone Tool Provider

**Brief explanation**: A compact provider unifies tools, resources, prompts, validation, and filtering.

**Code**: Run `python3 code/ex-54-capstone-tool-provider/example.py`.

**Expected observation**: A discovered allowed tool completes the local task.

**Key takeaway**: A complete provider is a set of small enforceable contracts.

**Why it matters**: The agent should use only capabilities the server explicitly exposes.
