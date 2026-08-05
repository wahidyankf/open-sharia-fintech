---
title: "Intermediate Elixir"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 20
---

# Intermediate Elixir

Run every source file with elixir main.exs.

## Example 27: Defmodule Def

_ex-27-defmodule-def · source-matched_

This runnable script is rendered from learning/code/ex-27-defmodule-def/main.exs.

```elixir
# defmodule def: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Greeter do
  # defmodule def: this expression makes the Elixir dispatch, transform, or message flow observable.
  def hello(name), do: "Hello, #{name}"
# defmodule def: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# defmodule def: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.puts(Greeter.hello("Ada"))
```

Run: elixir main.exs.

## Example 28: Private Defp

_ex-28-private-defp · source-matched_

This runnable script is rendered from learning/code/ex-28-private-defp/main.exs.

```elixir
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
```

Run: elixir main.exs.

## Example 29: Call Cross Module

_ex-29-call-cross-module · source-matched_

This runnable script is rendered from learning/code/ex-29-call-cross-module/main.exs.

```elixir
# call cross module: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Names do
  # call cross module: this expression makes the Elixir dispatch, transform, or message flow observable.
  def normalize(name), do: String.upcase(name)
# call cross module: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# call cross module: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Welcome do
  # call cross module: this expression makes the Elixir dispatch, transform, or message flow observable.
  def message(name), do: "WELCOME #{Names.normalize(name)}"
# call cross module: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# call cross module: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.puts(Welcome.message("ada"))
```

Run: elixir main.exs.

## Example 30: Anonymous Fn

_ex-30-anonymous-fn · source-matched_

This runnable script is rendered from learning/code/ex-30-anonymous-fn/main.exs.

```elixir
# anonymous fn: this expression makes the Elixir dispatch, transform, or message flow observable.
add = fn left, right -> left + right end
# anonymous fn: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.puts(add.(1, 2))
```

Run: elixir main.exs.

## Example 31: Anonymous Fn Dot Call

_ex-31-anonymous-fn-dot-call · source-matched_

This runnable script is rendered from learning/code/ex-31-anonymous-fn-dot-call/main.exs.

```elixir
# anonymous fn dot call: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Math do
  # anonymous fn dot call: this expression makes the Elixir dispatch, transform, or message flow observable.
  def add(left, right), do: left + right
# anonymous fn dot call: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# anonymous fn dot call: this expression makes the Elixir dispatch, transform, or message flow observable.
add = fn left, right -> left + right end
# anonymous fn dot call: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({Math.add(1, 2), add.(1, 2)})
```

Run: elixir main.exs.

## Example 32: Capture Operator

_ex-32-capture-operator · source-matched_

This runnable script is rendered from learning/code/ex-32-capture-operator/main.exs.

```elixir
# capture operator: this expression makes the Elixir dispatch, transform, or message flow observable.
double = &(&1 * 2)
# capture operator: this expression makes the Elixir dispatch, transform, or message flow observable.
upcase = &String.upcase/1
# capture operator: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({double.(3), upcase.("hi")})
```

Run: elixir main.exs.

## Example 33: Arity Notation

_ex-33-arity-notation · source-matched_

This runnable script is rendered from learning/code/ex-33-arity-notation/main.exs.

```elixir
# arity notation: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Arithmetic do
  # arity notation: this expression makes the Elixir dispatch, transform, or message flow observable.
  def sum(left, right), do: left + right
  # arity notation: this expression makes the Elixir dispatch, transform, or message flow observable.
  def sum(left, middle, right), do: left + middle + right
# arity notation: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# arity notation: this expression makes the Elixir dispatch, transform, or message flow observable.
two = &Arithmetic.sum/2
# arity notation: this expression makes the Elixir dispatch, transform, or message flow observable.
three = &Arithmetic.sum/3
# arity notation: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({two.(1, 2), three.(1, 2, 3)})
```

Run: elixir main.exs.

## Example 34: Same Name Diff Arity

_ex-34-same-name-diff-arity · source-matched_

This runnable script is rendered from learning/code/ex-34-same-name-diff-arity/main.exs.

```elixir
# same name diff arity: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Greeting do
  # same name diff arity: this expression makes the Elixir dispatch, transform, or message flow observable.
  def greet(name), do: "Hi #{name}"
  # same name diff arity: this expression makes the Elixir dispatch, transform, or message flow observable.
  def greet(name, greeting), do: "#{greeting} #{name}"
# same name diff arity: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# same name diff arity: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({Greeting.greet("Ada"), Greeting.greet("Ada", "Welcome")})
```

Run: elixir main.exs.

## Example 35: Default Args

_ex-35-default-args · source-matched_

This runnable script is rendered from learning/code/ex-35-default-args/main.exs.

