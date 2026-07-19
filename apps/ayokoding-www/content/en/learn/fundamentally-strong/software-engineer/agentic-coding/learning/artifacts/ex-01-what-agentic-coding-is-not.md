---
title: "Artifact: Autocomplete vs. Agent Session Tool-Call Log"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 41
---

> Autocomplete single-shot suggestion vs. a multi-step agent session on the same task -- exercises
> co-01.

```text
Autocomplete (single-shot, no tool use)
----------------------------------------
Editor cursor sits inside calculator.py, at the end of an empty function body.
Autocomplete suggests, in one shot, with no tool call:
    return a + b
The suggestion is accepted or rejected. Nothing else happens -- no other file
is read, no test is run, no command executes.

Agent session (multiple tool invocations)
------------------------------------------
Task given: "add input validation to add_positive() and cover it with a test."
1. read_file(path="calculator.py")
2. edit_file(path="calculator.py",
              diff="+  if a < 0 or b < 0:\n+      raise ValueError('inputs must be non-negative')")
3. edit_file(path="tests/test_calculator.py",
              diff="+  def test_add_positive_rejects_negative():\n+      with pytest.raises(ValueError):\n+          add_positive(-1, 2)")
4. run_shell(command="pytest tests/test_calculator.py -q")
5. read_file(path="pytest output")   # => reads back "1 passed" before considering the task done
```

**Verify**: the agent session's tool-call log lists five entries (`read_file`, `edit_file` x2,
`run_shell`, `read_file`); the autocomplete case lists zero tool invocations -- satisfying ex-01's
rule that the session log shows multiple tool invocations the autocomplete case never has.
