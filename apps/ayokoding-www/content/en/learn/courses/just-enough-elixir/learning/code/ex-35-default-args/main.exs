# default args: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule DefaultGreeting do
  # default args: this expression makes the Elixir dispatch, transform, or message flow observable.
  def greet(name, greeting \\ "Hi"), do: "#{greeting} #{name}"
# default args: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# default args: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({DefaultGreeting.greet("Ada"), DefaultGreeting.greet("Ada", "Welcome")})
