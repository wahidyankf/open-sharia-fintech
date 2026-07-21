# System Programming (By Example, C)

**Course ID**: `system-programming` · **Format**: By Example · **Language**: C.

**Short summary**: Memory, files, processes, OS-level programming

**Scope note**: programming close to the metal in C — the memory model (stack/heap/`malloc`/`free`),
undefined behavior & safety, manual resource management (C has no RAII — cleanup is explicit), low-level
data (bits/unions/endianness/serialization), building & linking (the ABI), and interfacing with the OS.
Builds on the OS topics ([`79-linux-os`](./linux-os.md)) and the CS memory foundations
([`19-computer-science-foundations`](./computer-science-foundations.md)).

## Why this exists · the big idea

- **The problem before the solution**: C hands you the machine with no guardrails — no garbage collector,
  no RAII, no bounds checks — so a single mismanaged pointer becomes a use-after-free, a buffer overflow,
  or silent undefined behaviour that ships and corrupts memory in production. This topic is about doing it
  safely, by discipline.
- **Keep-this-if-you-forget-everything**: without RAII, every resource you acquire is one you must
  explicitly release on every path — ownership in C is a discipline you enforce by hand, not a guarantee
  the language gives you.
- **Big ideas touched**: `taming-state` — manual `malloc`/`free`, fd ownership, and by-hand cleanup are a
  discipline for containing mutable resources the language won't manage for you; `layering-and-leaks` —
  linking, the ABI, endianness, and syscalls are where your program meets the layers beneath it, and
  undefined behaviour is the machine leaking through the abstraction.

## Prerequisites

- **Prior topics**: [topic 78 Just Enough C](./just-enough-c.md) (the language),
  [topic 79 Linux OS](./linux-os.md) (syscalls, the process/memory model), and
  [topic 19 Computer Science Foundations](./computer-science-foundations.md) (data representation,
  memory).
