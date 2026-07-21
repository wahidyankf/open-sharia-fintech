# Just Enough C (Primer, C)

**Course ID**: `just-enough-c` · **Format**: Primer · **Language**: C.

**Short summary**: C syntax, pointers, memory, manual management

**Scope note**: **just enough C** to be productive in the OS and systems-programming topics
([`79-linux-os`](./linux-os.md), [`80-windows-os`](./windows-os.md),
[`81-system-programming`](./system-programming.md)). The compiler/`make` toolchain, syntax/types,
a pointers intro, arrays/structs, `stdio`, the preprocessor, and a minimal `Makefile`.

## Why this exists · the big idea

- **The problem before the solution**: the OS and systems topics that follow are written against a machine
  that speaks C — without a working grip on pointers, structs, and the compile/link loop, the memory and
  syscall material is unreadable. C is the just-enough key that unlocks it.
- **Keep-this-if-you-forget-everything**: C is a thin, honest layer over the machine — a pointer is just an
  address, a struct is just laid-out bytes — and almost nothing is hidden from you, which is both its power
  and its danger.
- **Big ideas touched**: `abstraction-and-its-cost` — C buys portability over assembly while hiding almost
  nothing; you manage memory and layout yourself, and the machine leaks through every pointer;
  `taming-state` — manual memory means you own each allocation's lifetime by hand, the discipline the later
  systems topics are built on.

## Prerequisites

- **Prior topics**: [topic 4 Just Enough Python](./just-enough-python.md) (a high-level contrast) and
  [topic 5 Just Enough Bash](./just-enough-bash.md) (compilers, `make`,
  the build loop).
- **Tools & environment**: a macOS/Linux terminal; **gcc/clang** + **make**; Neovim/VSCode with a C LSP
  (DD-17).
- **Assumed knowledge**: variables/functions/loops in some language (topic 04); running CLI tools + a build
  step (topic 05).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified (nuance): **C23 is published as ISO/IEC 9899:2024** (2024-10-31), and **GCC 15
  (~Apr 2025) made `-std=c23`/`gnu23` the default C dialect** — so C23 is now the practical default in
  current GCC. Clang has only **partial** C23 support (`-std=c23` since Clang 18); MSVC lags. The successor
  **C2y** is an early WG14 draft with no release date. Given GCC's default shift, consider leading with C23
  while keeping **C17 as the conservative portability baseline** (esp. vs Clang's partial coverage);
  re-verify Clang C23 completeness at authoring time. (gcc.gnu.org/projects/c-status.html / clang.llvm.org/c_status.html)
- 2026-07-12 — verified: gcc/clang + make toolchain, `Makefile` conventions, and `-Wall -Wextra` are
  evergreen/unchanged.

### DD-35 primary-source citations (fetched-and-read)

Per DD-35, every standard/toolchain claim below traces to a primary source; version-sensitive items are
flagged for re-verification at authoring time.

- **C standard** — `[Verified]` C23 is published as **ISO/IEC 9899:2024** (2024-10-31); the last freely
  published committee draft is **N1570 (C11)** at open-std.org (used for verbatim clause citations since
  ISO charges for the final text). C17 is the conservative portability baseline
  (open-std.org/jtc1/sc22/wg14).
- **Compiler defaults** — `[Verified]` **GCC 15 (~Apr 2025) made `-std=gnu23` the default C dialect**;
  **Clang has only partial C23 support** (`-std=c23` since Clang 18); MSVC lags
  (gcc.gnu.org/projects/c-status.html, clang.llvm.org/c_status.html). **`[Needs Verification]` at
  authoring** — re-check Clang's C23 completeness; keep shipped examples C17-portable unless a C23 feature
  is the point.
- **Toolchain** — `[Verified]` `gcc`/`clang` compile + link; `make` drives builds from a `Makefile`;
  `-Wall -Wextra` enable the standard warning set (gcc.gnu.org/onlinedocs/gcc/Warning-Options.html,
  gnu.org/software/make/manual).
- **Header guards** — `[Verified]` the portable idiom is `#ifndef`/`#define`/`#endif` include guards.
  **`#pragma once` is NON-STANDARD** (not in the ISO C standard) though widely supported by GCC/Clang/MSVC —
  authored content must present it as a common non-standard extension, not a standard feature
  (gcc.gnu.org/onlinedocs/cpp/Once-Only-Headers.html, "supported by many compilers" but not ISO C).
- **stdio / string.h** — `[Verified]` `printf`/`scanf`/`fopen`/`fprintf`/`fclose` (`<stdio.h>`) and
  `strlen`/`strcpy` (`<string.h>`) are standard-library functions (open-std.org N1570 §7.21, §7.24).
- **Dynamic memory** — `[Verified]` `malloc`/`free` (`<stdlib.h>`) are the standard heap primitives; kept at
  intro depth here (open-std.org N1570 §7.22.3). Depth deferred to
  [`81-system-programming`](./system-programming.md).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Primer, subject band). Each example below cites the co-NN it exercises. -->

