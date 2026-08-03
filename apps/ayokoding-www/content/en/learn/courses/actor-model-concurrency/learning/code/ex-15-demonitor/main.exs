# demonitor: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> receive do :stop -> exit(:done) end end)
# demonitor: this step exposes process identity, mailbox flow, or failure isolation.
ref = Process.monitor(pid)
# demonitor: this step exposes process identity, mailbox flow, or failure isolation.
true = Process.demonitor(ref, [:flush])
# demonitor: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, :stop)
# demonitor: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:DOWN, ^ref, :process, ^pid, _} -> raise "unexpected DOWN" after 10 -> IO.puts("no DOWN after demonitor") end