```elixir
# default args: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule DefaultGreeting do
  # default args: this expression makes the Elixir dispatch, transform, or message flow observable.
  def greet(name, greeting \\ "Hi"), do: "#{greeting} #{name}"
# default args: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# default args: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({DefaultGreeting.greet("Ada"), DefaultGreeting.greet("Ada", "Welcome")})
```

Run: elixir main.exs.

## Example 36: Guard When

_ex-36-guard-when · source-matched_

This runnable script is rendered from learning/code/ex-36-guard-when/main.exs.

```elixir
# guard when: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Absolute do
  # guard when: this expression makes the Elixir dispatch, transform, or message flow observable.
  def value(number) when number < 0, do: -number
  # guard when: this expression makes the Elixir dispatch, transform, or message flow observable.
  def value(number), do: number
# guard when: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# guard when: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(Absolute.value(-7))
```

Run: elixir main.exs.

## Example 37: Guard Allowed Exprs

_ex-37-guard-allowed-exprs · source-matched_

This runnable script is rendered from learning/code/ex-37-guard-allowed-exprs/main.exs.

```elixir
# guard allowed exprs: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Adult do
  # guard allowed exprs: this expression makes the Elixir dispatch, transform, or message flow observable.
  def classify(age) when is_integer(age) and age >= 18, do: :adult
  # guard allowed exprs: this expression makes the Elixir dispatch, transform, or message flow observable.
  def classify(_), do: :not_adult
# guard allowed exprs: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# guard allowed exprs: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({Adult.classify(21), Adult.classify("21")})
```

Run: elixir main.exs.

## Example 38: Guard Fail Skips

_ex-38-guard-fail-skips · source-matched_

This runnable script is rendered from learning/code/ex-38-guard-fail-skips/main.exs.

```elixir
# guard fail skips: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule StartsWithOne do
  # guard fail skips: this expression makes the Elixir dispatch, transform, or message flow observable.
  def classify(value) when hd(value) == 1, do: :starts_with_one
  # guard fail skips: this expression makes the Elixir dispatch, transform, or message flow observable.
  def classify(_), do: :other
# guard fail skips: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# guard fail skips: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(StartsWithOne.classify([]))
```

Run: elixir main.exs.

## Example 39: Function Clauses Pattern

_ex-39-function-clauses-pattern · source-matched_

This runnable script is rendered from learning/code/ex-39-function-clauses-pattern/main.exs.

```elixir
# function clauses pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Result do
  # function clauses pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
  def describe({:ok, value}), do: "value=#{value}"
  # function clauses pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
  def describe({:error, reason}), do: "error=#{reason}"
# function clauses pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# function clauses pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({Result.describe({:ok, 7}), Result.describe({:error, :missing})})
```

Run: elixir main.exs.

## Example 40: Clause Order Matters

_ex-40-clause-order-matters · source-matched_

This runnable script is rendered from learning/code/ex-40-clause-order-matters/main.exs.

```elixir
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
```

Run: elixir main.exs.

## Example 41: Recursion Sum List

_ex-41-recursion-sum-list · source-matched_

This runnable script is rendered from learning/code/ex-41-recursion-sum-list/main.exs.

```elixir
# recursion sum list: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule RecursiveSum do
  # recursion sum list: this expression makes the Elixir dispatch, transform, or message flow observable.
  def sum([]), do: 0
  # recursion sum list: this expression makes the Elixir dispatch, transform, or message flow observable.
  def sum([head | tail]), do: head + sum(tail)
# recursion sum list: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# recursion sum list: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(RecursiveSum.sum([1, 2, 3]))
```

Run: elixir main.exs.

## Example 42: Recursion Accumulator

_ex-42-recursion-accumulator · source-matched_

This runnable script is rendered from learning/code/ex-42-recursion-accumulator/main.exs.

```elixir
# recursion accumulator: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule AccumulatorSum do
  # recursion accumulator: this expression makes the Elixir dispatch, transform, or message flow observable.
  def sum(items), do: sum(items, 0)
  # recursion accumulator: this expression makes the Elixir dispatch, transform, or message flow observable.
  def sum([], total), do: total
  # recursion accumulator: this expression makes the Elixir dispatch, transform, or message flow observable.
  def sum([head | tail], total), do: sum(tail, total + head)
# recursion accumulator: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# recursion accumulator: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(AccumulatorSum.sum([1, 2, 3]))
```

Run: elixir main.exs.

## Example 43: Recursion Map Manual

_ex-43-recursion-map-manual · source-matched_

This runnable script is rendered from learning/code/ex-43-recursion-map-manual/main.exs.

```elixir
# recursion map manual: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule ManualMap do
  # recursion map manual: this expression makes the Elixir dispatch, transform, or message flow observable.
  def map([], _fun), do: []
  # recursion map manual: this expression makes the Elixir dispatch, transform, or message flow observable.
  def map([head | tail], fun), do: [fun.(head) | map(tail, fun)]
# recursion map manual: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# recursion map manual: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(ManualMap.map([1, 2, 3], &(&1 * 2)))
```

