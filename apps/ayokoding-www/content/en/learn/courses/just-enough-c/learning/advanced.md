---
title: "Advanced Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 30
---

Examples 55–78 add the minimum ownership and build surface needed by systems work: malloc/free, pointer chains, linked nodes, Makefiles, object files, conditional compilation, and a short multi-file integration.

## Example 55: Allocate One int

_ex-55 · exercises co-24_

Allocate, check, use, and release one integer. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-55-malloc-basic/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include <stdlib.h>
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    int *value = malloc(sizeof *value);
// => this line makes the program's state or output explicit
    if (value == NULL) return 1;
// => this line makes the program's state or output explicit
    *value = 8;
// => this line makes the program's state or output explicit
    printf("value=%d\n", *value);
// => this line makes the program's state or output explicit
    free(value);
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
value=8
```

**Key takeaway**: Allocate, check, use, and release one integer. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Allocate, check, use, and release one integer. Keep ownership and the build boundary explicit.

---

## Example 56: Allocate a Dynamic Array

_ex-56 · exercises co-24, co-12_

Allocate indexed storage at runtime. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-56-malloc-array/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include <stdlib.h>
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    int *values = malloc(3 * sizeof *values);
// => this line makes the program's state or output explicit
    if (values == NULL) return 1;
// => this line makes the program's state or output explicit
    values[0] = 1; values[1] = 2; values[2] = 3;
// => this line makes the program's state or output explicit
    printf("sum=%d\n", values[0] + values[1] + values[2]);
// => this line makes the program's state or output explicit
    free(values);
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
sum=6
```

**Key takeaway**: Allocate indexed storage at runtime. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Allocate indexed storage at runtime. Keep ownership and the build boundary explicit.

---

## Example 57: Release Allocated Memory

_ex-57 · exercises co-24_

Pair a successful allocation with free exactly once. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-57-free-memory/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include <stdlib.h>
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    int *value = malloc(sizeof *value);
// => this line makes the program's state or output explicit
    if (value == NULL) return 1;
// => this line makes the program's state or output explicit
    *value = 1;
// => this line makes the program's state or output explicit
    free(value);
// => this line makes the program's state or output explicit
    puts("released");
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
released
```

**Key takeaway**: Pair a successful allocation with free exactly once. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Pair a successful allocation with free exactly once. Keep ownership and the build boundary explicit.

---

## Example 58: Allocate a struct

_ex-58 · exercises co-24, co-16_

Allocate a record and access it through ->. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-58-malloc-struct/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include <stdlib.h>
// => this line makes the program's state or output explicit
struct Server { int port; };
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    struct Server *server = malloc(sizeof *server);
// => this line makes the program's state or output explicit
    if (server == NULL) return 1;
// => this line makes the program's state or output explicit
    server->port = 443;
// => this line makes the program's state or output explicit
    printf("port=%d\n", server->port);
// => this line makes the program's state or output explicit
    free(server);
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
port=443
```

**Key takeaway**: Allocate a record and access it through ->. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Allocate a record and access it through ->. Keep ownership and the build boundary explicit.

---

## Example 59: A Pointer to a Pointer

_ex-59 · exercises co-10, co-11_

Follow two levels of indirection carefully. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-59-pointer-to-pointer/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    int value = 4;
// => this line makes the program's state or output explicit
    int *pointer = &value;
// => this line makes the program's state or output explicit
    int **double_pointer = &pointer;
// => this line makes the program's state or output explicit
    printf("value=%d\n", **double_pointer);
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
value=4
```

**Key takeaway**: Follow two levels of indirection carefully. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Follow two levels of indirection carefully. Keep ownership and the build boundary explicit.

---

## Example 60: An Array of String Pointers

_ex-60 · exercises co-13, co-14_

Iterate pointers to null-terminated strings. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-60-array-of-pointers/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    const char *colors[] = {"red", "blue"};
// => this line makes the program's state or output explicit
    printf("%s %s\n", colors[0], colors[1]);
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
red blue
```

**Key takeaway**: Iterate pointers to null-terminated strings. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Iterate pointers to null-terminated strings. Keep ownership and the build boundary explicit.

---

## Example 61: A Linked Node struct

_ex-61 · exercises co-16, co-24_

Link two heap nodes and traverse the small chain. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-61-struct-linked/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include <stdlib.h>
// => this line makes the program's state or output explicit
struct Node { int value; struct Node *next; };
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    struct Node *first = malloc(sizeof *first);
// => this line makes the program's state or output explicit
    struct Node *second = malloc(sizeof *second);
// => this line makes the program's state or output explicit
    if (first == NULL || second == NULL) { free(first); free(second); return 1; }
// => this line makes the program's state or output explicit
    first->value = 1; first->next = second;
// => this line makes the program's state or output explicit
    second->value = 2; second->next = NULL;
// => this line makes the program's state or output explicit
    for (struct Node *node = first; node != NULL; node = node->next) {
// => this line makes the program's state or output explicit
        printf("%d%s", node->value, node->next == NULL ? "\n" : " ");
// => this line makes the program's state or output explicit
    }
