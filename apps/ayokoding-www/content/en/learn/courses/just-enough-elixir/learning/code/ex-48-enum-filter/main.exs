# enum filter: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(Enum.filter([-1, 0, 2, 3], &(&1 > 0)))
