# anonymous fn: this expression makes the Elixir dispatch, transform, or message flow observable.
add = fn left, right -> left + right end
# anonymous fn: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.puts(add.(1, 2))