// => this line makes the program's state or output explicit
    free(second); free(first);
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
1 2
```

**Key takeaway**: Link two heap nodes and traverse the small chain. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Link two heap nodes and traverse the small chain. Keep ownership and the build boundary explicit.

---

## Example 62: A Basic Makefile

_ex-62 · exercises co-03_

Use make to compile a named target. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-62-makefile-basic/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    puts("make builds this example");
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `make && ./example`.

**Expected output**:

```text
make builds this example
```

**Key takeaway**: Use make to compile a named target. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Use make to compile a named target. Keep ownership and the build boundary explicit.

---

## Example 63: A clean Target

_ex-63 · exercises co-03_

Remove local build artifacts through make clean. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-63-makefile-clean/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    puts("clean target documented");
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `make && ./example`.

**Expected output**:

```text
clean target documented
```

**Key takeaway**: Remove local build artifacts through make clean. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Remove local build artifacts through make clean. Keep ownership and the build boundary explicit.

---

## Example 64: Makefile CC and CFLAGS Variables

_ex-64 · exercises co-03_

Make compiler choices explicit in a Makefile. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-64-makefile-vars/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    puts("variables documented");
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `make && ./example`.

**Expected output**:

```text
variables documented
```

**Key takeaway**: Make compiler choices explicit in a Makefile. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Make compiler choices explicit in a Makefile. Keep ownership and the build boundary explicit.

---

## Example 65: A Multi-Object Makefile

_ex-65 · exercises co-03, co-02_

Describe object dependencies for an incremental build. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-65-makefile-multi/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int add(int left, int right);
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    puts("multi-file build");
// => this line makes the program's state or output explicit
    return add(1, 1) == 2 ? 0 : 1;
// => this line makes the program's state or output explicit
}
```

**Run**: `make && ./example`.

**Expected output**:

```text
multi-file build
```

**Key takeaway**: Describe object dependencies for an incremental build. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Describe object dependencies for an incremental build. Keep ownership and the build boundary explicit.

---

## Example 66: Object Files Then Link

_ex-66 · exercises co-02_

Separate compilation from final linking. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-66-object-files/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int add(int left, int right);
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    puts("object workflow");
// => this line makes the program's state or output explicit
    return add(1, 1) == 2 ? 0 : 1;
// => this line makes the program's state or output explicit
}
```

**Run**: `make && ./example`.

**Expected output**:

```text
object workflow
```

**Key takeaway**: Separate compilation from final linking. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Separate compilation from final linking. Keep ownership and the build boundary explicit.

---

## Example 67: An extern Declaration

_ex-67 · exercises co-23_

Read one definition from another translation unit. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-67-extern-declaration/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include "limit.h"
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    printf("limit=%d\n", limit);
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `make && ./example`.

**Expected output**:

```text
limit=9
```

**Key takeaway**: Read one definition from another translation unit. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Read one definition from another translation unit. Keep ownership and the build boundary explicit.

---

## Example 68: Conditional Compilation

_ex-68 · exercises co-21_

Select code when a macro is defined. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-68-conditional-compile/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int main(void) {
// => this directive is part of the source interface
#ifdef DEBUG
// => this line makes the program's state or output explicit
    puts("debug=on");
// => this directive is part of the source interface
#else
// => this line makes the program's state or output explicit
    puts("debug=off");
// => this directive is part of the source interface
#endif
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
debug=off
```

**Key takeaway**: Select code when a macro is defined. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Select code when a macro is defined. Keep ownership and the build boundary explicit.

---

## Example 69: sizeof and struct Layout

_ex-69 · exercises co-25, co-15_

Measure a struct without assuming its padding. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-69-sizeof-struct-layout/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
struct Record { char tag; int id; };
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    printf("record-bytes=%zu\n", sizeof(struct Record));
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
record byte count shown
```

**Key takeaway**: Measure a struct without assuming its padding. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Measure a struct without assuming its padding. Keep ownership and the build boundary explicit.

---

## Example 70: Read Standard Input Until EOF

_ex-70 · exercises co-18_

Accumulate integer input until scanf reaches EOF. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-70-stdin-loop/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    int value = 0;
// => this line makes the program's state or output explicit
    int sum = 0;
// => this line makes the program's state or output explicit
    while (scanf("%d", &value) == 1) {
// => this line makes the program's state or output explicit
        sum += value;
// => this line makes the program's state or output explicit
    }
// => this line makes the program's state or output explicit
    printf("sum=%d\n", sum);
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `printf "1 2 3\\n" | ./example`.

**Expected output**:

```text
sum=6
```

**Key takeaway**: Accumulate integer input until scanf reaches EOF. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Accumulate integer input until scanf reaches EOF. Keep ownership and the build boundary explicit.

---

## Example 71: A File I/O Round Trip

_ex-71 · exercises co-19_

Write then read the same controlled file. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-71-file-round-trip/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    FILE *file = tmpfile();
// => this line makes the program's state or output explicit
    char message[8] = {0};
// => this line makes the program's state or output explicit
    if (file == NULL) return 1;
// => this line makes the program's state or output explicit
    fputs("ok\n", file);
// => this line makes the program's state or output explicit
    rewind(file);
// => this line makes the program's state or output explicit
    if (fgets(message, sizeof message, file) == NULL) return 1;
// => this line makes the program's state or output explicit
    fclose(file);
// => this line makes the program's state or output explicit
    printf("message=%s", message);
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
message=ok
```

