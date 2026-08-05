# stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
defmodule StoreLoop do
  # stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
  def loop(value) do
    # stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
    receive do
      # stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
      {:set, next} -> loop(next)
      # stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
      {:get, from} -> send(from, {:value, value}); loop(value)
    # stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
    end
  # stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
  end
# stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
end
# stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> StoreLoop.loop(:old) end)
# stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, {:set, :new})
# stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, {:get, self()})
# stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:value, value} -> IO.inspect(value) end
