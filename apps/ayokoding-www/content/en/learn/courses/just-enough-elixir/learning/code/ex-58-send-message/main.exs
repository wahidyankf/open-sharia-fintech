# send message: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# send message: this expression makes the Elixir dispatch, transform, or message flow observable.
pid = spawn(fn -> receive do message -> send(parent, {:delivered, message}) end end)
# send message: this expression makes the Elixir dispatch, transform, or message flow observable.
send(pid, {:hello, self()})
# send message: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # send message: this expression makes the Elixir dispatch, transform, or message flow observable.
  {:delivered, message} -> IO.inspect(message)
# send message: this expression makes the Elixir dispatch, transform, or message flow observable.
end
