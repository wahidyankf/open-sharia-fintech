# Agent owns a small mutable state without exposing its process loop.
{:ok, counter} = Agent.start_link(fn -> 0 end)
IO.inspect(Agent.get(counter, & &1), label: "initial")
