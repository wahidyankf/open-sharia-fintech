# enum map: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(Enum.map([1, 2, 3], fn value -> value * value end))
