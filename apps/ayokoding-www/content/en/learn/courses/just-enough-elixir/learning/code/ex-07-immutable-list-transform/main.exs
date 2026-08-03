# immutable list transform: this expression exposes the Elixir value or match being learned.
original = [:a, :c]
# immutable list transform: this expression exposes the Elixir value or match being learned.
changed = List.insert_at(original, 1, :b)
# immutable list transform: this expression exposes the Elixir value or match being learned.
IO.inspect(original, label: "original")
# immutable list transform: this expression exposes the Elixir value or match being learned.
IO.inspect(changed, label: "new list")
