# match mismatch error: this expression exposes the Elixir value or match being learned.
x = 1
# match mismatch error: this expression exposes the Elixir value or match being learned.
try do
  # match mismatch error: this expression exposes the Elixir value or match being learned.
  2 = x
# match mismatch error: this expression exposes the Elixir value or match being learned.
rescue
  # match mismatch error: this expression exposes the Elixir value or match being learned.
  MatchError -> IO.puts("caught MatchError")
# match mismatch error: this expression exposes the Elixir value or match being learned.
end
