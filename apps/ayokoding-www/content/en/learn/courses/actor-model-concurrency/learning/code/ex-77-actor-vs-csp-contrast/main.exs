# An actor has an identity and receives messages through its mailbox.
actor =
  spawn(fn ->
    receive do
      {:double, value, caller} -> send(caller, {:doubled, value * 2})
    end
  end)

send(actor, {:double, 21, self()})

actor_result =
  receive do
    {:doubled, value} -> value
  end

# Task.await makes the caller explicitly rendezvous with the concurrent computation.
csp_style_result = Task.async(fn -> 21 * 2 end) |> Task.await()

if actor_result != csp_style_result, do: raise("the two coordination styles disagreed")

IO.puts("actor mailbox and synchronous rendezvous both produced #{actor_result}")
