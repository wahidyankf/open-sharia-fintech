# receive block: this expression makes the Elixir dispatch, transform, or message flow observable.
send(self(), {:hello, "Ada"})
# receive block: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # receive block: this expression makes the Elixir dispatch, transform, or message flow observable.
  {:hello, name} -> IO.puts("hello #{name}")
# receive block: this expression makes the Elixir dispatch, transform, or message flow observable.
end
