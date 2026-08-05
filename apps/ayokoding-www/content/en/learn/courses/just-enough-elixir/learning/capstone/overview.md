---
title: "Capstone Work Processor"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

Implement the primer’s immutable pipeline, recursive total, and spawn/send/receive hand-off in code/,
then run mix test.

## Test source

The test is rendered from code/test/primer_test.exs.

```elixir
# capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
defmodule PrimerTest do
  # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
  use ExUnit.Case

  # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
  test "transforms, totals, and round-trips a message" do
    # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
    assert Primer.transform([1, 2, 3]) == [4, 6]
    # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
    assert Primer.total([1, 2, 3]) == 6
    # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
    assert Primer.round_trip(:ok) == :ok
  # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
  end
# capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
end
```
