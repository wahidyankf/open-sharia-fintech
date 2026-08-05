parent = self()
spawn(fn -> send(parent, {:result, 42}) end)
receive do
  {:result, value} -> IO.inspect(value, label: "received worker result")
end
