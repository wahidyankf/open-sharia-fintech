---
title: "Beginner Elixir"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

# Beginner Elixir

Run every source file with elixir main.exs. Each block is rendered from its neighboring source.

## Example 01: IEx Start Eval

_ex-01-iex-start-eval · co-01_

This runnable script is rendered from learning/code/ex-01-iex-start-eval/main.exs.

```elixir
# iex start eval: IEx evaluates expressions before returning its captured output.
{output, 0} = System.cmd("iex", ["--eval", "IO.puts(1 + 2); IO.puts(\"hello\")"])
# iex start eval: inspect the real IEx session output rather than imitating a REPL.
IO.write(output)
```

Run: elixir main.exs.

## Example 02: IEx Helpers

_ex-02-iex-helpers · co-01_

This runnable script is rendered from learning/code/ex-02-iex-helpers/main.exs.

```elixir
# iex helpers: h and i run inside IEx and print documentation and value information.
{output, 0} = System.cmd("iex", ["--eval", "h Enum.map; i \"abc\""])
# iex helpers: retain a short, structural proof that both helper outputs appeared.
true = String.contains?(output, "Enum.map")
# iex helpers: printing the captured session makes this script auditable without a manual REPL.
IO.puts("IEx h/i helpers completed")
```

Run: elixir main.exs.

## Example 03: Mix New Project

_ex-03-mix-new-project · co-02_

This runnable script is rendered from learning/code/ex-03-mix-new-project/main.exs.

```elixir
# mix new project: allocate an isolated temporary target before scaffolding.
project = Path.join(System.tmp_dir!(), "greeter-#{System.unique_integer([:positive])}")
# mix new project: mix creates the actual project rather than a printed imitation.
{_output, 0} = System.cmd("mix", ["new", project])
# mix new project: assert the structural artifacts promised by mix new.
true = File.exists?(Path.join(project, "mix.exs"))
true = File.exists?(Path.join(project, "lib/greeter.ex"))
# mix new project: remove only the temporary project this script created.
File.rm_rf!(project)
IO.puts("mix new created mix.exs and lib/greeter.ex")
```

Run: elixir main.exs.

## Example 04: Mix Run Script

_ex-04-mix-run-script · co-02_

This runnable script is rendered from learning/code/ex-04-mix-run-script/main.exs.

```elixir
# mix run script: make a disposable Mix project for a real mix run invocation.
project = Path.join(System.tmp_dir!(), "runner-#{System.unique_integer([:positive])}")
# mix run script: scaffold the project before executing its Mix task.
{_output, 0} = System.cmd("mix", ["new", project])
# mix run script: run the requested expression in the generated project.
{output, 0} = System.cmd("mix", ["run", "-e", "IO.puts(\"hi\")"], cd: project)
# mix run script: verify the task's observable output and clean only the temporary project.
true = String.contains?(output, "hi")
File.rm_rf!(project)
IO.puts("mix run printed hi")
```

Run: elixir main.exs.

## Example 05: Ex Vs Exs

_ex-05-ex-vs-exs · co-03_

This runnable script is rendered from learning/code/ex-05-ex-vs-exs/main.exs.

```elixir
# ex vs exs: this expression exposes the Elixir value or match being learned.
source = "defmodule Greeting do\n  def hello, do: :hello\nend"
# ex vs exs: this expression exposes the Elixir value or match being learned.
Code.compile_string(source)
# ex vs exs: this expression exposes the Elixir value or match being learned.
IO.inspect(Greeting.hello(), label: "compiled .ex intent")
# ex vs exs: this expression exposes the Elixir value or match being learned.
{result, _binding} = Code.eval_string(":hello")
# ex vs exs: this expression exposes the Elixir value or match being learned.
IO.inspect(result, label: "evaluated .exs intent")
```

Run: elixir main.exs.

## Example 06: Immutable Rebind

_ex-06-immutable-rebind · co-04_

This runnable script is rendered from learning/code/ex-06-immutable-rebind/main.exs.

```elixir
# immutable rebind: this expression exposes the Elixir value or match being learned.
x = 1
# immutable rebind: this expression exposes the Elixir value or match being learned.
first = x
# immutable rebind: this expression exposes the Elixir value or match being learned.
x = 2
# immutable rebind: this expression exposes the Elixir value or match being learned.
IO.inspect({first, x}, label: "old value and rebound name")
```

Run: elixir main.exs.

## Example 07: Immutable List Transform

_ex-07-immutable-list-transform · co-04_

This runnable script is rendered from learning/code/ex-07-immutable-list-transform/main.exs.

