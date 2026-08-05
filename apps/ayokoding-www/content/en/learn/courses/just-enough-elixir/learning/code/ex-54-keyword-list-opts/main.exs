# keyword list opts: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Paint do
  # keyword list opts: this expression makes the Elixir dispatch, transform, or message flow observable.
  def color(options), do: Keyword.fetch!(options, :color)
# keyword list opts: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# keyword list opts: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(Paint.color(color: :red))
