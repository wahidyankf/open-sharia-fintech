# pipe first arg: this expression exposes the Elixir value or match being learned.
explicit = String.replace("a-b", "-", "_")
# pipe first arg: this expression exposes the Elixir value or match being learned.
piped = "a-b" |> String.replace("-", "_")
# pipe first arg: this expression exposes the Elixir value or match being learned.
IO.inspect(explicit == piped, label: "first argument inserted")