Run: elixir main.exs.

## Example 44: Recursion Base Case

_ex-44-recursion-base-case · source-matched_

This runnable script is rendered from learning/code/ex-44-recursion-base-case/main.exs.

```elixir
# recursion base case: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Factorial do
  # recursion base case: this expression makes the Elixir dispatch, transform, or message flow observable.
  def value(0), do: 1
  # recursion base case: this expression makes the Elixir dispatch, transform, or message flow observable.
  def value(number), do: number * value(number - 1)
# recursion base case: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# recursion base case: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(Factorial.value(5))
```

Run: elixir main.exs.

## Example 45: Tail Call Recursion

_ex-45-tail-call-recursion · source-matched_

This runnable script is rendered from learning/code/ex-45-tail-call-recursion/main.exs.

```elixir
# tail call recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule TailLength do
  # tail call recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  def count(items), do: count(items, 0)
  # tail call recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  def count([], total), do: total
  # tail call recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  def count([_ | tail], total), do: count(tail, total + 1)
# tail call recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# tail call recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(TailLength.count(Enum.to_list(1..10_000)))
```

Run: elixir main.exs.

## Example 46: Tail Vs Body Recursion

_ex-46-tail-vs-body-recursion · source-matched_

This runnable script is rendered from learning/code/ex-46-tail-vs-body-recursion/main.exs.

```elixir
# tail vs body recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Sums do
  # tail vs body recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  def body([]), do: 0
  # tail vs body recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  def body([head | tail]), do: head + body(tail)
  # tail vs body recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  def tail(items), do: tail(items, 0)
  # tail vs body recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  defp tail([], total), do: total
  # tail vs body recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  defp tail([head | rest], total), do: tail(rest, total + head)
# tail vs body recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# tail vs body recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({Sums.body([1, 2, 3]), Sums.tail([1, 2, 3])})
```

Run: elixir main.exs.

## Example 47: Enum Map

_ex-47-enum-map · source-matched_

This runnable script is rendered from learning/code/ex-47-enum-map/main.exs.

```elixir
# enum map: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(Enum.map([1, 2, 3], fn value -> value * value end))
```

Run: elixir main.exs.

## Example 48: Enum Filter

_ex-48-enum-filter · source-matched_

This runnable script is rendered from learning/code/ex-48-enum-filter/main.exs.

```elixir
# enum filter: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(Enum.filter([-1, 0, 2, 3], &(&1 > 0)))
```

Run: elixir main.exs.

## Example 49: Enum Reduce

_ex-49-enum-reduce · source-matched_

This runnable script is rendered from learning/code/ex-49-enum-reduce/main.exs.

```elixir
# enum reduce: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(Enum.reduce([1, 2, 3], 0, &+/2))
```

Run: elixir main.exs.

## Example 50: Enum Vs Recursion

_ex-50-enum-vs-recursion · source-matched_

This runnable script is rendered from learning/code/ex-50-enum-vs-recursion/main.exs.

```elixir
# enum vs recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Doubler do
  # enum vs recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  def recursive([]), do: []
  # enum vs recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
  def recursive([head | tail]), do: [head * 2 | recursive(tail)]
# enum vs recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# enum vs recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
items = [1, 2, 3]
# enum vs recursion: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({Enum.map(items, &(&1 * 2)), Doubler.recursive(items)})
```

Run: elixir main.exs.

## Example 51: String Split

_ex-51-string-split · source-matched_

This runnable script is rendered from learning/code/ex-51-string-split/main.exs.

```elixir
# string split: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(String.split("a,b,c", ","))
```

Run: elixir main.exs.

## Example 52: String Upcase Trim

_ex-52-string-upcase-trim · source-matched_

This runnable script is rendered from learning/code/ex-52-string-upcase-trim/main.exs.

```elixir
# string upcase trim: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect("  hi  " |> String.trim() |> String.upcase())
```

Run: elixir main.exs.

## Example 53: Pipe Enum String

_ex-53-pipe-enum-string · source-matched_

This runnable script is rendered from learning/code/ex-53-pipe-enum-string/main.exs.

```elixir
# pipe enum string: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect("a b c" |> String.split() |> Enum.map(&String.upcase/1))
```

Run: elixir main.exs.

## Example 54: Keyword List Opts

_ex-54-keyword-list-opts · source-matched_

This runnable script is rendered from learning/code/ex-54-keyword-list-opts/main.exs.

```elixir
# keyword list opts: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Paint do
  # keyword list opts: this expression makes the Elixir dispatch, transform, or message flow observable.
  def color(options), do: Keyword.fetch!(options, :color)
# keyword list opts: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# keyword list opts: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(Paint.color(color: :red))
```

Run: elixir main.exs.
