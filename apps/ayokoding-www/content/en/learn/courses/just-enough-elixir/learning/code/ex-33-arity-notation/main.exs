# arity notation: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Arithmetic do
  # arity notation: this expression makes the Elixir dispatch, transform, or message flow observable.
  def sum(left, right), do: left + right
  # arity notation: this expression makes the Elixir dispatch, transform, or message flow observable.
  def sum(left, middle, right), do: left + middle + right
# arity notation: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# arity notation: this expression makes the Elixir dispatch, transform, or message flow observable.
two = &Arithmetic.sum/2
# arity notation: this expression makes the Elixir dispatch, transform, or message flow observable.
three = &Arithmetic.sum/3
# arity notation: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({two.(1, 2), three.(1, 2, 3)})
