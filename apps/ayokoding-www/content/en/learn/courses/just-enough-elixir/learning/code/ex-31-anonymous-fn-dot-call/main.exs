# anonymous fn dot call: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Math do
  # anonymous fn dot call: this expression makes the Elixir dispatch, transform, or message flow observable.
  def add(left, right), do: left + right
# anonymous fn dot call: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# anonymous fn dot call: this expression makes the Elixir dispatch, transform, or message flow observable.
add = fn left, right -> left + right end
# anonymous fn dot call: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({Math.add(1, 2), add.(1, 2)})
