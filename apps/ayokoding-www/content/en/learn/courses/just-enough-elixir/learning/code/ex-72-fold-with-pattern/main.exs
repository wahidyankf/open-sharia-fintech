# fold with pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Fold do
  # fold with pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
  def sum(items), do: sum(items, 0)
  # fold with pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
  defp sum([], total), do: total
  # fold with pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
  defp sum([head | tail], total), do: sum(tail, total + head)
# fold with pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# fold with pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(Fold.sum([2, 3, 4]))
