# string binary: this expression exposes the Elixir value or match being learned.
word = "hé"
# string binary: this expression exposes the Elixir value or match being learned.
IO.inspect({String.length(word), byte_size(word)}, label: "characters and bytes")
