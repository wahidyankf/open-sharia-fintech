# recursion sum list: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule RecursiveSum do
  # recursion sum list: this expression makes the Elixir dispatch, transform, or message flow observable.
  def sum([]), do: 0
  # recursion sum list: this expression makes the Elixir dispatch, transform, or message flow observable.
  def sum([head | tail]), do: head + sum(tail)
# recursion sum list: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# recursion sum list: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(RecursiveSum.sum([1, 2, 3]))
