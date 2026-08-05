# function clauses pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Result do
  # function clauses pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
  def describe({:ok, value}), do: "value=#{value}"
  # function clauses pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
  def describe({:error, reason}), do: "error=#{reason}"
# function clauses pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# function clauses pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({Result.describe({:ok, 7}), Result.describe({:error, :missing})})
