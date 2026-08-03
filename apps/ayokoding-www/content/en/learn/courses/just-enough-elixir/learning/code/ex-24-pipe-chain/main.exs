# pipe chain: this expression exposes the Elixir value or match being learned.
result = [1, 2, 3] |> Enum.map(&(&1 * 2)) |> Enum.sum()
# pipe chain: this expression exposes the Elixir value or match being learned.
IO.puts("sum=#{result}")
