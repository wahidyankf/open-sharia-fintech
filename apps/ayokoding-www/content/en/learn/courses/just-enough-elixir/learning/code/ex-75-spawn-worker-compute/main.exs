# spawn worker compute: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# spawn worker compute: this expression makes the Elixir dispatch, transform, or message flow observable.
spawn(fn -> send(parent, {:result, 6 * 7}) end)
# spawn worker compute: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # spawn worker compute: this expression makes the Elixir dispatch, transform, or message flow observable.
  {:result, value} -> IO.inspect(value)
# spawn worker compute: this expression makes the Elixir dispatch, transform, or message flow observable.
end
