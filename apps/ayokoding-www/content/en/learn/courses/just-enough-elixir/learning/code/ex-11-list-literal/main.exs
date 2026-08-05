# list literal: this expression exposes the Elixir value or match being learned.
items = [1, 2, 3]
# list literal: this expression exposes the Elixir value or match being learned.
IO.inspect({hd(items), tl(items)}, label: "head and tail")
