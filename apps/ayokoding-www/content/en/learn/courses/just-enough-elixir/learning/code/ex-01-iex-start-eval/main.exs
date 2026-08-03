# iex start eval: IEx evaluates expressions before returning its captured output.
{output, 0} = System.cmd("iex", ["--eval", "IO.puts(1 + 2); IO.puts(\"hello\")"])
# iex start eval: inspect the real IEx session output rather than imitating a REPL.
IO.write(output)
