---
title: "Drilling"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Use this in five passes. Answer before opening a disclosure; run katas only from a disposable build
directory; keep an ownership table beside unfamiliar C.

## 1. Recall

1. Who releases a successfully allocated buffer after ownership transfer?
2. Why is `tmp = realloc(p, n)` safer than assigning directly to `p`?
3. What must happen to every owned file descriptor at cleanup?
4. Why is copying a C struct directly to a socket not a serialization format?
5. What is the portable C cleanup technique used in this course?

<details><summary>Answers</summary>

The current single owner releases it; preserve `p` if resize fails; close it once; padding,
endianness, and widths are host-dependent; reverse-order `goto cleanup`. GCC/Clang cleanup
attributes are extensions, never the portable answer.

</details>

## 2. Trace ownership

For each line, write the owner before and after it:

```c
char *message = malloc(32);
if (message == NULL) goto cleanup;
client.message = message;
message = NULL;
```

<details><summary>Check</summary>

Before assignment, the local owns the allocation. After assignment, `client.message` owns it;
clearing the local makes the transfer visible and prevents two owners.

</details>

## 3. Repair kata

Repair this before running it: it uses the old pointer after an unchecked resize.

```c
items = realloc(items, new_count * sizeof *items);
items[new_count - 1] = value;
```

<details><summary>One safe shape</summary>

Check `new_count <= SIZE_MAX / sizeof *items`, assign `realloc` to a temporary,
check it, then replace `items`. Keep the old allocation live on failure.

</details>

## 4. Debugging drill

An ASan report says “heap-use-after-free”; do not treat it as an allocator failure. Locate the free,
identify all aliases, decide which component owns the allocation, and make post-transfer/non-owner
pointers unusable. Then run the safe fixture with ASan and, separately on Linux, Valgrind.

## 5. Completion checklist

- [ ] I can state one owner for every heap allocation, fd, and socket.
- [ ] I use checked size arithmetic before allocation.
- [ ] I can write a reverse-order `goto cleanup` path without hiding ownership.
- [ ] I serialize each wire field explicitly in network byte order.
- [ ] I ran the capstone clean under ASan and Valgrind separately (Linux).
