# spawn returns pid: this expression makes the Elixir dispatch, transform, or message flow observable.
pid = spawn(fn -> receive do :stop -> :ok end end)
# spawn returns pid: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({is_pid(pid), Process.alive?(pid)})
# spawn returns pid: this expression makes the Elixir dispatch, transform, or message flow observable.
send(pid, :stop)
