---
title: "Intermediate Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

Examples 27–54 make machine-visible data practical: pointers and dereferencing, array decay, strings, structs, file I/O, macros, headers, linking, and warning-clean compilation.

## Example 27: Take an Address with &

_ex-27 · exercises co-10_

Obtain an object's address without relying on its printed numeric form. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-27-pointer-address/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    int value = 9;
// => this line is part of the complete runnable program
    int *address = &value;
// => this line is part of the complete runnable program
    printf("address-captured=%d\n", address == &value);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
address-captured=1
```

**Key takeaway**: Obtain an object's address without relying on its printed numeric form. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Obtain an object's address without relying on its printed numeric form. Check the boundary before acting through an address or resource.

---

## Example 28: Declare a Pointer

_ex-28 · exercises co-10_

Store an integer's address in an int pointer. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-28-pointer-declare/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    int value = 9;
// => this line is part of the complete runnable program
    int *pointer = &value;
// => this line is part of the complete runnable program
    printf("same-address=%d\n", pointer == &value);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
same-address=1
```

**Key takeaway**: Store an integer's address in an int pointer. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Store an integer's address in an int pointer. Check the boundary before acting through an address or resource.

---

## Example 29: Dereference to Read

_ex-29 · exercises co-11_

Read the value behind a pointer. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-29-deref-read/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    int value = 12;
// => this line is part of the complete runnable program
    int *pointer = &value;
// => this line is part of the complete runnable program
    printf("value=%d\n", *pointer);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
value=12
```

**Key takeaway**: Read the value behind a pointer. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Read the value behind a pointer. Check the boundary before acting through an address or resource.

---

## Example 30: Dereference to Write

_ex-30 · exercises co-11_

Change a caller-owned value through its address. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-30-deref-write/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    int value = 0;
// => this line is part of the complete runnable program
    int *pointer = &value;
// => this line is part of the complete runnable program
    *pointer = 5;
// => this line is part of the complete runnable program
    printf("value=%d\n", value);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
value=5
```

**Key takeaway**: Change a caller-owned value through its address. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Change a caller-owned value through its address. Check the boundary before acting through an address or resource.

---

## Example 31: Pass a Pointer to Mutate

_ex-31 · exercises co-11, co-09_

Let a function update its caller's object. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-31-pointer-function/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
static void increment(int *value) {
// => this line is part of the complete runnable program
    *value += 1;
// => this line is part of the complete runnable program
}
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    int value = 10;
// => this line is part of the complete runnable program
    increment(&value);
// => this line is part of the complete runnable program
    printf("value=%d\n", value);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
value=11
```

**Key takeaway**: Let a function update its caller's object. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Let a function update its caller's object. Check the boundary before acting through an address or resource.

---

## Example 32: Guard a NULL Pointer

_ex-32 · exercises co-10_

Check a nullable address before dereferencing it. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-32-null-pointer/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    int *maybe_value = NULL;
// => this line is part of the complete runnable program
    if (maybe_value == NULL) {
// => this line is part of the complete runnable program
        puts("no value");
// => this line is part of the complete runnable program
    }
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
no value
```

**Key takeaway**: Check a nullable address before dereferencing it. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Check a nullable address before dereferencing it. Check the boundary before acting through an address or resource.

---

## Example 33: Array Decay at a Function Call

_ex-33 · exercises co-13_

Pass an array as a pointer to its first element. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-33-array-decay/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
static int first(const int values[]) {
// => this line is part of the complete runnable program
    return values[0];
// => this line is part of the complete runnable program
}
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    int values[] = {4, 5};
// => this line is part of the complete runnable program
    printf("first=%d\n", first(values));
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
first=4
```

**Key takeaway**: Pass an array as a pointer to its first element. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Pass an array as a pointer to its first element. Check the boundary before acting through an address or resource.

---

## Example 34: Pointer Arithmetic Matches Indexing

_ex-34 · exercises co-13, co-10_

Use a pointer offset to reach an array element. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-34-pointer-arithmetic/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    int values[] = {4, 5, 6};
// => this line is part of the complete runnable program
    printf("equal=%d\n", *(values + 1) == values[1]);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
equal=1
```

