// learning/code/ex-43-virtual-address-print/virtual_address.c
/* Example 43: map the SAME fixed virtual address in a parent and a forked
   child -- verify both processes see IDENTICAL address VALUES backed by
   INDEPENDENT physical pages (co-08). VERIFIED CAVEAT (found while building
   this example): a plain post-fork malloc() does NOT reliably reproduce
   this on macOS -- Apple's libmalloc reinitializes/switches allocator
   zones in the forked child for lock-safety reasons, so parent/child heap
   addresses land in DIFFERENT allocator regions even though both inherited
   the identical address space at fork time. mmap's MAP_FIXED sidesteps
   that allocator-internal behavior and demonstrates the OS-level concept
   directly and deterministically. */
#include <stdio.h>    // => printf/fflush -- the address/value report this program prints
#include <stdlib.h>   // => exit codes
#include <sys/mman.h> // => co-08: mmap/MAP_FIXED -- request the SAME virtual address in both processes
#include <sys/wait.h> // => waitpid -- the parent's cleanup of the forked child
#include <unistd.h>   // => co-08: fork -- creates a second, INDEPENDENT process

// co-08: a fixed target address, chosen well above the addresses this program's
// own text/heap/stack/default-mmap regions occupy (verified empirically:
// default anonymous mmaps on this machine land near 0x104xxxxxx; 0x200000000 is
// comfortably clear of that).
#define FIXED_ADDR ((void *)0x200000000UL) // constant FIXED_ADDR = ((void *)0x200000000UL)
#define MAP_SIZE 4096                      // constant MAP_SIZE = 4096

int main(void) {        // program entry point
    pid_t pid = fork(); // => co-08: from this line on, TWO separate
    if (pid < 0) {
        perror("fork");
        return 1;
    } //    virtual address spaces exist
    if (pid == 0) { // conditional check
        // co-08: CHILD -- requests the SAME fixed address the parent will ALSO
        // request below. MAP_FIXED tells the kernel "map it exactly HERE, in MY
        // address space" -- it says nothing about the parent's mapping, because
        // there IS no shared mapping between them.
        void *m = mmap(FIXED_ADDR, MAP_SIZE, PROT_READ | PROT_WRITE,
                       MAP_FIXED | MAP_ANON | MAP_PRIVATE, // declares m
                       -1, 0);                             // supporting statement for this example
        if (m == MAP_FAILED) {
            perror("child mmap");
            fflush(stdout);
            _exit(1);
        } // conditional check
        *(int *)m = 222;                                    // => co-08: write a value ONLY the child ever sees
        printf("child : addr=%p value=%d\n", m, *(int *)m); // prints a report line
        fflush(stdout);                                     // => co-08: _exit() below skips stdio flushing --
        _exit(0);                                           //    must flush explicitly or this line vanishes
    }

    // co-08: PARENT -- requests the IDENTICAL fixed address, in its OWN,
    // independent address space (unrelated to whatever the child already did with
    // that same number).
    int status = 0;                                                                                      // declares status
    waitpid(pid, &status, 0);                                                                            // => let the child finish and print first
    void *m = mmap(FIXED_ADDR, MAP_SIZE, PROT_READ | PROT_WRITE, MAP_FIXED | MAP_ANON | MAP_PRIVATE, -1, // declares m
                   0);                                                                                   // supporting statement for this example
    if (m == MAP_FAILED) {
        perror("parent mmap");
        return 1;
    } // conditional check
    *(int *)m = 111;                                    // => co-08: write a DIFFERENT value than the child's
    printf("parent: addr=%p value=%d\n", m, *(int *)m); // prints a report line
    int matches_target = (m == FIXED_ADDR);             // => co-08: the parent really got the requested address
    printf("both processes requested %p; parent got it: %s\n",
           FIXED_ADDR,                     // prints a report line
           matches_target ? "yes" : "no"); // continues the printf(...) call above
    printf(                                // prints a report line
        "same virtual address VALUE, independent processes, independent physical "
        "pages:\n" // continues the printf(...) call above
        "  parent sees value=%d at %p; child independently saw value=222 at the "
        "SAME address\n" // continues the printf(...) call above
        "  -> %s\n",     // continues the printf(...) call above
        *(int *)m, m,
        (matches_target && *(int *)m == 111) ? "PASS" : "FAIL"); // continues the printf(...) call above
    return (matches_target && *(int *)m == 111) ? 0 : 1;         // returns the computed result
}
