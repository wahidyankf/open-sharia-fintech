---
title: "Artifact: A Read-Only Allow-List for a Review-Only Session"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 64
---

> A review-only session whose tool schema never exposes an edit/write tool -- exercises co-11.

```json
{
  "permissions": {
    "allow": ["Read(**)", "Grep(**)", "Glob(**)"],
    "deny": ["Edit(**)", "Write(**)", "Bash(**)"]
  }
}
```

```text
[session mode] review-only (read-only allow-list active)
[agent's available tool schema this session]: read_file, grep, glob
  -- edit_file, write_file, run_shell are NOT present in the schema at all

[agent] reads carrier_adapter/retry.py, greps for other retry implementations across the repo
[agent] produces a written review comment -- no edit_file or write_file call is even offered
  as an option by the tool schema for this session
```
