# immutable transform chain: this expression makes the Elixir dispatch, transform, or message flow observable.
original = %{name: "ada", visits: 0}
# immutable transform chain: this expression makes the Elixir dispatch, transform, or message flow observable.
changed = original |> Map.update!(:name, &String.upcase/1) |> Map.update!(:visits, &(&1 + 1))
# immutable transform chain: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({original, changed})
