# send to named: this step exposes process identity, mailbox flow, or failure isolation.
parent = self()
# send to named: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> receive do message -> send(parent, {:received, message}) end end)
# send to named: this step exposes process identity, mailbox flow, or failure isolation.
true = Process.register(pid, :named_receiver)
# send to named: this step exposes process identity, mailbox flow, or failure isolation.
send(:named_receiver, :hello)
# send to named: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:received, :hello} -> IO.puts("named delivery") end
