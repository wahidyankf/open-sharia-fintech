# guard allowed exprs: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Adult do
  # guard allowed exprs: this expression makes the Elixir dispatch, transform, or message flow observable.
  def classify(age) when is_integer(age) and age >= 18, do: :adult
  # guard allowed exprs: this expression makes the Elixir dispatch, transform, or message flow observable.
  def classify(_), do: :not_adult
# guard allowed exprs: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# guard allowed exprs: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({Adult.classify(21), Adult.classify("21")})
