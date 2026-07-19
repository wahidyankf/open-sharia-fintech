---
title: "Artifact: MCP-Connected Subagent Research, Summary-Only Return"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 89
---

> A subagent researches a payment provider's webhook-signature verification over MCP; the main
> session receives only a cited summary, never the raw trace -- exercises co-08, co-10.

```text
[Main session]: dispatch_subagent(task="research how PayFlow verifies
webhook signatures, cite the exact header and algorithm")

  --- SUBAGENT'S ISOLATED CONTEXT (NOT visible to the main session -- shown
      here only to illustrate what stays contained) ---
  1. mcp_call(server="payflow-docs", tool="search_docs",
              params={"query": "webhook signature verification"})
     -> JSON-RPC result: {"jsonrpc": "2.0", "id": 1,
        "result": {"pages": ["docs/webhooks/signing.md"]}}
  2. mcp_call(server="payflow-docs", tool="fetch_page",
              params={"path": "docs/webhooks/signing.md"})
     -> JSON-RPC result: {"jsonrpc": "2.0", "id": 2,
        "result": {"content": "...HMAC-SHA256 over the raw body, header
        X-PayFlow-Signature, timestamp tolerance 5 minutes..."}}
  3. (subagent reasons over the fetched page, drafts its summary)
  --- END subagent's isolated context ---

[Main session receives ONLY:]
  Subagent summary: "PayFlow signs webhooks with HMAC-SHA256 over the raw
  request body, sent in the X-PayFlow-Signature header, with a 5-minute
  timestamp tolerance. Source: docs/webhooks/signing.md (PayFlow developer
  docs, fetched via the payflow-docs MCP server)."

[Main session]: proceeds to implement verify_payflow_signature() against
this summary -- it never saw the two mcp_call entries or their JSON-RPC
payloads above; only the final cited sentence entered its context.
```

The two `mcp_call` entries and their raw JSON-RPC results exist only inside the subagent's own,
isolated context -- the main session's actual context window gained one cited sentence, not the
full research trace, exactly matching co-10's "delegate a narrow research task, return a summary"
pattern applied here on top of an MCP-connected tool.

**Verify**: the main session's log contains exactly one entry after the dispatch -- the cited
summary -- with the subagent's `mcp_call` trace and JSON-RPC payloads explicitly marked as never
entering it -- satisfying ex-49's rule that the main session receives only a cited summary.
