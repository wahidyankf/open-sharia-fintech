# tail call recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule TailLength do
  # tail call recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  def count(items), do: count(items, 0)
  # tail call recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  def count([], total), do: total
  # tail call recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  def count([_ | tail], total), do: count(tail, total + 1)
# tail call recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# tail call recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(TailLength.count(Enum.to_list(1..10_000)))
