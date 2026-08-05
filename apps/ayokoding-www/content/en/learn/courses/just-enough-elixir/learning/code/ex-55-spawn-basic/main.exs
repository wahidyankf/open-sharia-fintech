# spawn basic: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# spawn basic: this expression makes the Elixir dispatch, transform, or message flow observable.
spawn(fn -> send(parent, :ran) end)
# spawn basic: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # spawn basic: this expression makes the Elixir dispatch, transform, or message flow observable.
  :ran -> IO.puts("spawned process ran")
# spawn basic: this expression makes the Elixir dispatch, transform, or message flow observable.
end