**Key takeaway**: Use a pointer offset to reach an array element. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Use a pointer offset to reach an array element. Check the boundary before acting through an address or resource.

---

## Example 35: Walk to a String Terminator

_ex-35 · exercises co-14_

Count characters until the terminating zero byte. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-35-string-length/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    const char *word = "cat";
// => this line is part of the complete runnable program
    size_t length = 0;
// => this line is part of the complete runnable program
    while (word[length] != '\0') {
// => this line is part of the complete runnable program
        ++length;
// => this line is part of the complete runnable program
    }
// => this line is part of the complete runnable program
    printf("length=%zu\n", length);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
length=3
```

**Key takeaway**: Count characters until the terminating zero byte. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Count characters until the terminating zero byte. Check the boundary before acting through an address or resource.

---

## Example 36: Use strlen and strcpy

_ex-36 · exercises co-14, co-20_

Use standard string helpers with enough destination space. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-36-string-h/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this directive makes a declaration available
#include <string.h>
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    char copy[8];
// => this line is part of the complete runnable program
    strcpy(copy, "cat");
// => this line is part of the complete runnable program
    printf("copy=%s length=%zu\n", copy, strlen(copy));
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
copy=cat length=3
```

**Key takeaway**: Use standard string helpers with enough destination space. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Use standard string helpers with enough destination space. Check the boundary before acting through an address or resource.

---

## Example 37: Define a struct

_ex-37 · exercises co-15_

Group related fields in one value. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-37-struct-define/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
struct User { const char *name; int id; };
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    struct User user = {"Ada", 7};
// => this line is part of the complete runnable program
    printf("%s %d\n", user.name, user.id);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
Ada 7
```

**Key takeaway**: Group related fields in one value. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Group related fields in one value. Check the boundary before acting through an address or resource.

---

## Example 38: Initialize a struct

_ex-38 · exercises co-15_

Initialize a named field at construction. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-38-struct-init/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
struct Service { const char *name; };
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    struct Service service = {.name = "api"};
// => this line is part of the complete runnable program
    printf("service=%s\n", service.name);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
service=api
```

**Key takeaway**: Initialize a named field at construction. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Initialize a named field at construction. Check the boundary before acting through an address or resource.

---

## Example 39: Pass a struct by Value

_ex-39 · exercises co-15, co-09_

Show that a struct parameter is copied. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-39-struct-function/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
struct Score { int value; };
// => this line is part of the complete runnable program
static void raise_copy(struct Score score) {
// => this line is part of the complete runnable program
    score.value = 9;
// => this line is part of the complete runnable program
    printf("inside=%d ", score.value);
// => this line is part of the complete runnable program
}
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    struct Score score = {3};
// => this line is part of the complete runnable program
    raise_copy(score);
// => this line is part of the complete runnable program
    printf("outside=%d\n", score.value);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
inside=9 outside=3
```

**Key takeaway**: Show that a struct parameter is copied. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Show that a struct parameter is copied. Check the boundary before acting through an address or resource.

---

## Example 40: Access a struct through ->

_ex-40 · exercises co-16_

Use arrow syntax through a struct pointer. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-40-struct-pointer/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
struct Server { int port; };
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    struct Server server = {80};
// => this line is part of the complete runnable program
    struct Server *pointer = &server;
// => this line is part of the complete runnable program
    printf("port=%d\n", pointer->port);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
port=80
```

**Key takeaway**: Use arrow syntax through a struct pointer. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Use arrow syntax through a struct pointer. Check the boundary before acting through an address or resource.

---

## Example 41: Mutate a struct through a Pointer

_ex-41 · exercises co-16, co-11_

Change a field visible to the caller. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-41-struct-pointer-mutate/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
struct Counter { int count; };
// => this line is part of the complete runnable program
static void increment(struct Counter *counter) {
// => this line is part of the complete runnable program
    counter->count += 1;
// => this line is part of the complete runnable program
}
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    struct Counter counter = {1};
// => this line is part of the complete runnable program
    increment(&counter);
