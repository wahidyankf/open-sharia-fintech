# Each Task runs concurrently; awaiting preserves result order.
tasks = for n <- 1..3, do: Task.async(fn -> Process.sleep(10); n * n end)
results = Enum.map(tasks, &Task.await/1)
if results != [1, 4, 9], do: raise("missing task result")
IO.inspect(results, label: "parallel results")
