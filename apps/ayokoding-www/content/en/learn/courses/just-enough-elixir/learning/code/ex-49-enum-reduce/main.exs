# enum reduce: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(Enum.reduce([1, 2, 3], 0, &+/2))
