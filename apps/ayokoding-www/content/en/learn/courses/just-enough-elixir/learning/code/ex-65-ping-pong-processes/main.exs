# ping pong processes: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# ping pong processes: this expression makes the Elixir dispatch, transform, or message flow observable.
child = spawn(fn ->
  # ping pong processes: this expression makes the Elixir dispatch, transform, or message flow observable.
  send(parent, :ping)
  # ping pong processes: this expression makes the Elixir dispatch, transform, or message flow observable.
  receive do :pong -> send(parent, :done) end
# ping pong processes: this expression makes the Elixir dispatch, transform, or message flow observable.
end)
# ping pong processes: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do :ping -> send(child, :pong) end
# ping pong processes: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do :done -> IO.puts("ping pong complete") end
