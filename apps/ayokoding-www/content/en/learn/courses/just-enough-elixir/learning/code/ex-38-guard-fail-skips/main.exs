# guard fail skips: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule StartsWithOne do
  # guard fail skips: this expression makes the Elixir dispatch, transform, or message flow observable.
  def classify(value) when hd(value) == 1, do: :starts_with_one
  # guard fail skips: this expression makes the Elixir dispatch, transform, or message flow observable.
  def classify(_), do: :other
# guard fail skips: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# guard fail skips: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(StartsWithOne.classify([]))
