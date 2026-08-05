# recursion map manual: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule ManualMap do
  # recursion map manual: this expression makes the Elixir dispatch, transform, or message flow observable.
  def map([], _fun), do: []
  # recursion map manual: this expression makes the Elixir dispatch, transform, or message flow observable.
  def map([head | tail], fun), do: [fun.(head) | map(tail, fun)]
# recursion map manual: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# recursion map manual: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(ManualMap.map([1, 2, 3], &(&1 * 2)))
