defmodule KataSum do
  def sum([]), do: 0
  def sum([head | tail]), do: head + sum(tail)
end
IO.inspect(KataSum.sum([1, 2, 3]), label: "base and step clauses")
