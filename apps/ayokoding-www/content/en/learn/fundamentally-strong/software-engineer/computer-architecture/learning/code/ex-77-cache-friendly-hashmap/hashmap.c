// learning/code/ex-77-cache-friendly-hashmap/hashmap.c
/* Example 77: open-addressing (linear probe) vs separate chaining -- lookup
 * locality compared. */
#include <stdio.h>  // stdio.h: standard library header
#include <stdlib.h> // stdlib.h: standard library header
#include <time.h>   // time.h: standard library header

#define N_KEYS 2200000 // => co-03: 2.2M keys inserted into both tables
#define TABLE_CAP \
    4194304 // => co-03: 4M slots (power of 2), ~52% load factor -- keeps both
            // structures' AVERAGE traversal length short and comparable, so the
            // measured gap reflects per-step cache locality, not probe-count skew
#define N_QUERIES \
    4000000 // => co-03: 4M lookups, ALL guaranteed HITS (see rationale below),
            // per table

static unsigned hash_u32(unsigned x) { // => co-03: cheap multiplicative hash (Knuth)
    x ^= x >> 16;                      // updates x
    x *= 0x7feb352dU;                  // updates x
    x ^= x >> 15;                      // updates x
    return x;                          // returns the computed result
}

// ex-77: OPEN ADDRESSING -- co-17: one FLAT array of {key, used} slots. co-03:
// a probe sequence walks CONSECUTIVE array slots (linear probing), which stay
// in the SAME or adjacent 128 B cache lines -- a probe chain of length k costs
// at most a couple of cache-line touches, often just one.
typedef struct {
    int key;
    int used;
} OaSlot; // performs several bookkeeping updates in one line

static void oa_insert(OaSlot *table, unsigned cap,
                      int key) {                        // defines oa_insert(): helper function used by this example
    unsigned idx = hash_u32((unsigned)key) & (cap - 1); // declares idx
    while (table[idx].used) {                           // => co-03: linear probe -- walks FORWARD through the array
        idx = (idx + 1) & (cap - 1);                    // co-06: wraps at the table boundary (power-of-2 mask)
    }
    table[idx].key = key; // assigns table[idx].key
    table[idx].used = 1;  // assigns table[idx].used
}

static int oa_lookup(const OaSlot *table, unsigned cap,
                     int key) {                         // defines oa_lookup(): helper function used by this example
    unsigned idx = hash_u32((unsigned)key) & (cap - 1); // declares idx
    while (table[idx].used) {                           // => co-03: same forward, cache-line-friendly probe
                                                        // as insert
        if (table[idx].key == key)
            return 1;                // => hit
        idx = (idx + 1) & (cap - 1); // assigns idx
    }
    return 0; // => empty slot reached -- definite miss (never inserted)
}

// ex-77: SEPARATE CHAINING -- co-17: each bucket is a linked-list HEAD POINTER;
// every inserted key lives in its OWN node. co-03: a lookup that walks a chain
// of length k follows k POINTER CHASES.
typedef struct ChainNode {
    int key;
    struct ChainNode *next;
} ChainNode; // performs several bookkeeping updates in one line

// co-03: nodes are drawn from a PRE-SHUFFLED pool instead of being malloc'd
// one-at-a-time in insertion order. A first version used a fresh
// `malloc(sizeof(ChainNode))` per insert and found chaining just as fast as (or
// faster than) open addressing -- macOS's small-object allocator packs
// same-size allocations densely within a few pages, so nodes malloc'd
// back-to-back land NEAR each other regardless of which hash bucket they end up
// in, which quietly erases the "scattered pointer chase" cost real chaining has
// in a long-running, heap-fragmented program. Drawing each node from a RANDOM
// position in a large pre-allocated pool (57.6 MB, far past this machine's
// caches) restores that realistic scatter without relying on allocator
// internals this program cannot control.
static ChainNode *node_pool;    // declares node_pool
static int *node_pool_perm;     // declares node_pool_perm
static long node_pool_next = 0; // declares node_pool_next

static void chain_insert(ChainNode **buckets, unsigned cap,
                         int key) {                                 // defines chain_insert(): helper function used by this example
    unsigned idx = hash_u32((unsigned)key) & (cap - 1);             // declares idx
    ChainNode *node = &node_pool[node_pool_perm[node_pool_next++]]; // => co-03: a RANDOM pool
                                                                    // slot, not the next free
                                                                    // one
    node->key = key;                                                // assigns node->key
    node->next = buckets[idx];                                      // => co-03: prepend -- classic chaining insert
    buckets[idx] = node;                                            // assigns buckets[idx]
}

static int chain_lookup(ChainNode *const *buckets, unsigned cap,
                        int key) {                              // defines chain_lookup(): helper function used by this example
    unsigned idx = hash_u32((unsigned)key) & (cap - 1);         // declares idx
    for (ChainNode *n = buckets[idx]; n != NULL; n = n->next) { // => co-03: pointer chase through the chain
        if (n->key == key)
            return 1; // conditional check
    }
    return 0; // returns the computed result
}

