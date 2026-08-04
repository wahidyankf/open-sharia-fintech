# link crash propagates: this step exposes process identity, mailbox flow, or failure isolation.
victim = spawn(fn ->
  # link crash propagates: this step exposes process identity, mailbox flow, or failure isolation.
  child = spawn_link(fn -> exit(:boom) end)
  # link crash propagates: this step exposes process identity, mailbox flow, or failure isolation.
  Process.monitor(child)
  # link crash propagates: this step exposes process identity, mailbox flow, or failure isolation.
  receive do {:DOWN, _ref, :process, _pid, :boom} -> :ok end
# link crash propagates: this step exposes process identity, mailbox flow, or failure isolation.
end)
# link crash propagates: this step exposes process identity, mailbox flow, or failure isolation.
ref = Process.monitor(victim)
# link crash propagates: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:DOWN, ^ref, :process, ^victim, :boom} -> IO.puts("linked parent died too") end
