# spawn process: this step exposes process identity, mailbox flow, or failure isolation.
parent = self()
# spawn process: this step exposes process identity, mailbox flow, or failure isolation.
spawn(fn -> send(parent, :ran) end)
# spawn process: this step exposes process identity, mailbox flow, or failure isolation.
receive do :ran -> IO.puts("separate process ran") end
