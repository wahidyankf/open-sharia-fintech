# async returns a task handle; await receives its result or raises if it fails.
task = Task.async(fn -> Enum.sum(1..3) end)
IO.inspect(Task.await(task), label: "sum")