- **co-01 · gcc-clang** — `gcc`/`clang` compile a C source file into a runnable binary.
- **co-02 · compile-link** — compilation produces object files that the linker combines into an executable.
- **co-03 · make-makefile** — `make` drives a build from a `Makefile` with targets and rules.
- **co-04 · main-and-return** — `main()` is the entry point; its `return` value is the process exit code.
- **co-05 · types** — `int`/`char`/`float`/`double` are the core scalar types.
- **co-06 · variables-scope** — variables have a declaration, a type, and a block/file scope.
- **co-07 · operators** — arithmetic, comparison, logical, and bitwise operators combine values.
- **co-08 · control-flow** — `if`/`else`, `switch`, and `for`/`while` loops direct execution.
- **co-09 · functions** — functions take parameters, return a value, and may need a forward prototype.
- **co-10 · pointers-intro** — a pointer holds an address; `&` takes an address, `*` declares/dereferences.
- **co-11 · pointer-deref** — dereferencing a pointer reads or writes the pointed-to object.
- **co-12 · arrays** — arrays store fixed-length contiguous elements accessed by index.
- **co-13 · array-pointer-decay** — an array passed to a function decays to a pointer to its first element.
- **co-14 · strings** — C strings are null-terminated `char` arrays manipulated via `<string.h>`.
- **co-15 · structs** — a `struct` groups named members into one aggregate type.
- **co-16 · struct-pointers** — a struct pointer accesses members with `->`.
- **co-17 · stdio-printf** — `printf` formats output with `%d`/`%s`/`%f` specifiers.
- **co-18 · stdio-scanf** — `scanf` reads formatted input.
- **co-19 · file-io** — `fopen`/`fprintf`/`fscanf`/`fclose` do file I/O.
- **co-20 · preprocessor-include** — `#include` pulls in header declarations.
- **co-21 · preprocessor-define** — `#define` defines constants and function-like macros; `#ifdef` conditionally compiles.
- **co-22 · header-guards** — `#ifndef`/`#define`/`#endif` include guards prevent double inclusion (`#pragma once` is a common non-standard alternative).
- **co-23 · multi-file** — a program splits declarations into `.h` headers and definitions into `.c` files linked together.
- **co-24 · malloc-free** — `malloc`/`free` allocate and release heap memory (intro).
- **co-25 · const-sizeof** — `const` marks immutability; `sizeof` reports a type's byte size.
- **co-26 · compiler-warnings** — `-Wall -Wextra` surface warnings; clean builds are the goal.

## Worked examples

Colocated under `just-enough-c/learning/code/`; each built via gcc/clang + make (DD-20/DD-30). Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · gcc-compile** — `gcc hello.c -o hello` — verify a binary is produced. (co-01)
- **ex-02 · run-binary** — run `./hello` — verify output. (co-01)
- **ex-03 · clang-compile** — `clang hello.c` — verify it also compiles. (co-01)
- **ex-04 · main-return** — `main` returns 0 — verify the exit code. (co-04)
- **ex-05 · int-var** — declare an `int` + print it — verify the value. (co-05)
- **ex-06 · char-var** — a `char` + print — verify the value. (co-05)
- **ex-07 · float-double** — `float`/`double` — verify precision. (co-05)
- **ex-08 · arithmetic** — arithmetic operators — verify results. (co-07)
- **ex-09 · comparison-logical** — comparison + logical operators — verify booleans. (co-07)
- **ex-10 · bitwise** — bitwise `& | ^ << >>` — verify results. (co-07)
- **ex-11 · if-else** — an `if`/`else` branch — verify selection. (co-08)
- **ex-12 · switch** — a `switch` — verify case dispatch. (co-08)
- **ex-13 · for-loop** — a `for` loop — verify iteration. (co-08)
- **ex-14 · while-loop** — a `while` loop — verify iteration. (co-08)
- **ex-15 · function-def** — a function + call — verify the return. (co-09)
- **ex-16 · function-prototype** — a forward prototype — verify it compiles. (co-09)
- **ex-17 · printf-format** — `printf` with `%d`/`%s`/`%f` — verify formatting. (co-17)
- **ex-18 · scanf-input** — `scanf` reads an int — verify the value. (co-18)
- **ex-19 · scope-block** — a block-scoped variable — verify scope. (co-06)
- **ex-20 · sizeof** — `sizeof(int)`/`sizeof(struct)` — verify sizes. (co-25)
- **ex-21 · const** — a `const` variable — verify it can't be reassigned. (co-25)
- **ex-22 · array-declare** — an int array + indexing — verify elements. (co-12)
- **ex-23 · array-loop** — iterate an array — verify traversal. (co-12, co-08)
- **ex-24 · string-literal** — a `char[]` string + `printf %s` — verify output. (co-14)
- **ex-25 · include-stdio** — `#include <stdio.h>` — verify `printf` resolves. (co-20)
- **ex-26 · define-const** — `#define` a constant — verify substitution. (co-21)

