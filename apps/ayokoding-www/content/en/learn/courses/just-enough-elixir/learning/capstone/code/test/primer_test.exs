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