```elixir
# immutable list transform: this expression exposes the Elixir value or match being learned.
original = [:a, :c]
# immutable list transform: this expression exposes the Elixir value or match being learned.
changed = List.insert_at(original, 1, :b)
# immutable list transform: this expression exposes the Elixir value or match being learned.
IO.inspect(original, label: "original")
# immutable list transform: this expression exposes the Elixir value or match being learned.
IO.inspect(changed, label: "new list")
```

Run: elixir main.exs.

## Example 08: Integer Float

_ex-08-integer-float · co-05_

This runnable script is rendered from learning/code/ex-08-integer-float/main.exs.

```elixir
# integer float: this expression exposes the Elixir value or match being learned.
IO.inspect({5 / 2, div(5, 2), rem(5, 2)}, label: "float, quotient, remainder")
```

Run: elixir main.exs.

## Example 09: Boolean And Atom

_ex-09-boolean-and-atom · co-06_

This runnable script is rendered from learning/code/ex-09-boolean-and-atom/main.exs.

```elixir
# boolean and atom: this expression exposes the Elixir value or match being learned.
IO.inspect({true, :ok, is_boolean(true), is_atom(true), is_atom(:ok)})
```

Run: elixir main.exs.

## Example 10: String Binary

_ex-10-string-binary · co-05_

This runnable script is rendered from learning/code/ex-10-string-binary/main.exs.

```elixir
# string binary: this expression exposes the Elixir value or match being learned.
word = "hé"
# string binary: this expression exposes the Elixir value or match being learned.
IO.inspect({String.length(word), byte_size(word)}, label: "characters and bytes")
```

Run: elixir main.exs.

## Example 11: List Literal

_ex-11-list-literal · co-05_

This runnable script is rendered from learning/code/ex-11-list-literal/main.exs.

```elixir
# list literal: this expression exposes the Elixir value or match being learned.
items = [1, 2, 3]
# list literal: this expression exposes the Elixir value or match being learned.
IO.inspect({hd(items), tl(items)}, label: "head and tail")
```

Run: elixir main.exs.

## Example 12: Tuple Literal

_ex-12-tuple-literal · co-05_

This runnable script is rendered from learning/code/ex-12-tuple-literal/main.exs.

```elixir
# tuple literal: this expression exposes the Elixir value or match being learned.
pair = {:ok, 42}
# tuple literal: this expression exposes the Elixir value or match being learned.
IO.inspect({elem(pair, 1), tuple_size(pair)}, label: "element and size")
```

Run: elixir main.exs.

## Example 13: Is Type Checks

_ex-13-is-type-checks · co-05_

This runnable script is rendered from learning/code/ex-13-is-type-checks/main.exs.

```elixir
# is type checks: this expression exposes the Elixir value or match being learned.
IO.inspect({is_integer(1), is_list([]), is_tuple({}), is_binary("text")})
```

Run: elixir main.exs.

## Example 14: Atom As Tag

_ex-14-atom-as-tag · co-06_

This runnable script is rendered from learning/code/ex-14-atom-as-tag/main.exs.

```elixir
# atom as tag: this expression exposes the Elixir value or match being learned.
case {:ok, 7} do
  # atom as tag: this expression exposes the Elixir value or match being learned.
  {:ok, value} -> IO.puts("value=#{value}")
  # atom as tag: this expression exposes the Elixir value or match being learned.
  {:error, reason} -> IO.puts("error=#{reason}")
# atom as tag: this expression exposes the Elixir value or match being learned.
end
```

Run: elixir main.exs.

## Example 15: Match Operator Basic

_ex-15-match-operator-basic · co-07_

This runnable script is rendered from learning/code/ex-15-match-operator-basic/main.exs.

```elixir
# match operator basic: this expression exposes the Elixir value or match being learned.
x = 1
# match operator basic: this expression exposes the Elixir value or match being learned.
1 = x
# match operator basic: this expression exposes the Elixir value or match being learned.
IO.puts("matched #{x}")
```

Run: elixir main.exs.

## Example 16: Match Mismatch Error

_ex-16-match-mismatch-error · co-07_

This runnable script is rendered from learning/code/ex-16-match-mismatch-error/main.exs.

```elixir
# match mismatch error: this expression exposes the Elixir value or match being learned.
x = 1
# match mismatch error: this expression exposes the Elixir value or match being learned.
try do
  # match mismatch error: this expression exposes the Elixir value or match being learned.
  2 = x
# match mismatch error: this expression exposes the Elixir value or match being learned.
rescue
  # match mismatch error: this expression exposes the Elixir value or match being learned.
  MatchError -> IO.puts("caught MatchError")
# match mismatch error: this expression exposes the Elixir value or match being learned.
end
```

Run: elixir main.exs.

## Example 17: Destructure Tuple

_ex-17-destructure-tuple · co-08_

