# pipe transform pipeline: this expression makes the Elixir dispatch, transform, or message flow observable.
result = [1, 2, 3] |> Enum.map(&(&1 * 2)) |> Enum.filter(&(&1 > 2)) |> Enum.sum()
# pipe transform pipeline: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(result)
