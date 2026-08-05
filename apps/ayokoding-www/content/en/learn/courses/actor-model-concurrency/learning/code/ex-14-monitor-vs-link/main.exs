# monitor vs link: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> exit(:boom) end)
# monitor vs link: this step exposes process identity, mailbox flow, or failure isolation.
ref = Process.monitor(pid)
# monitor vs link: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:DOWN, ^ref, :process, ^pid, :boom} -> IO.puts("monitor survived target crash") end
