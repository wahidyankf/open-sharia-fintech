# process isolation: this step exposes process identity, mailbox flow, or failure isolation.
parent_state = :intact
# process isolation: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> exit(:boom) end)
# process isolation: this step exposes process identity, mailbox flow, or failure isolation.
ref = Process.monitor(pid)
# process isolation: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:DOWN, ^ref, :process, ^pid, :boom} -> IO.inspect(parent_state) end
