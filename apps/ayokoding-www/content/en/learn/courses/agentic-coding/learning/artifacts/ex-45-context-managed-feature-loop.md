---
title: "Artifact: Context Scoped to One Subsystem for a Multi-File Feature"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 85
---

> A multi-file feature change scoped to only the notifications subsystem's files, with every diff
> confirmed inside that declared scope -- exercises co-04, co-10.

```text
Scoped context (declared before the session starts):
  src/notifications/**
  tests/notifications/**
(everything else in the repo -- src/orders/, src/auth/, src/billing/, docs/,
etc. -- is deliberately excluded from this session's context, per co-04.)

Session tool-call log:
1. read_file(path="src/notifications/dispatcher.py")
2. read_file(path="src/notifications/templates/order_shipped.txt")
3. read_file(path="tests/notifications/test_dispatcher.py")
4. edit_file(path="src/notifications/dispatcher.py", diff="+  add SMS channel")
5. edit_file(path="src/notifications/templates/order_shipped_sms.txt", diff="+  new template")
6. edit_file(path="tests/notifications/test_dispatcher.py", diff="+  def test_sms_channel(): ...")
7. run_shell(command="pytest tests/notifications/ -q") -> "6 passed"

Diffs touched, full list:
  src/notifications/dispatcher.py
  src/notifications/templates/order_shipped_sms.txt
  tests/notifications/test_dispatcher.py
```

All three edited files fall inside `src/notifications/**` or `tests/notifications/**` -- the two
globs declared as this session's scope. No file under `src/orders/`, `src/auth/`, or
`src/billing/` was ever read or written, even though the feature (adding an SMS channel) could
plausibly have tempted the agent to also touch `src/orders/` for order-status triggers -- keeping
that out of context kept the diff to exactly the subsystem it needed to change.

**Verify**: every entry in the "diffs touched" list is a path under `src/notifications/` or
`tests/notifications/` -- the declared scope -- and no diff anywhere in the log falls outside it --
satisfying ex-45's rule that the agent's diffs touch no file outside the scoped set.
