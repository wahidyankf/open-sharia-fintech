# Updates run inside the Agent process, so callers do not share the integer directly.
{:ok, counter} = Agent.start_link(fn -> 0 end)
Agent.update(counter, &(&1 + 1))
IO.inspect(Agent.get(counter, & &1), label: "after update")
