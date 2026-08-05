# pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Adder do
  # pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
  def loop(total) do
    # pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
    receive do
      # pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
      {:add, number} -> loop(total + number)
      # pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
      {:get, from} -> send(from, {:total, total})
    # pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
    end
  # pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
  end
# pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
pid = spawn(fn -> Adder.loop(0) end)
# pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
send(pid, {:add, 5})
# pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
send(pid, {:get, self()})
# pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do {:total, total} -> IO.inspect(total) end