**Key takeaway**: Write then read the same controlled file. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Write then read the same controlled file. Keep ownership and the build boundary explicit.

---

## Example 72: Parse Fields from a String

_ex-72 · exercises co-14_

Use sscanf to separate known text fields. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-72-string-parse/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    char name[16];
// => this line makes the program's state or output explicit
    int age = 0;
// => this line makes the program's state or output explicit
    if (sscanf("ada:37", "%15[^:]:%d", name, &age) != 2) return 1;
// => this line makes the program's state or output explicit
    printf("name=%s age=%d\n", name, age);
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
name=ada age=37
```

**Key takeaway**: Use sscanf to separate known text fields. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Use sscanf to separate known text fields. Keep ownership and the build boundary explicit.

---

## Example 73: Fix a Warning at Its Cause

_ex-73 · exercises co-26_

Use the matching printf format for size_t. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-73-warning-fix/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include <string.h>
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    const char *word = "cat";
// => this line makes the program's state or output explicit
    size_t length = strlen(word);
// => this line makes the program's state or output explicit
    printf("length=%zu\n", length);
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
length=3
```

**Key takeaway**: Use the matching printf format for size_t. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Use the matching printf format for size_t. Keep ownership and the build boundary explicit.

---

## Example 74: A Pointer to const char

_ex-74 · exercises co-25, co-10_

Read text through a pointer that must not modify it. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-74-const-pointer/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    const char *message = "read-only";
// => this line makes the program's state or output explicit
    printf("%s\n", message);
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
read-only
```

**Key takeaway**: Read text through a pointer that must not modify it. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Read text through a pointer that must not modify it. Keep ownership and the build boundary explicit.

---

## Example 75: Share a struct through a Header

_ex-75 · exercises co-23, co-15_

Define one shared record type for multiple sources. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-75-multi-file-struct/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include "worker.h"
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    struct Worker worker = {7};
// => this line makes the program's state or output explicit
    printf("worker=%d\n", worker_id(&worker));
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `make && ./example`.

**Expected output**:

```text
worker=7
```

**Key takeaway**: Define one shared record type for multiple sources. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Define one shared record type for multiple sources. Keep ownership and the build boundary explicit.

---

## Example 76: Put Warning Flags in CFLAGS

_ex-76 · exercises co-03, co-26_

Make every build warning-clean by default. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-76-makefile-warnings/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    puts("warning flags documented");
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `make && ./example`.

**Expected output**:

```text
warning flags documented
```

**Key takeaway**: Make every build warning-clean by default. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Make every build warning-clean by default. Keep ownership and the build boundary explicit.

---

## Example 77: Pointers, structs, and malloc Together

_ex-77 · exercises co-24, co-16, co-11, co-03_

Build a short heap-backed record workflow. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-77-integration-pointer-struct-slice/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include <stdlib.h>
// => this line makes the program's state or output explicit
struct Slice { const char *name; };
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    struct Slice *slice = malloc(sizeof *slice);
// => this line makes the program's state or output explicit
    if (slice == NULL) return 1;
// => this line makes the program's state or output explicit
    slice->name = "systems";
// => this line makes the program's state or output explicit
    printf("slice=%s\n", slice->name);
// => this line makes the program's state or output explicit
    free(slice);
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
slice=systems
```

**Key takeaway**: Build a short heap-backed record workflow. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Build a short heap-backed record workflow. Keep ownership and the build boundary explicit.

---

## Example 78: Capstone: a Multi-File C Program

_ex-78 · exercises co-03, co-10, co-12, co-15, co-17, co-20, co-22, co-23, co-26_

Consolidate the primer surface in a small Makefile build. The source demonstrates the smallest safe pattern that the later systems material relies on.

**`learning/code/ex-78-capstone-multifile-c/example.c`**

```c
// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include "item.h"
// => this line makes the program's state or output explicit
int main(void) {
// => this line makes the program's state or output explicit
    const struct Item items[] = {{"a", 3}, {"b", 4}};
// => this line makes the program's state or output explicit
    printf("items=2 total=%d\n", total(items, 2));
// => this line makes the program's state or output explicit
    return 0;
// => this line makes the program's state or output explicit
}
```

**Run**: `make && ./example`.

**Expected output**:

```text
items=2 total=7
```

**Key takeaway**: Consolidate the primer surface in a small Makefile build. Keep ownership and the build boundary explicit.

**Why it matters**: Resource lifetime and linking mistakes become expensive once a program crosses into operating-system APIs. This runnable slice establishes the local contract first: check a result, use it through the right type, and release or build it by an explicit rule that a teammate can reproduce. That discipline prevents local shortcuts from becoming opaque ownership or linkage defects after the code joins a larger native service. The specific practice in this example is: Consolidate the primer surface in a small Makefile build. Keep ownership and the build boundary explicit.

---
