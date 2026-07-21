# Just Enough Lua (Primer, Lua)

**Course ID**: `just-enough-lua` · **Format**: Primer · **Language**: Lua.

**Short summary**: Lua fundamentals as Neovim's scripting language

**Scope note**: just enough Lua to be productive configuring and extending Neovim in
[`03-extending-neovim`](./extending-neovim.md); **not** full mastery. Lua is the `†` language
exception here because it is the config language of the editor the whole book is built around. All
tooling is OSS (Lua is MIT-licensed) — Tier-1 per DD-21.

## Why this exists · the big idea

- **The problem before the solution**: [`03`](./extending-neovim.md) configures Neovim in Lua; learning
  the config language and the editor-extension concept at once doubles the difficulty — so get just-enough
  Lua first (DD-13).
- **Keep-this-if-you-forget-everything**: in Lua a single structure — the **table** — is array, map,
  object, and module at once; master the table and the rest of the language is small.
- **Big ideas touched**: `abstraction-and-its-cost` — one universal abstraction (the table) buys a tiny,
  learnable language and charges you the specialized types a bigger language would give.

## Prerequisites

- **Prior topics**: [topic 1 Just Enough Nvim](./just-enough-nvim.md) (to edit and run files
  comfortably).
- **Tools & environment**: a macOS/Linux terminal; the standalone **`lua`** interpreter installed
  (`lua -v`) for running scripts outside Neovim.
- **Assumed knowledge**: basic terminal use; no prior programming language required (this is a first
  language for some readers).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28). Re-confirm version pins at authoring.

- 2026-07-12 — verified (CORRECTION): PUC-Lua's current major is now **5.5.0** (2025-12-22), superseding
  the 5.4 line (latest 5.4.x patch 5.4.8). Neovim still embeds **LuaJIT 2.1** (Lua-5.1 semantics), so the
  "LuaJIT vs PUC-Lua" gap is now 5.1-vs-5.5 — widen the version note in Items accordingly. (lua.org)
- 2026-07-12 — verified: Lua remains **MIT**-licensed; Neovim bundles it as MIT (Tier-1, DD-21). (lua.org)
- 2026-07-12 — verified (stable): the `vim` global + `require` semantics match current embedded Lua; no
  change found.