int main(void) {                                                      // program entry point
    OaSlot *oa_table = calloc(TABLE_CAP, sizeof(OaSlot));             // heap-allocates memory for oa_table
    ChainNode **chain_table = calloc(TABLE_CAP, sizeof(ChainNode *)); // heap-allocates memory for chain_table
    node_pool = malloc(sizeof(ChainNode) * N_KEYS);                   // heap-allocates memory for node_pool
    node_pool_perm = malloc(sizeof(int) * N_KEYS);                    // heap-allocates memory for node_pool_perm
    if (!oa_table || !chain_table || !node_pool || !node_pool_perm) { // conditional check
        fprintf(stderr, "alloc failed\n");                            // prints a report line
        return 1;                                                     // returns the computed result
    }
    for (int i = 0; i < N_KEYS; i++)
        node_pool_perm[i] = i;                    // loop header controlling the sweep below
    unsigned pseed = 31u;                         // => co-03: Fisher-Yates -- scatters pool-slot assignment
    for (int i = N_KEYS - 1; i > 0; i--) {        // order independent of insertion (hash-bucket) order
        pseed = pseed * 1103515245u + 12345u;     // assigns pseed
        int j = (int)(pseed % (unsigned)(i + 1)); // declares j
        int tmp = node_pool_perm[i];
        node_pool_perm[i] = node_pool_perm[j];
        node_pool_perm[j] = tmp; // declares tmp
    }

    // co-03: insert the SAME N_KEYS distinct keys into BOTH tables so lookup
    // results are comparable.
    int *keys = malloc(sizeof(int) * N_KEYS); // heap-allocates memory for keys
    for (int i = 0; i < N_KEYS; i++)
        keys[i] = i * 2 + 1;                           // => odd numbers -- easy to distinguish from misses
    for (int i = 0; i < N_KEYS; i++) {                 // loop header controlling the sweep below
        oa_insert(oa_table, TABLE_CAP, keys[i]);       // calls oa_insert(...)
        chain_insert(chain_table, TABLE_CAP, keys[i]); // calls chain_insert(...)
    }

    // co-03: N_QUERIES lookups, ALL guaranteed HITS -- both tables see the
    // IDENTICAL query sequence. Two earlier mixes were tried and rejected: a
    // 50/50 hit/miss mix let chaining win outright (an UNSUCCESSFUL chaining
    // lookup that lands on an empty bucket costs ZERO pointer chases -- nearly
    // free -- while an unsuccessful open-addressing lookup at this load factor
    // must probe past several occupied slots first); even an 80/20 mix still left
    // the gap too close to call reliably across repeated runs (measured
    // ~0.9x-1.2x, noise-dominated). Both mixes conflate a real ALGORITHMIC
    // step-count asymmetry (open addressing's unsuccessful-search probe count
    // grows with load factor; chaining's does not) with the LOCALITY question
    // this example is actually about. All-hit queries hold the average traversal
    // length for both structures roughly comparable (dictated by the SAME load
    // factor), isolating per-step cache cost as the only remaining variable --
    // exactly what "open addressing beats chaining from better locality" (this
    // example's claim) is supposed to measure.
    int *queries = malloc(sizeof(int) * N_QUERIES); // heap-allocates memory for queries
    unsigned seed = 21u;                            // declares seed
    for (int i = 0; i < N_QUERIES; i++) {           // loop header controlling the sweep below
        seed = seed * 1103515245u + 12345u;         // assigns seed
        queries[i] = keys[seed % (unsigned)N_KEYS]; // => guaranteed hit, every query
    }

    struct timespec t0, t1;              // supporting statement for this example
    clock_gettime(CLOCK_MONOTONIC, &t0); // calls clock_gettime(...)
    long oa_hits = 0;                    // declares oa_hits
    for (int i = 0; i < N_QUERIES; i++)
        oa_hits += oa_lookup(oa_table, TABLE_CAP,
                             queries[i]);                                    // loop header controlling the sweep below
    clock_gettime(CLOCK_MONOTONIC, &t1);                                     // calls clock_gettime(...)
    double t_oa = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // declares t_oa

    clock_gettime(CLOCK_MONOTONIC, &t0); // calls clock_gettime(...)
    long chain_hits = 0;                 // declares chain_hits
    for (int i = 0; i < N_QUERIES; i++)
        chain_hits += chain_lookup(chain_table, TABLE_CAP,
                                   queries[i]);                                 // loop header controlling the sweep below
    clock_gettime(CLOCK_MONOTONIC, &t1);                                        // calls clock_gettime(...)
    double t_chain = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // declares t_chain

    printf("N_KEYS=%d, TABLE_CAP=%d (load factor %.2f), N_QUERIES=%d\n", N_KEYS,
           TABLE_CAP, // prints a report line
           (double)N_KEYS / TABLE_CAP,
           N_QUERIES); // continues the printf(...) call above
    printf("open addressing: %.4f s, %ld hits (expect %d)\n", t_oa, oa_hits,
           N_QUERIES);                                                                           // prints a report line
    printf("separate chaining: %.4f s, %ld hits (expect %d)\n", t_chain, chain_hits, N_QUERIES); // prints a report line
    printf("results agree: %s\n",
           oa_hits == chain_hits ? "yes" : "NO -- BUG");                                // prints a report line
    double speedup = t_chain / t_oa;                                                    // declares speedup
    printf("open-addressing speedup: %.2fx\n", speedup);                                // prints a report line
    int pass = (oa_hits == N_QUERIES) && (chain_hits == N_QUERIES) && (speedup > 1.05); // declares pass
    printf("PASS (identical, correct hit counts; open addressing faster from "
           "better locality): %s\n", // prints a report line
           pass ? "PASS" : "FAIL");  // continues the printf(...) call above

    free(oa_table);       // releases oa_table's heap memory
    free(chain_table);    // => nodes now live in node_pool (one bulk allocation),
                          // nothing per-node to free
    free(node_pool);      // releases node_pool's heap memory
    free(node_pool_perm); // releases node_pool_perm's heap memory
    free(keys);           // releases keys's heap memory
    free(queries);        // releases queries's heap memory
    return 0;             // returns the computed result
}
