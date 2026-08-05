parent=self(); spawn(fn -> send(parent,:ok) end); receive do :ok -> IO.puts("reply") end
