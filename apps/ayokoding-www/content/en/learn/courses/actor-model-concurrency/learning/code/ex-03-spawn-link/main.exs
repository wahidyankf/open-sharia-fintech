# spawn link: this step exposes process identity, mailbox flow, or failure isolation.
parent = self()
# spawn link: this step exposes process identity, mailbox flow, or failure isolation.
spawn(fn ->
  # spawn link: this step exposes process identity, mailbox flow, or failure isolation.
  Process.flag(:trap_exit, true)
  # spawn link: this step exposes process identity, mailbox flow, or failure isolation.
  spawn_link(fn -> exit(:boom) end)
  # spawn link: this step exposes process identity, mailbox flow, or failure isolation.
  receive do {:EXIT, _pid, :boom} -> send(parent, :linked_crash_observed) end
# spawn link: this step exposes process identity, mailbox flow, or failure isolation.
end)
# spawn link: this step exposes process identity, mailbox flow, or failure isolation.
receive do :linked_crash_observed -> IO.puts("spawn_link propagated crash") end
