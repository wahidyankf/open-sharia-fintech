# capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Preview do
  # capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
  def total(items), do: items |> Enum.map(&(&1 * 2)) |> sum()
  # capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
  defp sum([]), do: 0
  # capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
  defp sum([head | tail]), do: head + sum(tail)
# capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
spawn(fn -> send(parent, {:total, Preview.total([1, 2, 3])}) end)
# capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
  {:total, value} -> IO.inspect(value, label: "round trip total")
# capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
end
