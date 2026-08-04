# receive pattern match: this expression makes the Elixir dispatch, transform, or message flow observable.
send(self(), {:add, 2})
# receive pattern match: this expression makes the Elixir dispatch, transform, or message flow observable.
send(self(), {:stop})
# receive pattern match: this expression makes the Elixir dispatch, transform, or message flow observable.
for _ <- 1..2 do
  # receive pattern match: this expression makes the Elixir dispatch, transform, or message flow observable.
  receive do
    # receive pattern match: this expression makes the Elixir dispatch, transform, or message flow observable.
    {:add, number} -> IO.puts("add #{number}")
    # receive pattern match: this expression makes the Elixir dispatch, transform, or message flow observable.
    :stop -> IO.puts("stop")
  # receive pattern match: this expression makes the Elixir dispatch, transform, or message flow observable.
  end
# receive pattern match: this expression makes the Elixir dispatch, transform, or message flow observable.
end
