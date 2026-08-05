# recursion base case: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Factorial do
  # recursion base case: this expression makes the Elixir dispatch, transform, or message flow observable.
  def value(0), do: 1
  # recursion base case: this expression makes the Elixir dispatch, transform, or message flow observable.
  def value(number), do: number * value(number - 1)
# recursion base case: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# recursion base case: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(Factorial.value(5))
