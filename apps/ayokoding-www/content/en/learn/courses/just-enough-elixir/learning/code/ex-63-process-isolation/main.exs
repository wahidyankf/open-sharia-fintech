# process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
pid = spawn(fn -> exit(:boom) end)
# process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
ref = Process.monitor(pid)
# process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
  {:DOWN, ^ref, :process, ^pid, :boom} -> send(parent, :parent_survived)
# process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
  :parent_survived -> IO.puts("parent survived child crash")
# process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
end
