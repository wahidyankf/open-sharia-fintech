# stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
defmodule CounterLoop do
  # stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
  def loop(total) do
    # stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
    receive do
      # stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
      {:add, value} -> loop(total + value)
      # stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
      {:get, from} -> send(from, {:total, total}); loop(total)
    # stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
    end
  # stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
  end
# stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
end
# stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> CounterLoop.loop(0) end)
# stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, {:add, 3})
# stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, {:get, self()})
# stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:total, total} -> IO.inspect(total) end
