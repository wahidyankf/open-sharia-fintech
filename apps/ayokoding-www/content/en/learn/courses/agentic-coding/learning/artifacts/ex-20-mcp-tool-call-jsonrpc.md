---
title: "Artifact: A Tool Call via MCP -- JSON-RPC Request/Result"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 60
---

> A real JSON-RPC 2.0 request/result pair for one MCP tool call -- exercises co-08.

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/call",
  "params": {
    "name": "project-docs__search_files",
    "arguments": { "query": "retry backoff", "path": "./docs" }
  }
}
```

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "docs/adr/0004-carrier-retry-policy.md: \"CarrierAdapter retries a failed ParcelLink call up to 3 times with exponential backoff (200ms/400ms/800ms) before surfacing an error.\""
      }
    ],
    "isError": false
  }
}
```

The request's `id: 7` and the result's `id: 7` are the same JSON-RPC correlation ID -- how the host
matches an asynchronous result back to the call that triggered it, even with several tool calls in
flight.
