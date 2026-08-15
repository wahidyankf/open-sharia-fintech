---
title: "Beginner Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 10
---

These credential-free examples model the tool and MCP boundary with Python's standard library. The
local protocol shapes are deliberate simulations: a production adapter can use a pinned MCP SDK without
changing the contracts being learned here.

### Example 1: Define a Tool

**Brief explanation**: A tool is a named operation with a model-facing description and typed arguments.

**Code**: Run `python3 code/ex-01-define-a-tool/example.py`.

**Expected observation**: The tool reports its name and required `city` argument.

**Key takeaway**: A schema is the deterministic contract behind a model's choice.

**Why it matters**: A callable without a name, description, and argument shape is difficult to select and
unsafe to dispatch.

### Example 2: Derive a Pydantic-Style Argument Schema

**Brief explanation**: Pydantic can derive a JSON schema from a typed model; this standard-library
simulation keeps the same validation boundary runnable without an external dependency.

**Code**: Run `python3 code/ex-02-pydantic-arg-schema/example.py`.

**Expected observation**: A valid city is accepted and a missing city is rejected.

**Key takeaway**: Deriving schemas from types prevents the handler and advertised contract drifting apart.

**Why it matters**: The server must reject invalid input before an action is attempted.

### Example 3: Compare Good and Bad Descriptions

**Brief explanation**: A description tells a model when a tool applies, so it is part of the interface.

**Code**: Run `python3 code/ex-03-good-vs-bad-description/example.py`.

**Expected observation**: The fake selector prefers the precise weather description.

**Key takeaway**: Descriptions are operational prompts, not decorative documentation.

**Why it matters**: Precise descriptions reduce avoidable wrong-tool calls.

### Example 4: Complete a Function-Calling Round Trip

**Brief explanation**: A model returns a structured name and arguments; the loop executes the handler and
appends a typed result.

**Code**: Run `python3 code/ex-04-function-calling-roundtrip/example.py`.

**Expected observation**: The request becomes a `sum` result of `5`.

**Key takeaway**: Model output proposes an action; deterministic code performs it.

**Why it matters**: Keeping proposal and execution separate makes validation auditable.

### Example 5: Return a Structured Tool Result

**Brief explanation**: A tool result should have stable fields the model can consume rather than prose it
must parse.

**Code**: Run `python3 code/ex-05-structured-tool-result/example.py`.

**Expected observation**: The result contains `ok`, `value`, and `unit` fields.

**Key takeaway**: Result shape is part of the tool contract.

**Why it matters**: Typed results make downstream decisions and failures predictable.

### Example 6: Return a Tool Error Shape

**Brief explanation**: Expected failures should become structured observations instead of uncaught errors.

**Code**: Run `python3 code/ex-06-tool-error-shape/example.py`.

**Expected observation**: Division by zero returns a typed `DIVIDE_BY_ZERO` error.

**Key takeaway**: Errors are data for the loop to reason about.

**Why it matters**: A model can choose a recovery only when it receives a clear error category.

### Example 7: Validate Arguments Before Running

**Brief explanation**: Validate a call against its advertised boundary before the tool can have an effect.

**Code**: Run `python3 code/ex-07-validate-args-before-run/example.py`.

**Expected observation**: An unexpected argument is rejected before the handler runs.

**Key takeaway**: Validation belongs at the executable boundary.

**Why it matters**: Model-generated arguments are untrusted input.

### Example 8: Contrast Tool Granularity

**Brief explanation**: A focused pair of tools makes intent clearer than a single ambiguous do-everything
operation.

**Code**: Run `python3 code/ex-08-tool-granularity-contrast/example.py`.

**Expected observation**: The fake selector chooses `read_note` for a read request.

**Key takeaway**: Tool surfaces should be small but task-shaped.

**Why it matters**: Too-coarse tools hide authority; too-many tools reduce selection accuracy.

### Example 9: Start a Minimal MCP Server

**Brief explanation**: An MCP server advertises capabilities over a protocol boundary. This local registry
models the server without opening a socket.

**Code**: Run `python3 code/ex-09-hello-mcp-server/example.py`.

**Expected observation**: The server advertises one `greet` tool.

**Key takeaway**: An MCP server exposes named capabilities for discovery.

**Why it matters**: Providers can publish a capability once for multiple clients.

### Example 10: Connect an MCP Client

**Brief explanation**: A client asks a server what tools it offers rather than maintaining a private list.

**Code**: Run `python3 code/ex-10-hello-mcp-client/example.py`.

**Expected observation**: The client discovers `greet` from the local server.

**Key takeaway**: Discovery decouples clients from provider implementation details.

**Why it matters**: A new server capability can be visible without editing every agent.

### Example 11: Call an MCP Tool

**Brief explanation**: A client sends a JSON-RPC-shaped request and receives a matching typed response.

**Code**: Run `python3 code/ex-11-call-an-mcp-tool/example.py`.

**Expected observation**: Response id `1` carries the greeting result.

**Key takeaway**: Request ids connect concurrent protocol messages to their results.

**Why it matters**: A client must not mistake an event or another response for its own call.

### Example 12: Model MCP over Standard I/O

**Brief explanation**: Stdio transports line-delimited protocol messages between a local host and server.

**Code**: Run `python3 code/ex-12-mcp-over-stdio/example.py`.

**Expected observation**: A JSON request is encoded and decoded unchanged.

**Key takeaway**: Transport moves messages; it does not change the capability contract.

**Why it matters**: Stdio is a simple local boundary that avoids exposing a network listener.

### Example 13: Expose an MCP Resource

**Brief explanation**: A resource is readable context, not executable authority.

**Code**: Run `python3 code/ex-13-mcp-resource/example.py`.

**Expected observation**: The client reads the local `policy://greeting` resource.

**Key takeaway**: Resources let a server provide data without turning it into a tool.

**Why it matters**: Separating read access from action narrows authority.

### Example 14: Expose an MCP Prompt Template

**Brief explanation**: A parameterized prompt is reusable instruction content supplied by the server.

**Code**: Run `python3 code/ex-14-mcp-prompt-template/example.py`.

**Expected observation**: The template fills `Ada` into a greeting task.

**Key takeaway**: Prompts are reusable templates, not server-side executable actions.

**Why it matters**: A shared template keeps repeated task framing consistent.

### Example 15: Connect MCP to the Agent Loop

**Brief explanation**: The loop can discover an MCP tool, validate the requested call, and append its
observation without coupling to the server implementation.

**Code**: Run `python3 code/ex-15-connect-mcp-to-loop/example.py`.

**Expected observation**: The loop reaches the server and returns `hello, Ada`.

**Key takeaway**: MCP supplies capabilities; the agent loop remains the dispatch owner.

**Why it matters**: This seam permits independently evolved agents and capability providers.

### Example 16: Discover Tools at Startup

**Brief explanation**: An agent builds its usable registry from server discovery instead of a hard-coded
tool list.

**Code**: Run `python3 code/ex-16-tool-discovery-at-startup/example.py`.

**Expected observation**: The startup registry contains the newly advertised `status` tool.

**Key takeaway**: Dynamic discovery keeps the client schema-driven.

**Why it matters**: Adding a server tool should not require a synchronized client release.
