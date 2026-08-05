# spawn link exit signal: this step exposes process identity, mailbox flow, or failure isolation.
Process.flag(:trap_exit, true)
# spawn link exit signal: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn_link(fn -> exit(:boom) end)
# spawn link exit signal: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:EXIT, ^pid, :boom} -> IO.puts("received EXIT signal") end
