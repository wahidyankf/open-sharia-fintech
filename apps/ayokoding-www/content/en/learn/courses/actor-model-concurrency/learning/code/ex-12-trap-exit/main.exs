# trap exit: this step exposes process identity, mailbox flow, or failure isolation.
Process.flag(:trap_exit, true)
# trap exit: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn_link(fn -> exit(:boom) end)
# trap exit: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:EXIT, ^pid, :boom} -> IO.puts("survived trapped exit") end
