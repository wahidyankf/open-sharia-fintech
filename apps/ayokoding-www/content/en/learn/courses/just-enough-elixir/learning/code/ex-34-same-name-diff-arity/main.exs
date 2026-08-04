# same name diff arity: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Greeting do
  # same name diff arity: this expression makes the Elixir dispatch, transform, or message flow observable.
  def greet(name), do: "Hi #{name}"
  # same name diff arity: this expression makes the Elixir dispatch, transform, or message flow observable.
  def greet(name, greeting), do: "#{greeting} #{name}"
# same name diff arity: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# same name diff arity: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({Greeting.greet("Ada"), Greeting.greet("Ada", "Welcome")})
