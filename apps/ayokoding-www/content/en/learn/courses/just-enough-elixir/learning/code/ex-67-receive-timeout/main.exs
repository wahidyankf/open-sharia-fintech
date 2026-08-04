# receive timeout: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # receive timeout: this expression makes the Elixir dispatch, transform, or message flow observable.
  :message -> IO.puts("received")
# receive timeout: this expression makes the Elixir dispatch, transform, or message flow observable.
after
  # receive timeout: this expression makes the Elixir dispatch, transform, or message flow observable.
  10 -> IO.puts("timeout")
# receive timeout: this expression makes the Elixir dispatch, transform, or message flow observable.
end
