# destructure tuple: this expression exposes the Elixir value or match being learned.
{status, value, count} = {:ok, "v", 42}
# destructure tuple: this expression exposes the Elixir value or match being learned.
IO.inspect({status, value, count})
