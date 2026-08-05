# self reply address: this step exposes process identity, mailbox flow, or failure isolation.
parent = self()
# self reply address: this step exposes process identity, mailbox flow, or failure isolation.
worker = spawn(fn -> receive do {:work, from} -> send(from, {:result, parent}) end end)
# self reply address: this step exposes process identity, mailbox flow, or failure isolation.
send(worker, {:work, self()})
# self reply address: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:result, from} -> IO.inspect(from, label: "reply address worked") end
