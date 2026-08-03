# is type checks: this expression exposes the Elixir value or match being learned.
IO.inspect({is_integer(1), is_list([]), is_tuple({}), is_binary("text")})