### Intermediate

- **ex-27 · pointer-address** — take `&x` — verify the address prints. (co-10)
- **ex-28 · pointer-declare** — `int *p = &x` — verify it holds the address. (co-10)
- **ex-29 · deref-read** — read `*p` — verify it equals `x`. (co-11)
- **ex-30 · deref-write** — write `*p = 5` — verify `x` changes. (co-11)
- **ex-31 · pointer-function** — pass a pointer to a function to mutate — verify the caller sees the change. (co-11, co-09)
- **ex-32 · null-pointer** — a `NULL` pointer check — verify guarded access. (co-10)
- **ex-33 · array-decay** — pass an array to a function (decays to a pointer) — verify element access. (co-13)
- **ex-34 · pointer-arithmetic** — `*(a+i)` equals `a[i]` — verify equivalence. (co-13, co-10)
- **ex-35 · string-length** — walk a `char*` to the null terminator — verify the length. (co-14)
- **ex-36 · string-h** — `strlen`/`strcpy` from `<string.h>` — verify results. (co-14, co-20)
- **ex-37 · struct-define** — a `struct` + member access — verify fields. (co-15)
- **ex-38 · struct-init** — initialize a struct — verify values. (co-15)
- **ex-39 · struct-function** — pass a struct to a function — verify it's copied. (co-15, co-09)
- **ex-40 · struct-pointer** — a struct pointer + `->` — verify member access. (co-16)
- **ex-41 · struct-pointer-mutate** — mutate via a struct pointer — verify the caller sees it. (co-16, co-11)
- **ex-42 · array-of-structs** — an array of structs — verify iteration. (co-15, co-12)
- **ex-43 · fopen-write** — `fopen` + `fprintf` a file — verify contents. (co-19)
- **ex-44 · fopen-read** — `fopen` + `fscanf` a file — verify parsed values. (co-19)
- **ex-45 · fclose** — `fclose` after I/O — verify the file is flushed. (co-19)
- **ex-46 · printf-specifiers** — `%x`/`%p`/`%c` specifiers — verify formatting. (co-17)
- **ex-47 · multiple-args** — a function with several args — verify the computation. (co-09)
- **ex-48 · recursion** — a recursive function (factorial) — verify the result. (co-09)
- **ex-49 · define-macro** — a function-like `#define` macro — verify expansion. (co-21)
- **ex-50 · header-file** — declare in a `.h`, define in a `.c` — verify it links. (co-23, co-20)
- **ex-51 · header-guard** — an `#ifndef` include guard — verify no double-include error. (co-22)
- **ex-52 · pragma-once** — `#pragma once` (non-standard but widely supported) — verify single inclusion. (co-22)
- **ex-53 · two-file-compile** — compile two `.c` files + link — verify one binary. (co-02, co-23)
- **ex-54 · warnings-clean** — compile with `-Wall -Wextra` — verify no warnings. (co-26)

### Advanced