// => this line is part of the complete runnable program
    printf("count=%d\n", counter.count);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
count=2
```

**Key takeaway**: Change a field visible to the caller. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Change a field visible to the caller. Check the boundary before acting through an address or resource.

---

## Example 42: An Array of structs

_ex-42 · exercises co-15, co-12_

Traverse records stored contiguously. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-42-array-of-structs/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
struct Item { int quantity; };
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    struct Item items[] = {{1}, {2}};
// => this line is part of the complete runnable program
    int total = 0;
// => this line is part of the complete runnable program
    for (size_t index = 0; index < 2; ++index) {
// => this line is part of the complete runnable program
        total += items[index].quantity;
// => this line is part of the complete runnable program
    }
// => this line is part of the complete runnable program
    printf("total=%d\n", total);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
total=3
```

**Key takeaway**: Traverse records stored contiguously. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Traverse records stored contiguously. Check the boundary before acting through an address or resource.

---

## Example 43: Write a File with fopen

_ex-43 · exercises co-19_

Open a temporary file and write a record. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-43-fopen-write/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    FILE *file = tmpfile();
// => this line is part of the complete runnable program
    if (file == NULL) return 1;
// => this line is part of the complete runnable program
    fprintf(file, "written\n");
// => this line is part of the complete runnable program
    fclose(file);
// => this line is part of the complete runnable program
    puts("written");
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
written
```

**Key takeaway**: Open a temporary file and write a record. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Open a temporary file and write a record. Check the boundary before acting through an address or resource.

---

## Example 44: Read a File with fscanf

_ex-44 · exercises co-19_

Write controlled input then parse it from a file. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-44-fopen-read/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    FILE *file = tmpfile();
// => this line is part of the complete runnable program
    int value = 0;
// => this line is part of the complete runnable program
    if (file == NULL) return 1;
// => this line is part of the complete runnable program
    fprintf(file, "12\n");
// => this line is part of the complete runnable program
    rewind(file);
// => this line is part of the complete runnable program
    if (fscanf(file, "%d", &value) != 1) return 1;
// => this line is part of the complete runnable program
    fclose(file);
// => this line is part of the complete runnable program
    printf("value=%d\n", value);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
value=12
```

**Key takeaway**: Write controlled input then parse it from a file. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Write controlled input then parse it from a file. Check the boundary before acting through an address or resource.

---

## Example 45: Close a File

_ex-45 · exercises co-19_

Close an output stream and check the result. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-45-fclose/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    FILE *file = tmpfile();
// => this line is part of the complete runnable program
    if (file == NULL) return 1;
// => this line is part of the complete runnable program
    fputs("closed\n", file);
// => this line is part of the complete runnable program
    if (fclose(file) != 0) return 1;
// => this line is part of the complete runnable program
    puts("closed");
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
closed
```

**Key takeaway**: Close an output stream and check the result. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Close an output stream and check the result. Check the boundary before acting through an address or resource.

---

## Example 46: More printf Specifiers

_ex-46 · exercises co-17_

Print hexadecimal, a character, and a captured address fact. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-46-printf-specifiers/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    int value = 42;
// => this line is part of the complete runnable program
    printf("hex=%x char=%c address-captured=%d\n", value, 'A', &value != NULL);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
hex=2a char=A address-captured=1
```

**Key takeaway**: Print hexadecimal, a character, and a captured address fact. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Print hexadecimal, a character, and a captured address fact. Check the boundary before acting through an address or resource.

---

## Example 47: A Function with Multiple Arguments

_ex-47 · exercises co-09_

