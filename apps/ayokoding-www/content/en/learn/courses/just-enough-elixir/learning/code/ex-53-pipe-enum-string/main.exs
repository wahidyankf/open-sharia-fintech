# pipe enum string: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect("a b c" |> String.split() |> Enum.map(&String.upcase/1))
