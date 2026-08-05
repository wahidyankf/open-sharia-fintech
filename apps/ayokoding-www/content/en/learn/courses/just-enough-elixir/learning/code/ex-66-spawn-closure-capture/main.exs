# spawn closure capture: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# spawn closure capture: this expression makes the Elixir dispatch, transform, or message flow observable.
value = 42
# spawn closure capture: this expression makes the Elixir dispatch, transform, or message flow observable.
spawn(fn -> send(parent, {:captured, value}) end)
# spawn closure capture: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # spawn closure capture: this expression makes the Elixir dispatch, transform, or message flow observable.
  {:captured, captured} -> IO.inspect(captured)
# spawn closure capture: this expression makes the Elixir dispatch, transform, or message flow observable.
end
