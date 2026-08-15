---
title: "Drilling Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

This is the active-recall companion to Just Enough C. It has five fixed sections: recall, applied
judgment, runnable repairs, a self-check, and elaborative explanation. Attempt each prompt before
revealing its answer or opening an after-file.

## Recall Q&A

**Q1 (co-01, co-02, co-26).** What command compiles a conservative C17 source with useful warnings,
and what are compilation and linking producing?

<details><summary>Answer</summary>

`cc -std=c17 -Wall -Wextra -pedantic example.c -o example` compiles source into object code and
links it into the `example` executable. Warnings are evidence to fix, not normal build output.

</details>

**Q2 (co-10, co-11).** What is the difference between `&value` and `*pointer`?

<details><summary>Answer</summary>

`&value` obtains the address of the object. `*pointer` dereferences a valid pointer to read or
write the object at that address; it must not be applied to `NULL` or a dead address.

</details>

**Q3 (co-12, co-13, co-14).** What happens when an array is passed to a function, and how does a C
string end?

<details><summary>Answer</summary>

An array argument decays to a pointer to its first element, so pass a separate count when the
function needs bounds. A C string is a `char` sequence ending in `'\0'`.

</details>

**Q4 (co-15, co-16).** When do you use `.` versus `->` for a struct member?

<details><summary>Answer</summary>

Use `.` with a struct value and `->` with a pointer to a struct. `pointer->field` is shorthand
for `(*pointer).field`.

</details>

**Q5 (co-19, co-24).** What check comes before using `fopen` or `malloc`, and what cleanup
follows success?

<details><summary>Answer</summary>

Check the returned pointer for `NULL`. A successful file stream is closed with `fclose`; a
successful heap allocation is released once with `free`, then never dereferenced or freed again.

</details>

**Q6 (co-20 through co-23).** Why does a small multi-file program need a guarded header?

<details><summary>Answer</summary>

The header shares declarations without creating multiple definitions, and the `#ifndef` /
`#define` / `#endif` guard makes repeated inclusion safe in portable C.

</details>

## Applied problems

1. A parser accepts a pointer that may be absent. State the guard that must occur before
   dereferencing it, then write the smallest safe branch.
2. A function must update a caller’s counter. Decide whether to pass the integer or its address, and
   explain where the mutation becomes visible.
3. A record is shared between two `.c` files. Name the three artifacts needed for one declaration,
   one definition, and a linkable program.
4. A heap allocation succeeds. List the only owner, the point at which it is released, and the two
   actions that must never follow release.
5. A build emits a warning. Treat it as a failing contract: identify the source mismatch and make
   the `-Wall -Wextra` build clean.

## Code katas

1. Add a NULL guard before using an optional pointer, then explain which caller-visible result
   represents absence.
2. Change a caller-owned counter through a pointer while preserving a single, obvious owner.
3. Pass an array with an explicit element count and reject an index outside that count.
4. Trace a successful `malloc` through its single `free`, then identify the first invalid use after
   release.
5. Split a declaration and definition across a guarded header and two C source files, then make the
   warning-clean build repeatable.

## Self-check checklist

- [ ] I can compile and run a C17 source file with warnings enabled.
- [ ] I can explain `&`, `*`, `[]`, `.`, and `->` without treating them as interchangeable.
- [ ] I can pass an array or a struct pointer to a function and name who owns the mutation.
- [ ] I can check allocation and file-opening failures before using their results.
- [ ] I can split a small program into a guarded header and two source files, then build it with
      `make`.

## Elaborative interrogation and self-explanation

1. Why does C make an address explicit instead of automatically copying every object into a function?
2. Why is a header declaration not a definition, and how does that distinction help the linker?
3. Why must `free` happen exactly once for each successful `malloc`, even in a small program?
4. Why do warning flags belong in a Makefile rather than only in a developer’s remembered command?
5. Why are C17-portable examples safer systems prerequisites than compiler-specific extensions?
