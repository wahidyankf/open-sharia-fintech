# tuple literal: this expression exposes the Elixir value or match being learned.
pair = {:ok, 42}
# tuple literal: this expression exposes the Elixir value or match being learned.
IO.inspect({elem(pair, 1), tuple_size(pair)}, label: "element and size")
