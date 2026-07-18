---
title: "Artifact: A Deny Rule Scoping Writes to One Subdirectory"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 63
---

> A permission config that blocks an out-of-scope write, logged as denied -- exercises co-11.

```json
{
  "permissions": {
    "allow": ["Edit(carrier_adapter/**)", "Read(**)"],
    "deny": ["Edit(**)", "Write(**)"]
  }
}
```

```text
[agent] attempts: Edit(carrier_adapter/retry.py)
[harness] permission check: matches allow rule "Edit(carrier_adapter/**)" -- ALLOWED

[agent] attempts: Edit(shared_config/database.yml)
[harness] permission check: matches deny rule "Edit(**)"; no allow rule covers this path
[harness] BLOCKED and logged: denied -- Edit(shared_config/database.yml) is outside the
allowed scope carrier_adapter/**
```
