# call cross module: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Names do
  # call cross module: this expression makes the Elixir dispatch, transform, or message flow observable.
  def normalize(name), do: String.upcase(name)
# call cross module: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# call cross module: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Welcome do
  # call cross module: this expression makes the Elixir dispatch, transform, or message flow observable.
  def message(name), do: "WELCOME #{Names.normalize(name)}"
# call cross module: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# call cross module: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.puts(Welcome.message("ada"))
