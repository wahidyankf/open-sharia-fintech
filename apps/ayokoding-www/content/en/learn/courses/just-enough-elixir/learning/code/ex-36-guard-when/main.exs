# guard when: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Absolute do
  # guard when: this expression makes the Elixir dispatch, transform, or message flow observable.
  def value(number) when number < 0, do: -number
  # guard when: this expression makes the Elixir dispatch, transform, or message flow observable.
  def value(number), do: number
# guard when: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# guard when: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(Absolute.value(-7))
