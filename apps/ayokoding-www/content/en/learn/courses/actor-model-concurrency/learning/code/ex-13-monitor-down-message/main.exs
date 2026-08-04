# monitor down message: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> exit(:finished) end)
# monitor down message: this step exposes process identity, mailbox flow, or failure isolation.
ref = Process.monitor(pid)
# monitor down message: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:DOWN, ^ref, :process, ^pid, :finished} -> IO.puts("DOWN arrived") end
