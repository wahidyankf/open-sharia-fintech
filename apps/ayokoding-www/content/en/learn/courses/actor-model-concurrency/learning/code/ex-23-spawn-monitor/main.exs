# spawn monitor: this step exposes process identity, mailbox flow, or failure isolation.
{pid, ref} = spawn_monitor(fn -> exit(:done) end)
# spawn monitor: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:DOWN, ^ref, :process, ^pid, :done} -> IO.puts("pid and ref produced DOWN") end