Pass several values to one calculation. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-47-multiple-args/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
static int volume(int width, int height, int depth) {
// => this line is part of the complete runnable program
    return width * height * depth;
// => this line is part of the complete runnable program
}
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    printf("volume=%d\n", volume(2, 3, 4));
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
volume=24
```

**Key takeaway**: Pass several values to one calculation. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Pass several values to one calculation. Check the boundary before acting through an address or resource.

---

## Example 48: A Recursive Function

_ex-48 · exercises co-09_

Make progress toward a base case. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-48-recursion/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
static int factorial(int value) {
// => this line is part of the complete runnable program
    return value <= 1 ? 1 : value * factorial(value - 1);
// => this line is part of the complete runnable program
}
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    printf("factorial=%d\n", factorial(5));
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
factorial=120
```

**Key takeaway**: Make progress toward a base case. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Make progress toward a base case. Check the boundary before acting through an address or resource.

---

## Example 49: A Function-Like Macro

_ex-49 · exercises co-21_

Use a parenthesized macro expression safely. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-49-define-macro/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this directive makes a declaration available
#define SQUARE(value) ((value) * (value))
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    printf("square=%d\n", SQUARE(5));
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
square=25
```

**Key takeaway**: Use a parenthesized macro expression safely. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Use a parenthesized macro expression safely. Check the boundary before acting through an address or resource.

---

## Example 50: Separate Header and Definition

_ex-50 · exercises co-23, co-20_

Compile a declaration and definition in separate files. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-50-header-file/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this directive makes a declaration available
#include "answer.h"
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    printf("answer=%d\n", answer());
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `make && ./example`.

**Expected output**:

```text
answer=42
```

**Key takeaway**: Compile a declaration and definition in separate files. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Compile a declaration and definition in separate files. Check the boundary before acting through an address or resource.

---

## Example 51: A Portable Header Guard

_ex-51 · exercises co-22_

Include the same guarded header twice safely. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-51-header-guard/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this directive makes a declaration available
#include "config.h"
// => this directive makes a declaration available
#include "config.h"
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    puts(MESSAGE);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `make && ./example`.

**Expected output**:

```text
guard works
```

**Key takeaway**: Include the same guarded header twice safely. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Include the same guarded header twice safely. Check the boundary before acting through an address or resource.

---

## Example 52: #pragma once Is Non-Standard

_ex-52 · exercises co-22_

Observe a common extension while keeping portable guards preferred. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-52-pragma-once/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this directive makes a declaration available
#include "config.h"
// => this directive makes a declaration available
#include "config.h"
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    puts(MESSAGE);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `make && ./example`.

**Expected output**:

```text
extension compiled
```

**Key takeaway**: Observe a common extension while keeping portable guards preferred. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Observe a common extension while keeping portable guards preferred. Check the boundary before acting through an address or resource.

---

## Example 53: Compile Two Sources and Link

_ex-53 · exercises co-02, co-23_

Build two translation units into one executable. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-53-two-file-compile/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
int add(int left, int right);
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    printf("sum=%d\n", add(2, 3));
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `make && ./example`.

**Expected output**:

```text
sum=5
```

**Key takeaway**: Build two translation units into one executable. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Build two translation units into one executable. Check the boundary before acting through an address or resource.

---

## Example 54: Build Warning-Clean

_ex-54 · exercises co-26_

Compile with warning flags and use every value. The complete source set stays deliberately small and local to this example.

**`learning/code/ex-54-warnings-clean/example.c`**

```c
// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
int main(void) {
// => this line is part of the complete runnable program
    int value = 3;
// => this line is part of the complete runnable program
    printf("value=%d\n", value);
// => this line is part of the complete runnable program
    return 0;
// => this line is part of the complete runnable program
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
value=3
```

**Key takeaway**: Compile with warning flags and use every value. Check the boundary before acting through an address or resource.

**Why it matters**: C does not hide representation or ownership. This isolated program shows exactly which object is being passed, read, changed, or released, so the same decision remains legible when later systems programs add OS-facing APIs around it. Reviewers can then trace the boundary without inferring hidden copying, lifetime, or layout assumptions from surrounding framework code. The specific practice in this example is: Compile with warning flags and use every value. Check the boundary before acting through an address or resource.

---
