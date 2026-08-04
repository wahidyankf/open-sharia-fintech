# private defp: public functions may call a private helper inside their module.
defmodule SecretGreeter do
  # private defp: this public boundary delegates internal formatting.
  def public(name), do: decorate(name)
  # private defp: the helper is deliberately unavailable outside this module.
  defp decorate(name), do: "[#{name}]"
end
# private defp: the public API succeeds.
IO.puts(SecretGreeter.public("Ada"))
# private defp: a dynamic external call proves the private helper is inaccessible.
try do
  apply(SecretGreeter, :decorate, ["Ada"])
rescue
  UndefinedFunctionError -> IO.puts("private helper is inaccessible")
end