- **Tools & environment**: a macOS/Linux terminal; **gcc/clang** + make + **valgrind**/**AddressSanitizer**
  for memory checking; Neovim/VSCode (DD-17).
- **Assumed knowledge**: C pointers/structs + a `make` build (topic 78); the process/memory/syscall model
  (topic 79); binary/number representation (topic 19).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: stack/heap, `malloc`/`free`, alignment, UB categories (buffer overflow,
  use-after-free, integer overflow), ASan (built into GCC/Clang) + Valgrind, static-vs-dynamic linking,
  and ABI concepts are evergreen/unchanged. The `__attribute__((cleanup))` note is correctly scoped as a
  **GCC/Clang extension** (not standard C, not portable to MSVC) presented among a portability spectrum.

### DD-35 primary-source citations (fetched-and-read)

> Anti-hallucination (DD-35): every API/flag/standard below traces to a primary source a
> `web-researcher` fetched and read on 2026-07-12. Unverifiable claims are marked `[Needs Verification]`.

- **Undefined behavior** — the UB categories (out-of-bounds access, use-after-free via an invalid
  pointer, signed integer overflow) are drawn from **ISO/IEC 9899** (the C standard); the publicly
  readable near-final draft **N1570** is used for verbatim clause references. Signed-overflow is UB
  while unsigned arithmetic wraps modulo 2ⁿ — both standard-mandated.
- **`__attribute__((cleanup))`** — a **GCC/Clang compiler extension**, NOT standard C and NOT portable
  to MSVC; GCC/Clang also accept the C23 attribute spelling `[[gnu::cleanup]]`. Presented as an
  extension alongside the portable standard goto-cleanup pattern, never as portable C.
- **`errno` + `perror`/`strerror`** — standard C error reporting (`<errno.h>`, `<string.h>`); `errno`
  is thread-local and must be saved before a later call can clobber it.
- **Byte order** — `htonl`/`htons`/`ntohl`/`ntohs` (POSIX `<arpa/inet.h>`) convert host↔network
  (big-endian) order; verified against the POSIX/man-pages specification.
- **BSD sockets** — `socket`/`bind`/`listen`/`accept`/`connect`/`send`/`recv` (POSIX `<sys/socket.h>`)
  are the standard TCP call sequence; verified against the man-pages.
- **AddressSanitizer** `-fsanitize=address` and **UndefinedBehaviorSanitizer** `-fsanitize=undefined`
  are built into GCC and Clang; **Valgrind** (memcheck) is a separate runtime leak/UAF detector.
  Static-vs-dynamic linking and the ABI (calling convention + struct layout) are evergreen, verified
  unchanged.

## Concepts

<!-- co-01 · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · stack-vs-heap** — automatic (stack) storage is scope-bound and freed on return; dynamic (heap) storage lives until you free it.
- **co-02 · pointers** — a pointer holds an address; dereferencing, pointer arithmetic, and NULL are the core operations.
- **co-03 · malloc-free** — `malloc` acquires heap memory and `free` releases it; every `malloc` needs exactly one `free`.
- **co-04 · realloc** — `realloc` resizes an allocation, preserving contents and possibly moving the block.
- **co-05 · calloc** — `calloc` allocates zero-initialized memory and guards the size multiplication.
- **co-06 · alignment** — objects have alignment requirements (`alignof`/`_Alignas`, `aligned_alloc`); misalignment can be UB or slow.
- **co-07 · ownership-discipline** — every resource has exactly one owner responsible for releasing it on every path.
- **co-08 · dangling-pointer** — a pointer to freed or out-of-scope memory is dangling; using it is undefined.
- **co-09 · undefined-behavior** — the C standard leaves some operations undefined; the compiler may assume they never happen.
- **co-10 · buffer-overflow** — writing past an array's bounds corrupts adjacent memory and is UB.
- **co-11 · use-after-free** — accessing memory after `free` is UB, a classic exploit primitive.
- **co-12 · double-free** — freeing the same block twice corrupts the allocator and is UB.
- **co-13 · integer-overflow** — signed overflow is UB; unsigned overflow wraps modulo 2ⁿ; size math must be checked.
- **co-14 · fd-ownership** — a file descriptor is an OS resource that must be `close`d exactly once, like heap memory.
- **co-15 · goto-cleanup** — the single-exit `goto cleanup:` pattern releases every acquired resource on all error paths (portable C).
- **co-16 · attribute-cleanup** — `__attribute__((cleanup))` (GCC/Clang extension, `[[gnu::cleanup]]` in C23) auto-runs a destructor at scope exit.
- **co-17 · errno** — library calls report failure via the thread-local `errno`, reported with `perror`/`strerror`.
- **co-18 · bit-manipulation** — masks and shifts set/clear/toggle/test bits and pack flags into integers.
- **co-19 · structs** — a struct aggregates fields with compiler-inserted padding for alignment.
- **co-20 · unions** — a union overlays members in one storage region; reading a different member is type punning.
- **co-21 · endianness** — byte order (big vs little endian) matters on the wire; `htonl`/`ntohl` normalize it.
- **co-22 · serialization** — converting in-memory values to a defined byte layout and back, independent of host representation.
- **co-23 · compilation-units** — each `.c` file is a translation unit compiled to an object file, then linked.
- **co-24 · headers** — headers declare shared interfaces; include guards prevent double inclusion.
- **co-25 · static-linking** — static libraries (`.a`) are copied into the executable at link time.
- **co-26 · dynamic-linking** — shared objects (`.so`) are resolved at load/run time and shared across processes.
- **co-27 · abi** — the ABI fixes calling convention, register use, and struct layout so separately compiled code interoperates.
- **co-28 · syscalls** — `read`/`write`/`open`/`close` are the direct interface to kernel services.
- **co-29 · signals** — signals deliver asynchronous notifications; handlers must be async-signal-safe (`sig_atomic_t`, `sigaction`).
- **co-30 · sockets** — BSD sockets (`socket`/`bind`/`listen`/`accept`/`connect`) provide the standard TCP endpoint API.

## Worked examples

Colocated under `system-programming/learning/code/`; C, memory-checked with ASan/valgrind (DD-20/DD-30).
Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · malloc-basic** — `malloc` an `int`, write and read it, then `free` — verify the value round-trips. (co-03)
- **ex-02 · malloc-array** — `malloc` an `int` array — verify indexed access. (co-03, co-02)
- **ex-03 · free-basic** — `free` the allocation — verify no leak under ASan. (co-03, co-07)
- **ex-04 · calloc-zeroed** — `calloc` an array — verify every element is zero. (co-05)
- **ex-05 · realloc-grow** — `realloc` to a larger size — verify old contents are preserved. (co-04)
- **ex-06 · realloc-shrink** — `realloc` smaller — verify it still holds the retained prefix. (co-04)
- **ex-07 · pointer-deref** — dereference a pointer — verify the pointed-to value. (co-02)
- **ex-08 · pointer-arith** — walk an array by pointer arithmetic — verify element addresses step by `sizeof`. (co-02)
- **ex-09 · null-check** — check `malloc` returned non-`NULL` — verify the failure path is handled. (co-03, co-02)
- **ex-10 · stack-vs-heap** — a stack variable vs a heap variable — verify their lifetimes differ. (co-01)
- **ex-11 · sizeof** — `sizeof` of types and a struct — verify the reported sizes. (co-19)
- **ex-12 · alignment-alignof** — `alignof` a type — verify its alignment requirement. (co-06)
- **ex-13 · bit-set** — set a bit with `| mask` — verify the bit is set. (co-18)
- **ex-14 · bit-clear** — clear a bit with `& ~mask` — verify the bit is cleared. (co-18)
- **ex-15 · bit-toggle** — toggle a bit with `^ mask` — verify it flips. (co-18)
- **ex-16 · bit-test** — test a bit with `& mask` — verify the result. (co-18)
- **ex-17 · bit-flags** — pack multiple flags into one `int` — verify several flags coexist. (co-18)
- **ex-18 · shift-ops** — left/right shifts — verify multiply/divide by powers of two. (co-18)
- **ex-19 · struct-basic** — define and use a struct — verify field access. (co-19)
- **ex-20 · struct-padding** — observe padding via `sizeof` — verify the compiler-inserted gaps. (co-19, co-06)
- **ex-21 · struct-pointer** — a pointer to a struct with the `->` operator — verify access. (co-19, co-02)
- **ex-22 · array-of-structs** — an array of structs — verify iteration over it. (co-19)
- **ex-23 · union-basic** — a union — verify members share storage. (co-20)
- **ex-24 · union-type-pun** — read a `float`'s bytes via a union — verify the bit pattern. (co-20)
- **ex-25 · dynamic-array-append** — a growable array (`malloc`+`realloc`) append — verify it grows. (co-03, co-04, co-07)
- **ex-26 · dynamic-array-free** — `free` the dynamic array's buffer — verify leak-free under ASan. (co-03, co-07)

### Intermediate

- **ex-27 · double-free-detect** — a double `free` caught by ASan — verify the diagnostic. (co-12, co-11)
- **ex-28 · use-after-free-detect** — a use-after-free caught by ASan — verify the diagnostic. (co-11, co-08)
- **ex-29 · buffer-overflow-detect** — an off-by-one write caught by ASan — verify the diagnostic. (co-10)
- **ex-30 · dangling-pointer** — a dangling pointer after `free` — verify the hazard. (co-08, co-11)
- **ex-31 · null-deref-guard** — guard against a `NULL` dereference — verify the safe path. (co-02)
- **ex-32 · integer-overflow-signed** — signed overflow is UB — verify it under `-fsanitize=undefined`. (co-13, co-09)
- **ex-33 · unsigned-wraparound** — unsigned wraparound is defined — verify the modular result. (co-13)
- **ex-34 · size-overflow-check** — check a `malloc` size multiplication for overflow — verify the guard. (co-13, co-03)
- **ex-35 · goto-cleanup-single** — the single-exit `goto cleanup` pattern — verify every path frees. (co-15, co-07)
- **ex-36 · goto-cleanup-multi** — `goto cleanup` with several resources — verify ordered release. (co-15, co-14)
- **ex-37 · attribute-cleanup** — `__attribute__((cleanup))` auto-frees at scope exit — verify (GCC/Clang only). (co-16)
- **ex-38 · attribute-cleanup-fd** — a cleanup attribute closing an fd — verify the fd is closed. (co-16, co-14)
- **ex-39 · errno-open-fail** — `open` a missing file, check `errno` — verify `ENOENT`. (co-17, co-28)
- **ex-40 · perror-strerror** — report `errno` via `perror`/`strerror` — verify the message. (co-17)
- **ex-41 · errno-save** — save `errno` before it's clobbered — verify it's preserved. (co-17)
- **ex-42 · fd-open-close** — `open` then `close` a file — verify the fd lifecycle. (co-14, co-28)
- **ex-43 · fd-leak-detect** — an fd leak and its fix — verify the descriptor is released. (co-14)
- **ex-44 · read-syscall** — `read` from an fd — verify the bytes read. (co-28)
- **ex-45 · write-syscall** — `write` to an fd — verify the bytes written. (co-28)
- **ex-46 · endianness-detect** — detect host endianness — verify little vs big. (co-21)
- **ex-47 · htonl-ntohl** — an `htonl`/`ntohl` round-trip — verify network byte order. (co-21)
- **ex-48 · serialize-int** — serialize an `int` to big-endian bytes — verify the byte order. (co-22, co-21)
- **ex-49 · deserialize-int** — deserialize bytes back to an `int` — verify the value. (co-22, co-21)
- **ex-50 · serialize-struct** — serialize a struct field-by-field — verify it's layout-independent. (co-22, co-19)
- **ex-51 · serialize-roundtrip** — serialize then deserialize — verify the round-trip. (co-22)
- **ex-52 · linked-list-owned** — a linked list with disciplined node ownership + free-all — verify leak-free. (co-07, co-03)

### Advanced

- **ex-53 · compilation-units** — split code across `.c` files with a shared header — verify it links. (co-23, co-24)
- **ex-54 · include-guard** — a header include guard — verify no double-inclusion. (co-24)
- **ex-55 · static-library** — build a static `.a` and link it — verify the symbol resolves. (co-25, co-23)
- **ex-56 · dynamic-library** — build a shared `.so` and link it — verify runtime loading. (co-26)
- **ex-57 · abi-struct-layout** — an ABI-stable struct shared across units — verify binary compatibility. (co-27, co-19)
- **ex-58 · memory-pool** — a fixed-size memory-pool allocator — verify alloc/free from the pool. (co-03, co-07)
- **ex-59 · arena-allocator** — an arena/bump allocator — verify bulk free. (co-03, co-07)
- **ex-60 · pool-reuse** — pool slot reuse after free — verify recycling. (co-07)
- **ex-61 · aligned-alloc** — `aligned_alloc` for an aligned buffer — verify the alignment. (co-06, co-03)
- **ex-62 · signal-handler** — install a `SIGINT` handler — verify it fires. (co-29)
- **ex-63 · signal-safe-flag** — set a `volatile sig_atomic_t` flag in the handler — verify async-safety. (co-29)
- **ex-64 · sigaction** — `sigaction` over `signal()` — verify reliable handling. (co-29)
- **ex-65 · socket-create** — create a TCP socket — verify an fd is returned. (co-30, co-14)
- **ex-66 · socket-bind-listen** — `bind` + `listen` on a port — verify it's listening. (co-30)
- **ex-67 · socket-accept** — `accept` a connection — verify a client fd. (co-30)
- **ex-68 · socket-connect** — `connect` a client — verify the connection. (co-30)
- **ex-69 · socket-send-recv** — `send`/`recv` bytes — verify the data transfer. (co-30, co-28)
- **ex-70 · socket-serialized** — send serialized data over a socket — verify the round-trip. (co-30, co-22)
- **ex-71 · client-server-echo** — a minimal echo client/server — verify the message is echoed. (co-30)
- **ex-72 · overflow-then-fix** — a buffer overflow then its bounds-checked fix — verify ASan-clean after. (co-10)
- **ex-73 · uaf-then-fix** — a use-after-free then its ownership fix — verify ASan-clean after. (co-11, co-07)
- **ex-74 · valgrind-clean** — run a program under valgrind — verify no leaks are reported. (co-03, co-07)
- **ex-75 · asan-clean** — build with `-fsanitize=address` — verify a clean run. (co-10, co-11)
- **ex-76 · full-systems-slice** — pool + endianness serialization + socket exchange — verify the whole. (co-07, co-22, co-30)
- **ex-77 · integration-memclean** — the whole program under ASan + valgrind — verify no leak or UB. (co-03, co-07)
- **ex-78 · capstone-systems-component** — a systems component: a memory pool with disciplined ownership, endianness-aware serialization, and a minimal socket client/server, memory-clean under ASan/valgrind — verify ownership is disciplined, serialization is endianness-correct, the socket exchange works, and the whole program is memory-clean. (co-07, co-22, co-30)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a small systems component in C — a dynamic data structure or memory pool with disciplined
  manual ownership + cleanup, a serialization routine that handles endianness, and a minimal socket
  client/server — that runs **memory-clean under AddressSanitizer/valgrind** (no leaks, no use-after-free,
  no overflow), demonstrating safe systems programming without RAII.
- **Concepts exercised**: [ ] correct `malloc`/`realloc`/`free` ownership (co-03, co-04, co-07) [ ] scope-based
  manual cleanup (goto-cleanup / `__attribute__((cleanup))`) (co-15, co-16) [ ] `errno`-based error handling
  (co-17) [ ] endianness-aware serialization (co-21, co-22) [ ] a minimal socket client/server (co-30) [ ] a
  clean ASan/valgrind run (co-10, co-11).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a dynamic structure or memory pool with disciplined alloc/free +
     cleanup. Verify it runs **leak-free** under valgrind/ASan.
  2. Add an endianness-aware serialization routine. Verify round-tripping a value across serialize/
     deserialize preserves it regardless of host endianness.
  3. Add a minimal socket client/server exchanging serialized data. Verify a message round-trips and the
     whole program stays ASan/valgrind-clean.
- **Acceptance criteria**: ownership + cleanup are disciplined; serialization is endianness-correct; the
  socket exchange works; the entire program is **memory-clean** under AddressSanitizer/valgrind.
- **Done bar**: runnable end-to-end + memory-clean + web-verified.

## Read more

**Books**

- **The C Programming Language**, 2nd ed. — Brian W. Kernighan, Dennis M. Ritchie (1988). The original, definitive book on C, written by the language's co-creator; the field's baseline reference for decades.
- **Advanced Programming in the UNIX Environment**, 3rd ed. — W. Richard Stevens, Stephen A. Rago (2013). The canonical guide to Unix/POSIX systems programming: syscalls, processes, files, threads, and IPC.
- **The Linux Programming Interface** — Michael Kerrisk (2010). The most comprehensive modern single-volume reference for Linux/Unix system calls and the C library, by the Linux man-pages maintainer.
- **Operating Systems: Three Easy Pieces** — Remzi H. Arpaci-Dusseau, Andrea C. Arpaci-Dusseau. Free, widely-adopted OS textbook covering virtualization, concurrency, and persistence from first principles. <https://pages.cs.wisc.edu/~remzi/OSTEP/>
- **The Art of Unix Programming** — Eric S. Raymond (2003). Canonical treatment of Unix design philosophy and programming culture, freely licensed by the author. <http://www.catb.org/esr/writings/taoup/html/>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Theory & low-level systems — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Concurrency & language breadth — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 4 · Systems programming & OS internals.

> _Content originated in the now-closed FS-SE plan (topic 81); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