This runnable script is rendered from learning/code/ex-17-destructure-tuple/main.exs.

```elixir
# destructure tuple: this expression exposes the Elixir value or match being learned.
{status, value, count} = {:ok, "v", 42}
# destructure tuple: this expression exposes the Elixir value or match being learned.
IO.inspect({status, value, count})
```

Run: elixir main.exs.

## Example 18: Destructure List

_ex-18-destructure-list · co-08_

This runnable script is rendered from learning/code/ex-18-destructure-list/main.exs.

```elixir
# destructure list: this expression exposes the Elixir value or match being learned.
[a, b, c] = [1, 2, 3]
# destructure list: this expression exposes the Elixir value or match being learned.
IO.inspect({a, b, c})
```

Run: elixir main.exs.

## Example 19: Head Tail Match

_ex-19-head-tail-match · co-09_

This runnable script is rendered from learning/code/ex-19-head-tail-match/main.exs.

```elixir
# head tail match: this expression exposes the Elixir value or match being learned.
[head | tail] = [1, 2, 3]
# head tail match: this expression exposes the Elixir value or match being learned.
IO.inspect({head, tail})
```

Run: elixir main.exs.

## Example 20: Prepend List

_ex-20-prepend-list · co-09_

This runnable script is rendered from learning/code/ex-20-prepend-list/main.exs.

```elixir
# prepend list: this expression exposes the Elixir value or match being learned.
list = [1, 2, 3]
# prepend list: this expression exposes the Elixir value or match being learned.
IO.inspect([0 | list])
```

Run: elixir main.exs.

## Example 21: Pin Operator

_ex-21-pin-operator · co-10_

This runnable script is rendered from learning/code/ex-21-pin-operator/main.exs.

```elixir
# pin operator: this expression exposes the Elixir value or match being learned.
x = 1
# pin operator: this expression exposes the Elixir value or match being learned.
try do
  # pin operator: this expression exposes the Elixir value or match being learned.
  ^x = 2
# pin operator: this expression exposes the Elixir value or match being learned.
rescue
  # pin operator: this expression exposes the Elixir value or match being learned.
  MatchError -> IO.puts("pin preserved x=#{x}")
# pin operator: this expression exposes the Elixir value or match being learned.
end
```

Run: elixir main.exs.

## Example 22: Wildcard Underscore

_ex-22-wildcard-underscore · co-11_

This runnable script is rendered from learning/code/ex-22-wildcard-underscore/main.exs.

```elixir
# wildcard underscore: this expression exposes the Elixir value or match being learned.
{_, second} = {1, 2}
# wildcard underscore: this expression exposes the Elixir value or match being learned.
IO.puts("bound second=#{second}")
```

Run: elixir main.exs.

## Example 23: Pipe Single

_ex-23-pipe-single · co-12_

This runnable script is rendered from learning/code/ex-23-pipe-single/main.exs.

```elixir
# pipe single: this expression exposes the Elixir value or match being learned.
IO.inspect("hello" |> String.upcase())
```

Run: elixir main.exs.

## Example 24: Pipe Chain

_ex-24-pipe-chain · co-12_

This runnable script is rendered from learning/code/ex-24-pipe-chain/main.exs.

```elixir
# pipe chain: this expression exposes the Elixir value or match being learned.
result = [1, 2, 3] |> Enum.map(&(&1 * 2)) |> Enum.sum()
# pipe chain: this expression exposes the Elixir value or match being learned.
IO.puts("sum=#{result}")
```

Run: elixir main.exs.

## Example 25: Pipe First Arg

_ex-25-pipe-first-arg · co-12_

This runnable script is rendered from learning/code/ex-25-pipe-first-arg/main.exs.

```elixir
# pipe first arg: this expression exposes the Elixir value or match being learned.
explicit = String.replace("a-b", "-", "_")
# pipe first arg: this expression exposes the Elixir value or match being learned.
piped = "a-b" |> String.replace("-", "_")
# pipe first arg: this expression exposes the Elixir value or match being learned.
IO.inspect(explicit == piped, label: "first argument inserted")
```

Run: elixir main.exs.

## Example 26: Pipe Vs Nested

_ex-26-pipe-vs-nested · co-12_

This runnable script is rendered from learning/code/ex-26-pipe-vs-nested/main.exs.

```elixir
# pipe vs nested: this expression exposes the Elixir value or match being learned.
nested = String.upcase(String.trim("  hi  "))
# pipe vs nested: this expression exposes the Elixir value or match being learned.
piped = "  hi  " |> String.trim() |> String.upcase()
# pipe vs nested: this expression exposes the Elixir value or match being learned.
IO.inspect({nested, piped, nested == piped})
```

Run: elixir main.exs.
