# string word count: this expression makes the Elixir dispatch, transform, or message flow observable.
counts = "red blue red" |> String.split() |> Enum.reduce(%{}, fn word, acc -> Map.update(acc, word, 1, &(&1 + 1)) end)
# string word count: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(counts)
