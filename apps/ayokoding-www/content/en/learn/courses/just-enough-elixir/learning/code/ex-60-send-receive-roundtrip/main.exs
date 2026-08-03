# send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
spawn(fn ->
  # send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
  receive do
    # send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
    {:ping, from} -> send(from, {:pong, parent})
  # send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
  end
# send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
end) |> send({:ping, self()})
# send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
  {:pong, from} -> IO.inspect(from, label: "round trip from")
# send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
end
