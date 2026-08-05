# immutable rebind: this expression exposes the Elixir value or match being learned.
x = 1
# immutable rebind: this expression exposes the Elixir value or match being learned.
first = x
# immutable rebind: this expression exposes the Elixir value or match being learned.
x = 2
# immutable rebind: this expression exposes the Elixir value or match being learned.
IO.inspect({first, x}, label: "old value and rebound name")
