# map reduce pipeline: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect([1, 2, 3] |> Enum.map(&(&1 * 2)) |> Enum.reduce(0, &+/2))
