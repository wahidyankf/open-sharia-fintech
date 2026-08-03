# clause order matters: this general clause shadows the later specific clause.
defmodule Order do
  # clause order matters: every argument matches here first.
  def bad(_), do: :general
  # clause order matters: this clause is unreachable because bad/1 already matched.
  def bad(:special), do: :special
  # clause order matters: specific patterns must come before the general fallback.
  def good(:special), do: :special
  # clause order matters: this receives values the specific clause did not match.
  def good(_), do: :general
end
# clause order matters: compare the shadowed and correctly ordered dispatch.
IO.inspect({Order.bad(:special), Order.good(:special)})
