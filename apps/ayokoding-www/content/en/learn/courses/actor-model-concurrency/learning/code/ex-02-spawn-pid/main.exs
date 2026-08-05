# spawn pid: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> receive do :stop -> :ok end end)
# spawn pid: this step exposes process identity, mailbox flow, or failure isolation.
IO.inspect({is_pid(pid), Process.alive?(pid)})
# spawn pid: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, :stop)
