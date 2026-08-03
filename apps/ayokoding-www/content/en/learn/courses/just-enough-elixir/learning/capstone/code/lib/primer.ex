# capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
defmodule Primer do
  # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
  def transform(items), do: items |> Enum.map(&(&1 * 2)) |> Enum.filter(&(&1 > 2))

  # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
  def total(items), do: total(items, 0)
  # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
  defp total([], sum), do: sum
  # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
  defp total([head | tail], sum), do: total(tail, sum + head)

  # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
  def round_trip(value) do
    # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
    parent = self()
    # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
    spawn(fn -> send(parent, {:reply, value}) end)

    # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
    receive do
      # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
      {:reply, result} ->
        result

        # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
    end

    # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
  end

  # capstone: this line contributes to the immutable pipeline, recursion, or process hand-off.
end
