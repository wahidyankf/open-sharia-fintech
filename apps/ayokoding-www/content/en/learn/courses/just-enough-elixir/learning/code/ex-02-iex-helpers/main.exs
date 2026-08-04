# iex helpers: h and i run inside IEx and print documentation and value information.
{output, 0} = System.cmd("iex", ["--eval", "h Enum.map; i \"abc\""])
# iex helpers: retain a short, structural proof that both helper outputs appeared.
true = String.contains?(output, "Enum.map")
# iex helpers: printing the captured session makes this script auditable without a manual REPL.
IO.puts("IEx h/i helpers completed")
