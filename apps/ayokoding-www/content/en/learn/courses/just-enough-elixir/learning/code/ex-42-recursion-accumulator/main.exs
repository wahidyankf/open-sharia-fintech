# recursion accumulator: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule AccumulatorSum do
  # recursion accumulator: this expression makes the Elixir dispatch, transform, or message flow observable.
  def sum(items), do: sum(items, 0)
  # recursion accumulator: this expression makes the Elixir dispatch, transform, or message flow observable.
  def sum([], total), do: total
  # recursion accumulator: this expression makes the Elixir dispatch, transform, or message flow observable.
  def sum([head | tail], total), do: sum(tail, total + head)
# recursion accumulator: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# recursion accumulator: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(AccumulatorSum.sum([1, 2, 3]))
