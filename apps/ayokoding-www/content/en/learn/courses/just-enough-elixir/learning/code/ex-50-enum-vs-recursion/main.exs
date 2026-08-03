# enum vs recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Doubler do
  # enum vs recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  def recursive([]), do: []
  # enum vs recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  def recursive([head | tail]), do: [head * 2 | recursive(tail)]
# enum vs recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# enum vs recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
items = [1, 2, 3]
# enum vs recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({Enum.map(items, &(&1 * 2)), Doubler.recursive(items)})
