# atom as tag: this expression exposes the Elixir value or match being learned.
case {:ok, 7} do
  # atom as tag: this expression exposes the Elixir value or match being learned.
  {:ok, value} -> IO.puts("value=#{value}")
  # atom as tag: this expression exposes the Elixir value or match being learned.
  {:error, reason} -> IO.puts("error=#{reason}")
# atom as tag: this expression exposes the Elixir value or match being learned.
end
