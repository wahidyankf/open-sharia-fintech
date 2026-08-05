# send receive roundtrip: this step exposes process identity, mailbox flow, or failure isolation.
parent = self()
# send receive roundtrip: this step exposes process identity, mailbox flow, or failure isolation.
worker = spawn(fn -> receive do {:ping, from} -> send(from, {:pong, parent}) end end)
# send receive roundtrip: this step exposes process identity, mailbox flow, or failure isolation.
send(worker, {:ping, self()})
# send receive roundtrip: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:pong, from} -> IO.inspect(from, label: "round trip") end