- 2026-07-14 — re-confirmed at authoring time (Phase 2 V step): all four fast-moving claims above
  (Lua 5.5.0/2025-12-22 current major, 5.4.8 latest 5.4.x patch, MIT license, Neovim's Lua-5.1/LuaJIT-2.1
  targeting, LuaJIT's rolling-release-only status) re-checked against `lua.org/versions.html`,
  `lua.org/news.html`, `lua.org/license.html`, `runtime/doc/lua.txt` on `github.com/neovim/neovim`, and
  `luajit.org/status.html` — no change, all still current.

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to a primary source fetched and read in the retroactive grounding sweep
> (2026-07-12, `web-researcher`). Sources: `lua.org` (manual, PIL, versions/license/news), `luajit.org`,
> and Neovim's `runtime/doc`/`runtime/lua` source on `github.com/neovim/neovim`.

- **Versions + license** — [lua.org/versions.html](https://www.lua.org/versions.html) and
  [news.html](https://www.lua.org/news.html): **Lua 5.5.0** released **2025-12-22** (current major),
  **5.4.8** (2025-06-04) latest 5.4 patch. License **MIT**, verbatim from
  [lua.org/license.html](https://www.lua.org/license.html) ("Lua is free software distributed under the
  terms of the MIT license"). Fast-moving — re-confirm at authoring.
- **Neovim embeds LuaJIT 2.1 / Lua 5.1 (co-18)** —
  [`runtime/doc/lua.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/lua.txt):
  verbatim "Lua 5.1 is the permanent interface for Nvim Lua … later versions … are not supported" and
  "built with LuaJIT or a compatible fork … for performance reasons"; LuaJIT bundled MIT per
  [LICENSE.txt](https://raw.githubusercontent.com/neovim/neovim/master/LICENSE.txt). "LuaJIT 2.1" is
  correctly evergreen — [luajit.org/status.html](https://luajit.org/status.html) has no numbered stable
  release (rolling v2.1 branch).
- **Eight basic types (co-01)** — [Lua 5.4 Reference Manual §2.1](https://www.lua.org/manual/5.4/manual.html#2.1):
  verbatim "There are eight basic types in Lua: nil, boolean, number, string, function, userdata, thread,
  and table."
- **Tables, closures, metatables, patterns (co-03/04/07/10/11/16)** —
  [PIL 7.3](https://www.lua.org/pil/7.3.html) (`ipairs` contiguous integer keys vs `pairs`/`next` arbitrary
  order), [PIL 13](https://www.lua.org/pil/13.html) (metatables, `setmetatable`, `__add`),
  [PIL 8.1](https://www.lua.org/pil/8.1.html) (`require` caching), [PIL 20.2](https://www.lua.org/pil/20.2.html)
  (Lua pattern classes `%a`/`%d`/`%w`/`%s`; `string.format` is C-`printf`-style) — all confirmed.
- **co-18 5.1-vs-later dialect gaps** — `unpack` global in 5.1 → `table.unpack` in 5.2
  ([PIL 5.1](https://www.lua.org/pil/5.1.html); [neovim/neovim#30928](https://github.com/neovim/neovim/issues/30928));
  `//` floor-division and `&`/`|`/`~`/`<<`/`>>` bitwise operators are 5.3+ only
  ([Lua 5.3 readme "Main changes"](https://www.lua.org/manual/5.3/readme.html)); LuaJIT `bit` module +
  `goto`/`::label::` unconditionally enabled as 5.2 extensions
  ([luajit.org/extensions.html](https://luajit.org/extensions.html)) — all confirmed.
- **`vim.*` API (ex-78..ex-84)** —
  [`runtime/doc/lua.txt`](https://raw.githubusercontent.com/neovim/neovim/master/runtime/doc/lua.txt) and
  `runtime/lua/vim/shared.lua`/`keymap.lua`: `vim.tbl_deep_extend` (behavior `error`/`keep`/`force`, list
  tables opaque), `vim.tbl_map`, `vim.keymap.set('n', lhs, fn, opts)`, `vim.opt`/`vim.o.tabstop`,
  `vim.api.nvim_buf_set_lines`/`get_lines` (0-based, end-exclusive, `-1`=last), `vim.inspect`, and
  `vim.split` with `trimempty` defaulting to `false` — all confirmed. The `desc` opts field in
  `vim.keymap.set` (ex-80) is real and standard (flows to `nvim_set_keymap`) but marked
  `[Needs Verification]` at the byte-exact-quote level.
- **Read more citations** — _Programming in Lua_ 4th ed. (2016, targets Lua 5.3; free 1st edition online) per
  [lua.org/pil](https://www.lua.org/pil/); _Lua 5.4 Reference Manual_ (Ierusalimschy/de Figueiredo/Celes) —
  kept deliberately at 5.4 as the pedagogically-closer reference to Neovim's Lua-5.1 runtime, though 5.5 is
  now current ([lua.org/manual/5.4](https://www.lua.org/manual/5.4/manual.html)); "Lua — An Extensible
  Extension Language" (_Software: Practice & Experience_ 26(6), 1996, 635–652,
  [lua.org/spe.html](https://www.lua.org/spe.html)); "The Evolution of Lua" (HOPL III, 2007,
  [lua.org/doc/hopl.pdf](https://www.lua.org/doc/hopl.pdf)) — all confirmed.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 8 (Primer). Each example below cites the co-NN it exercises. -->

- **co-01 · dynamic-typing-eight-types** — Lua values carry types at runtime, not variables; every value is
  one of exactly eight types (`nil`, `boolean`, `number`, `string`, `function`, `userdata`, `thread`,
  `table`), checkable with `type()`.
- **co-02 · nil-and-false-are-falsy** — In a Lua condition only `nil` and `false` are false; every other
  value, including `0` and `""`, is truthy.
- **co-03 · tables-are-the-only-data-structure** — Tables are Lua's single structured type, used to build
  arrays, records/maps, sets, queues, and objects.
- **co-04 · array-part-vs-hash-part** — A table with contiguous integer keys from 1 forms a "sequence" walked
  by `ipairs`/`#`, while arbitrary keys form the hash part walked by `pairs`; mixing both is legal but the
  two views diverge.
- **co-05 · functions-are-first-class-values** — Functions are ordinary values that can be assigned to
  variables/table fields, passed as arguments, and returned from other functions.
- **co-06 · lexical-scope-and-local** — Variables are global unless declared `local`; `local` creates a
  lexically scoped binding visible only in the enclosing block and functions nested inside it.
- **co-07 · closures-and-upvalues** — A nested function that references a `local` from an enclosing scope
  keeps that variable alive as an upvalue after the outer function returns, forming a closure.
- **co-08 · multiple-return-values** — A Lua function can return more than one value; the count actually used
  is adjusted by call context (single assignment slot, middle of an argument list, or parentheses truncate
  to one).
- **co-09 · varargs-and-select** — A function declared with a trailing `...` parameter accepts a variable
  number of arguments, retrievable via `...` or counted/indexed with `select`.
- **co-10 · metatables-and-metamethods** — `setmetatable` attaches a metatable of metamethod entries
  (`__index`, `__newindex`, `__add`, `__call`, `__tostring`, `__eq`, etc.) that customize a table's
  behavior under indexing and operators.
- **co-11 · index-metamethod-prototype-oop** — The `__index` metamethod (as a table or a function) redirects
  failed field lookups to another table, and is the mechanism Lua uses to emulate classes and
  prototype-style inheritance.
- **co-12 · colon-syntax-for-methods** — `obj:method(args)` is sugar for `obj.method(obj, args)`; a function
  defined as `function T:method() … end` implicitly receives `self` as its first parameter.
- **co-13 · error-handling-with-pcall** — `error()` raises a Lua error (any value, not just a string);
  `pcall`/`xpcall` call a function in protected mode and convert a raised error into a `false, err` pair;
  `assert` raises when its first argument is falsy.
- **co-14 · modules-and-require** — `require(name)` searches `package.path` for a `name.lua` file, runs it
  once, caches the value it returns in `package.loaded[name]`, and returns that cached value on every
  subsequent call.
- **co-15 · coroutines-cooperative-multitasking** — `coroutine.create/resume/yield/wrap` implement
  cooperative threads that only switch at explicit `yield`/`resume` points, unlike preemptive OS threads.
- **co-16 · string-library-and-patterns** — The `string` library's `find`/`match`/`gmatch`/`gsub` use Lua
  patterns, a lightweight non-POSIX matching dialect distinct from full regular expressions; `string.format`
  follows C `printf`-style specifiers.
- **co-17 · standard-libraries-overview** — Core Lua 5.1 functionality beyond the language itself is
  organized into library tables: `string`, `table`, `math`, `os`, `io`, `coroutine`, `package`, and `debug`.
- **co-18 · luajit-and-lua51-in-neovim** — Neovim embeds a Lua 5.1-compatible interpreter (LuaJIT by
  default), so config Lua targets 5.1 semantics — global `unpack` (not `table.unpack`), no `//`
  integer-division and no `&`/`|`/`~`/`<<`/`>>` bitwise-operator _syntax_ (Lua 5.3+ only) — with LuaJIT's
  `bit` module as the bitwise fallback. Note `goto`/`::label::` _is_ available: LuaJIT enables it
  unconditionally as a Lua 5.2 extension.

## Worked examples

Colocated under `just-enough-lua/learning/code/`; each a complete runnable `.lua` script run with
`lua <file>` (DD-20, DD-30 — full listing on the page, exact command, expected output shown). Each cites the
`co-NN` it exercises. Contiguous `ex-01..ex-84`.

### Beginner

- **ex-01 · hello-world-print** — call `print("Hello, world!")` — verify output `Hello, world!`. (co-17)
- **ex-02 · type-function-eight-types** — `type()` on `nil, true, 1, "s", {}, print` — verify prints
  `nil boolean number string table function`. (co-01)
- **ex-03 · nil-vs-false-truthiness** — `if 0 then … end` and `if "" then … end` both run their body —
  verify both branches execute, proving only `nil`/`false` are falsy. (co-02)
- **ex-04 · local-vs-global-shadowing** — global `x=10`, then `do local x=20 print(x) end print(x)` — verify
  prints `20` then `10`. (co-06)
- **ex-05 · multiple-assignment-swap** — `local a,b=1,2; a,b=b,a; print(a,b)` — verify prints `2 1`. (co-08)
- **ex-06 · arithmetic-operators-modulo-power** — `print(7 % 3, 2^10, -5)` — verify prints `1 1024 -5`.
  (co-17)
- **ex-07 · math-library-floor-random** — `print(math.floor(3.7), math.huge > 1e300)` — verify prints
  `3 true`. (co-17)
- **ex-08 · string-concatenation-coercion** — `print("Value: " .. 42)` — verify prints `Value: 42`. (co-16)
- **ex-09 · string-length-operator** — `print(#"hello")` — verify prints `5`. (co-16)
- **ex-10 · comparison-operators** — `print(1 == 1.0, "a" < "b", 1 ~= 2)` — verify prints `true true true`.
  (co-01)
- **ex-11 · logical-or-default-idiom** — `local x=nil; print(x or "default")` — verify prints `default`.
  (co-02)
- **ex-12 · logical-and-or-ternary-idiom** — `local ok=true; print(ok and "yes" or "no")` — verify prints
  `yes`. (co-02)
- **ex-13 · not-operator-truthiness** — `print(not nil, not false, not 0)` — verify prints
  `true true false`. (co-02)
- **ex-14 · if-elseif-else-branching** — a grade classifier over a score with `if/elseif/else` — verify the
  correct branch's string is printed for a sample score. (co-02)
- **ex-15 · numeric-for-loop-ascending** — `for i=1,5 do io.write(i," ") end` — verify prints `1 2 3 4 5`
  followed by a trailing space. (co-17)
- **ex-16 · numeric-for-loop-descending-step** — `for i=10,1,-2 do io.write(i," ") end` — verify prints
  `10 8 6 4 2` followed by a trailing space. (co-17)
- **ex-17 · while-loop-counter** — `local n=0 while n<3 do n=n+1 end print(n)` — verify prints `3`. (co-17)
- **ex-18 · repeat-until-loop** — `local n=0 repeat n=n+1 until n>=3 print(n)` — verify prints `3` and runs
  its body at least once even when the condition starts true. (co-17)
- **ex-19 · table-array-literal-and-length** — `local t={10,20,30} print(t[1], t[3], #t)` — verify prints
  `10 30 3`. (co-03, co-04)
- **ex-20 · table-map-literal-and-field-access** — `local t={name="Ada", age=36} print(t.name, t["age"])` —
  verify prints `Ada 36`. (co-03)
- **ex-21 · table-nested-field-access** — `local t={a={b={c=42}}} print(t.a.b.c)` — verify prints `42`.
  (co-03)
- **ex-22 · ipairs-iteration-array** — `for i,v in ipairs({"x","y","z"}) do print(i,v) end` — verify prints
  `1 x`, `2 y`, `3 z` in order. (co-04)
- **ex-23 · pairs-iteration-map** — `for k,v in pairs({a=1,b=2}) do print(k,v) end` — verify both `a 1` and
  `b 2` are printed (order unspecified). (co-04)
- **ex-24 · function-basic-definition-call** — `local function add(a,b) return a+b end print(add(2,3))` —
  verify prints `5`. (co-05)
- **ex-25 · function-default-parameter-idiom** — `local function greet(name) name=name or "world" return
"Hello "..name end print(greet())` — verify prints `Hello world`. (co-02, co-05)
- **ex-26 · function-multiple-return-values** — `local function minmax(a,b) if a<b then return a,b else
return b,a end end local lo,hi=minmax(5,2) print(lo,hi)` — verify prints `2 5`. (co-08)

### Intermediate

- **ex-27 · varargs-basic-sum** — `local function sum(...) local s=0 for _,v in ipairs({...}) do s=s+v end
return s end print(sum(1,2,3))` — verify prints `6`. (co-09)
- **ex-28 · varargs-select-count** — `local function count(...) return select('#', ...) end
print(count(1,nil,3))` — verify prints `3`, showing `select('#')` counts a `nil` that `#` on a table would
  miss. (co-09)
- **ex-29 · table-insert-append** — `local t={1,2} table.insert(t,3) print(t[3])` — verify prints `3`. (co-17)
- **ex-30 · table-insert-at-position** — `table.insert(t,1,0) print(t[1])` — verify prints `0` with existing
  elements shifted right. (co-17)
- **ex-31 · table-remove-last** — `local v=table.remove(t) print(v, #t)` — verify the returned value equals
  the prior last element and `#t` drops by one. (co-17)
- **ex-32 · table-remove-at-position** — `table.remove(t,1) print(t[1])` — verify prints the element that was
  previously second. (co-17)
- **ex-33 · table-concat-join** — `print(table.concat({"a","b","c"}, ", "))` — verify prints `a, b, c`.
  (co-17)
- **ex-34 · table-sort-default-order** — `local t={3,1,2} table.sort(t) print(table.concat(t,","))` — verify
  prints `1,2,3`. (co-17)
- **ex-35 · table-sort-custom-comparator** — `table.sort(t, function(a,b) return a>b end)` — verify sorted
  descending, `3,2,1`. (co-05, co-17)
- **ex-36 · string-format-basic-placeholders** — `print(string.format("%s is %d", "age", 36))` — verify
  prints `age is 36`. (co-16)
- **ex-37 · string-format-float-width-precision** — `print(string.format("%5.2f", 3.14159))` — verify prints
  `3.14` right-aligned to width 5 (one leading space), 2 decimals. (co-16)
- **ex-38 · string-sub-substring-range** — `print(string.sub("hello world", 1, 5))` — verify prints `hello`.
  (co-16)
- **ex-39 · string-sub-negative-index-colon-syntax** — `print(("hello"):sub(-3))` — verify prints `llo`,
  demonstrating colon-call on a string literal. (co-12, co-16)
- **ex-40 · string-upper-lower-colon-syntax** — `print(("Neovim"):upper(), ("Neovim"):lower())` — verify
  prints `NEOVIM neovim`. (co-12, co-16)
- **ex-41 · string-rep-repeat** — `print(string.rep("ab", 3))` — verify prints `ababab`. (co-16)
- **ex-42 · string-find-plain-search** — `print(string.find("hello world", "world"))` — verify prints
  `7 11`. (co-16)
- **ex-43 · string-match-pattern-captures** — `print(string.match("key=value", "(%w+)=(%w+)"))` — verify
  prints `key value`. (co-16)
- **ex-44 · string-gmatch-word-iteration** — `for word in string.gmatch("one two three", "%a+") do
io.write(word,"|") end` — verify prints `one|two|three|`. (co-16)
- **ex-45 · string-gsub-substitution-count** — `local s,n=string.gsub("hello world","o","0") print(s,n)` —
  verify prints `hell0 w0rld 2`. (co-16)
- **ex-46 · generic-for-stateless-iterator** — a custom `range(n)` returning an `(f, s, control)` triplet
  used as `for i in range(3) do print(i) end` — verify prints `1`, `2`, `3` with no closure involved.
  (co-05)
- **ex-47 · closures-counter-factory** — `local function makeCounter() local n=0 return function() n=n+1
return n end end local c=makeCounter() print(c(),c(),c())` — verify prints `1 2 3`. (co-07)
- **ex-48 · closures-independent-instances** — two counters built from `makeCounter()` — verify each keeps
  its own separate count; advancing one leaves the other unchanged. (co-07)
- **ex-49 · function-recursion-factorial** — `local function fact(n) if n==0 then return 1 else return
n*fact(n-1) end end print(fact(5))` — verify prints `120`. (co-05)
- **ex-50 · function-as-callback-argument** — `local function apply(f,x) return f(x) end print(apply(function(x)
return x*x end, 5))` — verify prints `25`. (co-05)
- **ex-51 · function-returning-function-adder** — `local function adder(n) return function(x) return x+n end
end local add5=adder(5) print(add5(10))` — verify prints `15`. (co-05, co-07)
- **ex-52 · table-mixed-array-and-map** — `local t={1,2,3,name="mix"} print(#t, t.name)` — verify prints
  `3 mix`. (co-04)
- **ex-53 · metatable-index-function-default** — `setmetatable(t, {__index=function() return "N/A" end})
print(t.missing)` — verify prints `N/A` for any undefined key. (co-10, co-11)
- **ex-54 · metatable-index-table-inheritance** — `setmetatable(t, {__index=defaults})
print(t.inherited_field)` — verify prints the value stored in `defaults`, showing lookup falls through the
  metatable. (co-10, co-11)
- **ex-55 · metatable-tostring-custom-print** — `setmetatable(p, {__tostring=function(p) return
"Point("..p.x..","..p.y..")" end}) print(p)` — verify prints `Point(1,2)`. (co-10)
- **ex-56 · metatable-add-operator-overload** — `Vector.__add=function(a,b) return
Vector.new(a.x+b.x,a.y+b.y) end print((v1+v2).x)` — verify prints the summed `x` component. (co-10)
- **ex-57 · modules-require-return-table-and-caching** — a `mymodule.lua` returning `{greet=function()
return "hi" end}`; `local m1=require("mymodule") local m2=require("mymodule") print(m1.greet(), m1==m2)` —
  verify prints `hi true`, proving `require` caches the module. (co-14)
- **ex-58 · error-raise-with-message-and-pcall** — `local ok,err=pcall(function() error("boom") end)
print(ok, err)` — verify prints `false` plus a message ending in `boom`. (co-13)

### Advanced

- **ex-59 · error-raise-table-object** — `local ok,err=pcall(function() error({code=42}) end)
print(err.code)` — verify prints `42`, showing `error()` can raise any value, not just a string. (co-13)
- **ex-60 · assert-custom-message** — `local ok,err=pcall(function() assert(false,"custom failure") end)
print(err)` — verify prints `custom failure`. (co-13)
- **ex-61 · xpcall-with-traceback-handler** — `xpcall(function() error("oops") end, debug.traceback)` —
  verify the handler's returned string contains `stack traceback`. (co-13, co-17)
- **ex-62 · error-level-suppress-position** — `local ok,err=pcall(function() error("raw", 0) end)
print(err)` — verify prints exactly `raw` with no `file:line:` prefix. (co-13)
- **ex-63 · metatable-eq-operator** — `mt.__eq=function(a,b) return a.id==b.id end` on two distinct table
  objects sharing the same `id` — verify `a==b` prints `true` despite different table identities. (co-10)
- **ex-64 · metatable-call-operator** — `mt.__call=function(self,...) return "called" end setmetatable(t,mt)
print(t(1,2))` — verify prints `called`, showing a table can be invoked like a function. (co-10)
- **ex-65 · oop-class-with-index-metatable** — `Animal={} Animal.__index=Animal function Animal.new(name)
return setmetatable({name=name}, Animal) end function Animal:speak() return self.name.." makes a sound" end
print(Animal.new("Rex"):speak())` — verify prints `Rex makes a sound`. (co-11, co-12)
- **ex-66 · oop-inheritance-chain-setmetatable** — `Dog=setmetatable({}, {__index=Animal}) Dog.__index=Dog`
  then a `Dog` instance calls the inherited `:speak()` — verify prints the unchanged parent message.
  (co-11, co-12)
- **ex-67 · oop-method-override** — `function Dog:speak() return self.name.." barks" end` — verify a `Dog`
  instance prints `barks` while an `Animal` instance still prints the base message. (co-11, co-12)
- **ex-68 · coroutine-create-and-resume** — `co=coroutine.create(function() print("a") coroutine.yield()
print("b") end) coroutine.resume(co) coroutine.resume(co)` — verify prints `a` then `b` across two
  separate resumes. (co-15)
- **ex-69 · coroutine-yield-value-exchange** — `coroutine.yield(x)` and `coroutine.resume(co, y)` passing
  values in both directions — verify the value sent through `resume` is returned from `yield` inside the
  coroutine. (co-15)
- **ex-70 · coroutine-wrap-as-iterator** — `local gen=coroutine.wrap(function() for i=1,3 do
coroutine.yield(i) end end) for v in gen do io.write(v," ") end` — verify prints `1 2 3` followed by a
  trailing space. (co-15)
- **ex-71 · coroutine-status-transitions** — `print(coroutine.status(co))` checked before resuming, from
  inside the coroutine, and after it finishes — verify prints `suspended`, `running`, `dead` respectively.
  (co-15)
- **ex-72 · unpack-global-function-51** — `print(unpack({1,2,3}))` — verify prints `1 2 3` using Lua 5.1's
  global `unpack` rather than the later `table.unpack`. (co-18)
- **ex-73 · string-format-q-escape-quote** — `print(string.format("%q", 'He said "hi"'))` — verify prints an
  escaped, quote-safe literal that the Lua reader could load back unchanged. (co-16)
- **ex-74 · pattern-capture-anchored-date** — `print(string.match("2026-07-12", "^(%d+)-(%d+)-(%d+)$"))` —
  verify prints `2026 07 12`. (co-16)
- **ex-75 · memoized-closure-fibonacci** — a closure wrapping a cache table via upvalue to memoize `fib(n)` —
  verify `fib(30)` returns `832040` without recomputing already-cached calls. (co-07)
- **ex-76 · rawget-rawequal-bypass-metamethods** — `rawget(t,"x")` and `rawequal(a,b)` on tables carrying
  `__index`/`__eq` — verify the raw calls ignore the metamethods, differing from plain `.x`/`==`. (co-10)
- **ex-77 · varargs-table-constructor** — `local function collect(...) return {...} end local
t=collect(1,2,3) print(#t, t[1], t[3])` — verify prints `3 1 3`. (co-09)
- **ex-78 · neovim-vim-tbl-deep-extend-merge** — `:lua print(vim.inspect(vim.tbl_deep_extend("force",
{a=1,b={c=2}}, {b={c=3}})))` — verify output shows `b.c` overridden to `3` while `a` stays `1`. (co-18)
- **ex-79 · neovim-vim-tbl-map-filter** — `:lua print(vim.inspect(vim.tbl_map(function(x) return x*2 end,
{1,2,3})))` — verify `vim.inspect` output shows the doubled values `2, 4, 6`. (co-18)
- **ex-80 · neovim-vim-keymap-set-callback** — `:lua vim.keymap.set('n', '<leader>x', function() print("mapped")
end, {desc="test"})` then trigger the mapping — verify `mapped` appears in `:messages`. (co-18)
- **ex-81 · neovim-vim-opt-scalar-option** — `:lua vim.opt.tabstop = 2` then `:lua print(vim.o.tabstop)` —
  verify prints `2`. (co-18)
- **ex-82 · neovim-vim-api-buf-set-lines** — `:lua vim.api.nvim_buf_set_lines(0,0,-1,false,{"hello","world"})`
  — verify `:lua print(table.concat(vim.api.nvim_buf_get_lines(0,0,-1,false), "|"))` prints `hello|world`.
  (co-18)
- **ex-83 · neovim-vim-inspect-pretty-print** — `:lua print(vim.inspect({1,2,{x=3}}))` — verify output is a
  multi-line, human-readable table representation including the nested `x = 3`. (co-18)
- **ex-84 · neovim-vim-split-string-utility** — `:lua print(vim.inspect(vim.split("a,b,,c", ",")))` — verify
  output shows four elements, with an empty string between `"b"` and `"c"` (default `trimempty=false`).
  (co-18)

## Capstone spec — intra-topic (primer → light consolidation)

- **Goal**: write one small, self-contained Lua program (~60–120 lines) that uses tables, closures, a
  `require`d module, a metatable, and `pcall` error handling **together** — a mini "config-value store"
  the reader recognizes as the shape of Neovim config to come.
- **Concepts exercised**: [ ] tables as records+arrays [ ] `ipairs`/`pairs` [ ] closures capturing state
  [ ] a module returning a function table [ ] `__index` metatable defaulting [ ] `pcall`/`nil, err`.
- **Ordered steps**:
  1. `just-enough-lua/learning/capstone/code/store.lua` — a module returning `{ new = function() … end }`
     where `new()` returns a closure-backed store with `get`/`set`. Verify `lua -e 'require("store")'`
     loads without error.
  2. Add a `defaults` table wired via `setmetatable(store, { __index = defaults })` so missing keys fall
     back. Verify a `get` on an unset key returns the default.
  3. `just-enough-lua/learning/capstone/code/main.lua` — `require("store")`, set/get several keys, and
     wrap a deliberately failing lookup in `pcall`, printing `nil, err` cleanly.
  4. Run `lua main.lua`. Verify stdout matches the documented expected output block exactly.
- **Acceptance criteria**: `lua main.lua` exits 0 and prints the expected lines; the failing path is
  caught by `pcall` (no uncaught error); every listing on the page is complete and runnable as shown.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Programming in Lua** — Roberto Ierusalimschy (4th ed., 2016; Lua 5.3). Official book by the language's chief architect; free first edition online. <https://www.lua.org/pil/>

**Papers & articles**

- **Lua 5.4 Reference Manual** — Ierusalimschy, de Figueiredo, Celes (Lua.org). Canonical spec of syntax, semantics, standard libraries. <https://www.lua.org/manual/5.4/manual.html>
- **"Lua — An Extensible Extension Language"** — Ierusalimschy, de Figueiredo, Celes (1996, Software: Practice and Experience). Original paper on Lua's design as a small embeddable language. <https://www.lua.org/spe.html>
- **"The Evolution of Lua"** — Ierusalimschy, de Figueiredo, Celes (2007, HOPL III). The authors' own design history; context for why Neovim adopted Lua. <https://www.lua.org/doc/hopl.pdf>

## In which paths

- `interview-ready/software-engineer` — Prologue · Editor foundations (skippable for the experienced).
- `immediately-effective/software-engineer` — Stage 1 · Editor & tooling (get set up fast).
- `fundamentally-strong/software-engineer` — Prologue · Editor & reproducible forge (skippable).

> _Content originated in the now-closed FS-SE plan (topic 2); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
