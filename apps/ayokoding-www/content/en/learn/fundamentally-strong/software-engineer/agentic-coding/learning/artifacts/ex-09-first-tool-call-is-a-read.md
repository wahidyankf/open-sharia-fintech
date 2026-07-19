---
title: "Artifact: First Tool Call Is a Read"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 49
---

> A tool-call log whose first logged action is a file read, before any write -- exercises co-07.

```text
1. read_file(path="src/orders/discount.py")
2. read_file(path="tests/test_discount.py")
3. edit_file(path="src/orders/discount.py", diff="+  cap = min(cap, 500)")
4. run_shell(command="pytest tests/test_discount.py -q")
```

**Verify**: entry 1 is `read_file`, and both write-capable entries (`edit_file` at position 3,
`run_shell` at position 4) occur strictly after it in the log -- satisfying ex-09's rule that the
read precedes any write in the tool-call log.
