# self pid: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(self(), label: "current pid")
