# send message: this step exposes process identity, mailbox flow, or failure isolation.
parent = self()
# send message: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> receive do message -> send(parent, {:delivered, message}) end end)
# send message: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, {:msg, self()})
# send message: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:delivered, message} -> IO.inspect(message) end