- **ex-55 · malloc-basic** — `malloc` an int + use it — verify the value. (co-24)
- **ex-56 · malloc-array** — `malloc` a dynamic array — verify indexing. (co-24, co-12)
- **ex-57 · free-memory** — `free` after use — verify no leak (sanitizer/valgrind intuition). (co-24)
- **ex-58 · malloc-struct** — `malloc` a struct + `->` — verify fields. (co-24, co-16)
- **ex-59 · pointer-to-pointer** — an `int **` — verify double dereference. (co-10, co-11)
- **ex-60 · array-of-pointers** — a `char*[]` of strings — verify iteration. (co-13, co-14)
- **ex-61 · struct-linked** — a struct with a self-pointer (a linked node) — verify traversal. (co-16, co-24)
- **ex-62 · makefile-basic** — a `Makefile` with a build target — verify `make` builds. (co-03)
- **ex-63 · makefile-clean** — a `clean` target — verify `make clean` removes artifacts. (co-03)
- **ex-64 · makefile-vars** — Makefile variables (`CC`/`CFLAGS`) — verify they apply. (co-03)
- **ex-65 · makefile-multi** — a Makefile compiling multiple objects — verify an incremental build. (co-03, co-02)
- **ex-66 · object-files** — compile to `.o` then link — verify the two-step build. (co-02)
- **ex-67 · extern-declaration** — an `extern` variable across files — verify linkage. (co-23)
- **ex-68 · conditional-compile** — `#ifdef`/`#endif` — verify conditional inclusion. (co-21)
- **ex-69 · sizeof-struct-layout** — `sizeof` a struct (with padding) — verify the size. (co-25, co-15)
- **ex-70 · stdin-loop** — read stdin in a loop until EOF — verify processing. (co-18)
- **ex-71 · file-round-trip** — write then read a file back — verify the round-trip. (co-19)
- **ex-72 · string-parse** — parse a string into fields — verify the tokens. (co-14)
- **ex-73 · warning-fix** — fix a `-Wextra` warning — verify a clean build. (co-26)
- **ex-74 · const-pointer** — a `const char *` — verify immutability. (co-25, co-10)
- **ex-75 · multi-file-struct** — a struct shared across files via a header — verify it links + runs. (co-23, co-15)
- **ex-76 · makefile-warnings** — a Makefile with `-Wall -Wextra` in `CFLAGS` — verify warning-clean. (co-03, co-26)
- **ex-77 · integration-pointer-struct-slice** — a Makefile-built program using structs, pointers, and `malloc` — verify end-to-end. (co-24, co-16, co-11, co-03)
- **ex-78 · capstone-multifile-c** — a multi-file C program driven by a `Makefile`: header + two sources, structs, pointers, `stdio`, preprocessor, compiled warning-clean — verify `make` builds, `make clean` cleans, and output is correct. (co-03, co-10, co-12, co-15, co-17, co-20, co-22, co-23, co-26)

## Capstone spec — intra-topic (primer → light consolidation)

- **Goal**: build a small multi-file C program driven by a `Makefile` that exercises the primer's surface —
  pointers, arrays, structs, `stdio`, headers, and the preprocessor — compiling cleanly with warnings on,
  proving readiness for the OS/systems topics.
- **Concepts exercised**: [ ] a `Makefile`-driven multi-file build (co-03, co-23) [ ] pointers + arrays
  (co-10, co-12) [ ] structs (co-15) [ ] `stdio` I/O (co-17) [ ] headers + the preprocessor (co-20, co-22).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a program split across a header + two source files using structs +
     pointers + `stdio`. Verify it compiles warning-clean (`-Wall -Wextra`).
  2. `Makefile` — build + clean targets. Verify `make` produces the binary and `make clean` removes
     artifacts.
  3. Run it on sample input. Verify the output matches the expected result.
- **Acceptance criteria**: the multi-file build works via `make`; pointers/structs/`stdio` behave; the
  program compiles warning-clean and produces correct output.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **The C Programming Language**, 2nd ed. — Brian W. Kernighan & Dennis M. Ritchie (1988, Prentice Hall). "K&R" — the field-defining, canonical primer for C, updated for ANSI C.
- **Expert C Programming: Deep C Secrets** — Peter van der Linden (1994, Prentice Hall). The classic deep-dive into C idioms, quirks, and compiler/linker internals.

**Papers & articles**

- **ISO/IEC 9899:2011 (C11)**, public committee draft N1570 — ISO/IEC JTC1/SC22/WG14 (2011). The definitive language standard; N1570 is the last public draft, freely published by the standards committee itself. <https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Theory & low-level systems — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · CS fundamentals, DS&A & algorithms — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 1 · CS theory & foundations (the university core, taught first).

> _Content originated in the now-closed FS-SE plan (topic 78); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
