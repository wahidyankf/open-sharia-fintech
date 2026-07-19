---
title: "Artifact: MCP Server Config -- Before and After"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 59
---

> Adding an MCP server entry to a project's config -- exercises co-08.

**Before** (project MCP config -- no servers configured yet):

```json
{
  "mcpServers": {}
}
```

**Agent's tool list before this change** (built-in tools only):

```text
read_file, write_file, edit_file, run_shell, grep, glob
```

**After** (a `project-docs` server entry added, naming the command and args that launch it -- the
Host-configuration shape the MCP spec's client-configuration examples use):

```json
{
  "mcpServers": {
    "project-docs": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./docs"]
    }
  }
}
```

**Agent's tool list after restart** (the built-in tools, plus three new ones the `project-docs`
server exposed during MCP's initialization handshake):

```text
read_file, write_file, edit_file, run_shell, grep, glob,
project-docs__list_directory, project-docs__read_file, project-docs__search_files
```
