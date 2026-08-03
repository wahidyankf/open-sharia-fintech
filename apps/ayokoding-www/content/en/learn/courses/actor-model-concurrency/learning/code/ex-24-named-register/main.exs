# named register: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> receive do :stop -> :ok end end)
# named register: this step exposes process identity, mailbox flow, or failure isolation.
true = Process.register(pid, :actor_worker)
# named register: this step exposes process identity, mailbox flow, or failure isolation.
IO.inspect(Process.whereis(:actor_worker) == pid)
# named register: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, :stop)
