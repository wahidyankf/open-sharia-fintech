# stateful loop basic: this step exposes process identity, mailbox flow, or failure isolation.
defmodule ValueLoop do
  # stateful loop basic: this step exposes process identity, mailbox flow, or failure isolation.
  def loop(value) do
    # stateful loop basic: this step exposes process identity, mailbox flow, or failure isolation.
    receive do {:get, from} -> send(from, {:value, value}); loop(value) end
  # stateful loop basic: this step exposes process identity, mailbox flow, or failure isolation.
  end
# stateful loop basic: this step exposes process identity, mailbox flow, or failure isolation.
end
# stateful loop basic: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> ValueLoop.loop("saved") end)
# stateful loop basic: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, {:get, self()})
# stateful loop basic: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:value, value} -> IO.inspect(value) end
