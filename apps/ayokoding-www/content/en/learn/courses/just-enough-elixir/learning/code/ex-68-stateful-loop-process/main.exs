# stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Counter do
  # stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
  def loop(total) do
    # stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
    receive do
      # stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
      {:add, number} -> loop(total + number)
      # stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
      {:get, from} -> send(from, {:total, total}); loop(total)
      # stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
      :stop -> :ok
    # stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
    end
  # stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
  end
# stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
pid = spawn(fn -> Counter.loop(0) end)
# stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
send(pid, {:add, 3})
# stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
send(pid, {:get, self()})
# stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do {:total, total} -> IO.inspect(total) end
# stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
send(pid, :stop)
