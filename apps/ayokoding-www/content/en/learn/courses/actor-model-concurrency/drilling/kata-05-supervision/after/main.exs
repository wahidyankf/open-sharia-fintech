{:ok, supervisor} = Supervisor.start_link([], strategy: :one_for_one)
IO.inspect(Process.alive?(supervisor))
Supervisor.stop(supervisor)
