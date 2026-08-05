# Task.Supervisor owns task lifecycle without linking task failure to this caller.
{:ok, supervisor} = Task.Supervisor.start_link()
task = Task.Supervisor.async_nolink(supervisor, fn -> 6 * 7 end)
if Task.await(task) != 42, do: raise("supervised task failed")
IO.puts("supervised task returned 42")
