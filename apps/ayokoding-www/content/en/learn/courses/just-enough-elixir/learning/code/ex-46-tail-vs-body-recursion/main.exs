# tail vs body recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Sums do
  # tail vs body recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  def body([]), do: 0
  # tail vs body recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  def body([head | tail]), do: head + body(tail)
  # tail vs body recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  def tail(items), do: tail(items, 0)
  # tail vs body recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  defp tail([], total), do: total
  # tail vs body recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  defp tail([head | rest], total), do: tail(rest, total + head)
# tail vs body recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# tail vs body recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({Sums.body([1, 2, 3]), Sums.tail([1, 2, 3])})
