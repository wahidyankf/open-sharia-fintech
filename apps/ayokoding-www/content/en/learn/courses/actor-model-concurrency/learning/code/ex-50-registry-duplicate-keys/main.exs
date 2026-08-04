# Duplicate Registries retain every live process registered under one key.
{:ok, _} = Registry.start_link(keys: :duplicate, name: DuplicateRegistry)
parent = self()

pids =
  for value <- [:a, :b] do
    spawn(fn ->
      {:ok, _} = Registry.register(DuplicateRegistry, :workers, value)
      send(parent, {:registered, value})
      receive do
        :stop -> :ok
      end
    end)
  end

for _ <- 1..2, do: receive(do: ({:registered, _} -> :ok))
values = Registry.lookup(DuplicateRegistry, :workers) |> Enum.map(&elem(&1, 1)) |> Enum.sort()
if values != [:a, :b], do: raise("duplicate registry lost a worker")

IO.puts("duplicate registry found both workers")
Enum.each(pids, &send(&1, :stop))
