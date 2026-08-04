# whereis lookup: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> receive do :stop -> :ok end end)
# whereis lookup: this step exposes process identity, mailbox flow, or failure isolation.
true = Process.register(pid, :lookup_worker)
# whereis lookup: this step exposes process identity, mailbox flow, or failure isolation.
IO.inspect(Process.whereis(:lookup_worker) == pid)
# whereis lookup: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, :stop)
