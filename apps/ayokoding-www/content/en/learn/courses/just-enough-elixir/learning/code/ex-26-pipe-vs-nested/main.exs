# pipe vs nested: this expression exposes the Elixir value or match being learned.
nested = String.upcase(String.trim("  hi  "))
# pipe vs nested: this expression exposes the Elixir value or match being learned.
piped = "  hi  " |> String.trim() |> String.upcase()
# pipe vs nested: this expression exposes the Elixir value or match being learned.
IO.inspect({nested, piped, nested == piped})
