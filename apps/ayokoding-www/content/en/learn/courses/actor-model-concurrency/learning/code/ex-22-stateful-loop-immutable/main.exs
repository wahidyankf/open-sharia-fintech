# stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
defmodule ImmutableLoop do
  # stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
  def loop(value) do
    # stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
    receive do
      # stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
      {:next, from} -> next = value + 1; send(from, {value, next}); loop(next)
    # stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
    end
  # stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
  end
# stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
end
# stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> ImmutableLoop.loop(0) end)
# stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, {:next, self()})
# stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
receive do values -> IO.inspect(values) end
