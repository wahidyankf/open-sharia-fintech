// learning/code/ex-60-particle-sim-soa-simd/particles.c
/* Example 60: particle-system position update -- AoS scalar vs SoA scalar vs
 * SoA+NEON. */
#include <arm_neon.h> // => co-23: NEON intrinsics -- this machine is arm64, so NEON is the real SIMD ISA
#include <stdio.h>    // stdio.h: standard library header
#include <stdlib.h>   // stdlib.h: standard library header
#include <time.h>     // time.h: standard library header

#define N 4000000 // => co-17: 4M particles
#define STEPS \
    20           // => repeat the update this many times per timed run (amplifies the
                 // signal)
#define DT 0.01f // constant DT = 0.01f

// ex-60: AoS particle -- position and velocity interleaved per particle, plus
// one cold "mass" field never touched by this position-update kernel (co-17:
// realistic AoS shape)
typedef struct {      // struct layout definition
    float x, y, z;    // => position -- updated every step
    float vx, vy, vz; // => velocity -- read every step, never written here
    float mass;       // => co-17: cold field -- part of the record, irrelevant to this
                      // kernel
} ParticleAoS;        // supporting statement for this example

// clang's auto-vectorizer can still find some parallelism in AoS at -O2;
// disabling it here keeps this a clean apples-to-apples "scalar work, different
// layout" baseline (stated in prose).
static void update_aos(ParticleAoS *p, int n,
                       float dt) {                        // defines update_aos(): helper function used by this example
#pragma clang loop vectorize(disable) interleave(disable) // supporting statement for this example
    for (int i = 0; i < n; i++) {                         // => co-17: each iteration loads a full 28 B particle
        p[i].x += p[i].vx * dt;                           // to update 3 of its 7 floats -- the rest rides along
        p[i].y += p[i].vy * dt;                           // updates p[i].y
        p[i].z += p[i].vz * dt;                           // updates p[i].z
    }
}

// ex-60: SoA particle system -- position and velocity as six separate dense
// arrays. co-17: only the arrays this kernel actually touches (x/y/z, vx/vy/vz)
// are ever loaded -- there is no "mass" array to pay for in this loop at all.
typedef struct {                     // struct layout definition
    float *x, *y, *z, *vx, *vy, *vz; // declares x
} ParticleSoA;                       // supporting statement for this example

// Also forced non-vectorized (see note above ex ex-60's AoS version): this
// isolates the explicit-NEON win below from clang's own auto-vectorizer, which
// would otherwise blur the AoS-vs-SoA-vs-explicit-SIMD comparison this example
// is actually about. ex-47 already covers auto-vectorization on its own.
static void update_soa_scalar(ParticleSoA *p, int n,
                              float dt) {                 // defines update_soa_scalar(): helper
                                                          // function used by this example
#pragma clang loop vectorize(disable) interleave(disable) // supporting statement for this example
    for (int i = 0; i < n; i++) {                         // => co-03: each array is streamed
                                                          // sequentially, dense and separate
        p->x[i] += p->vx[i] * dt;                         // updates p->x[i]
        p->y[i] += p->vy[i] * dt;                         // updates p->y[i]
        p->z[i] += p->vz[i] * dt;                         // updates p->z[i]
    }
}

// ex-60: SoA + NEON -- because each particle's update is INDEPENDENT of every
// other particle's (no cross-particle dependency), 4 particles' worth of one
// axis can be updated in a single `vld1q_f32`/`vmlaq_f32`/`vst1q_f32` sequence
// -- co-23: this is exactly the data-parallel shape SIMD wants, and SoA is what
// MAKES it expressible: AoS's interleaved x,y,z,vx,vy,vz,mass fields cannot be
// loaded 4-at-a-time this cleanly.
static void update_soa_simd(ParticleSoA *p, int n,
                            float dt) {        // defines update_soa_simd(): helper
                                               // function used by this example
    float32x4_t vdt = vdupq_n_f32(dt);         // => co-23: broadcast dt into all 4 lanes once
    int i = 0;                                 // declares i
    for (; i + 4 <= n; i += 4) {               // => co-23: process 4 particles per axis per iteration
        float32x4_t x = vld1q_f32(&p->x[i]);   // => load 4 positions
        float32x4_t vx = vld1q_f32(&p->vx[i]); // => load 4 velocities
        x = vmlaq_f32(x, vx,
                      vdt);     // => x = x + vx*dt for all 4 lanes in one instruction
        vst1q_f32(&p->x[i], x); // => store 4 results back

        float32x4_t y = vld1q_f32(&p->y[i]);   // declares y
        float32x4_t vy = vld1q_f32(&p->vy[i]); // declares vy
        y = vmlaq_f32(y, vy, vdt);             // assigns y
        vst1q_f32(&p->y[i], y);                // calls vst1q_f32(...)

        float32x4_t z = vld1q_f32(&p->z[i]);   // declares z
        float32x4_t vz = vld1q_f32(&p->vz[i]); // declares vz
        z = vmlaq_f32(z, vz, vdt);             // assigns z
        vst1q_f32(&p->z[i], z);                // calls vst1q_f32(...)
    }
    for (; i < n; i++) {          // => co-23: scalar tail for n not a multiple of 4
        p->x[i] += p->vx[i] * dt; // updates p->x[i]
        p->y[i] += p->vy[i] * dt; // updates p->y[i]
        p->z[i] += p->vz[i] * dt; // updates p->z[i]
    }
}

static double best_of3(void (*run)(void *, int, float, int), void *ctx,
                       int n) {                                                  // declares function pointer run
    double best = -1.0;                                                          // declares best
    for (int t = 0; t < 7; t++) {                                                // loop header controlling the sweep below
        struct timespec t0, t1;                                                  // supporting statement for this example
        clock_gettime(CLOCK_MONOTONIC, &t0);                                     // calls clock_gettime(...)
        run(ctx, n, DT, STEPS);                                                  // calls run(...)
        clock_gettime(CLOCK_MONOTONIC, &t1);                                     // calls clock_gettime(...)
        double secs = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9; // declares secs
        if (best < 0 || secs < best)
            best = secs; // conditional check
    }
    return best; // returns the computed result
}

static void run_aos(void *ctx, int n, float dt,
                    int steps) {         // defines run_aos(): helper function used by this example
    ParticleAoS *p = (ParticleAoS *)ctx; // declares p
    for (int s = 0; s < steps; s++)
        update_aos(p, n, dt); // loop header controlling the sweep below
}
static void run_soa_scalar(void *ctx, int n, float dt,
                           int steps) {  // defines run_soa_scalar(): helper
                                         // function used by this example
    ParticleSoA *p = (ParticleSoA *)ctx; // declares p
    for (int s = 0; s < steps; s++)
        update_soa_scalar(p, n, dt); // loop header controlling the sweep below
}
static void run_soa_simd(void *ctx, int n, float dt,
                         int steps) {    // defines run_soa_simd(): helper function used by this example
    ParticleSoA *p = (ParticleSoA *)ctx; // declares p
    for (int s = 0; s < steps; s++)
        update_soa_simd(p, n, dt); // loop header controlling the sweep below
}

int main(void) {                                        // program entry point
    ParticleAoS *aos = malloc(sizeof(ParticleAoS) * N); // heap-allocates memory for aos
    ParticleSoA soa_scalar = {malloc(sizeof(float) * N), malloc(sizeof(float) * N),
                              malloc(sizeof(float) * N),                                                        // declares soa_scalar
                              malloc(sizeof(float) * N), malloc(sizeof(float) * N), malloc(sizeof(float) * N)}; // calls malloc(...)
    ParticleSoA soa_simd = {malloc(sizeof(float) * N), malloc(sizeof(float) * N),
                            malloc(sizeof(float) * N),                                                        // declares soa_simd
                            malloc(sizeof(float) * N), malloc(sizeof(float) * N), malloc(sizeof(float) * N)}; // calls malloc(...)
    if (!aos || !soa_scalar.x || !soa_simd.x) {                                                               // => guards all three allocation groups at once
        fprintf(stderr, "alloc failed\n");                                                                    // => reports to stderr, not stdout
        return 1;                                                                                             // => nonzero exit -- allocation failure is not this example's claim
    } // prints a report line

    unsigned seed = 42u;                                             // declares seed
    for (int i = 0; i < N; i++) {                                    // loop header controlling the sweep below
        seed = seed * 1103515245u + 12345u;                          // assigns seed
        float x = (float)(seed % 1000u) * 0.01f;                     // declares x
        seed = seed * 1103515245u + 12345u;                          // assigns seed
        float vx = (float)(seed % 100u) * 0.001f;                    // declares vx
        aos[i].x = aos[i].y = aos[i].z = x;                          // => identical starting state across all 3 variants
        aos[i].vx = aos[i].vy = aos[i].vz = vx;                      // assigns aos[i].vx
        aos[i].mass = 1.0f;                                          // assigns aos[i].mass
        soa_scalar.x[i] = soa_scalar.y[i] = soa_scalar.z[i] = x;     // assigns soa_scalar.x[i]
        soa_scalar.vx[i] = soa_scalar.vy[i] = soa_scalar.vz[i] = vx; // assigns soa_scalar.vx[i]
        soa_simd.x[i] = soa_simd.y[i] = soa_simd.z[i] = x;           // assigns soa_simd.x[i]
        soa_simd.vx[i] = soa_simd.vy[i] = soa_simd.vz[i] = vx;       // assigns soa_simd.vx[i]
    }

    double t_aos = best_of3(run_aos, aos, N);                // declares t_aos
    double t_soa = best_of3(run_soa_scalar, &soa_scalar, N); // declares t_soa
    double t_simd = best_of3(run_soa_simd, &soa_simd, N);    // declares t_simd

    // co-17/co-23: correctness -- all 3 variants ran the SAME dt/steps from the
    // SAME initial state, and each particle's update is independent, so every
    // variant must land on the same x within a small float tolerance (SIMD lane
    // order doesn't change any single lane's own arithmetic).
    double max_diff = 0.0;                                      // declares max_diff
    for (int i = 0; i < N; i++) {                               // loop header controlling the sweep below
        double d1 = (double)aos[i].x - (double)soa_scalar.x[i]; // declares d1
        double d2 = (double)aos[i].x - (double)soa_simd.x[i];   // declares d2
        if (d1 < 0)
            d1 = -d1; // conditional check
        if (d2 < 0)
            d2 = -d2; // conditional check
        if (d1 > max_diff)
            max_diff = d1; // conditional check
        if (d2 > max_diff)
            max_diff = d2; // conditional check
    }

    printf("N=%d particles, %d steps, dt=%.2f\n", N, STEPS,
           DT);                                            // prints a report line
    printf("AoS scalar:    best of 7 = %.4f s\n", t_aos);  // prints a report line
    printf("SoA scalar:    best of 7 = %.4f s\n", t_soa);  // prints a report line
    printf("SoA+NEON SIMD: best of 7 = %.4f s\n", t_simd); // prints a report line
    printf("max |x diff| across all 3 variants, all particles: %.9f\n",
           max_diff); // prints a report line
    printf("SoA+SIMD vs AoS speedup: %.2fx\n",
           t_aos / t_simd); // prints a report line
    printf("SoA+SIMD vs SoA-scalar speedup: %.2fx\n",
           t_soa / t_simd);                                               // prints a report line
    int pass = (max_diff < 1e-3) && (t_simd < t_soa) && (t_simd < t_aos); // declares pass
    printf("PASS (SoA+SIMD fastest, results agree): %s\n",
           pass ? "PASS" : "FAIL"); // prints a report line

    free(aos);           // releases aos's heap memory
    free(soa_scalar.x);  // releases soa_scalar.x
    free(soa_scalar.y);  // releases soa_scalar.y
    free(soa_scalar.z);  // releases soa_scalar's heap memory
    free(soa_scalar.vx); // releases soa_scalar.vx
    free(soa_scalar.vy); // releases soa_scalar.vy
    free(soa_scalar.vz); // releases soa_scalar's heap memory
    free(soa_simd.x);    // releases soa_simd.x
    free(soa_simd.y);    // releases soa_simd.y
    free(soa_simd.z);    // releases soa_simd's heap memory
    free(soa_simd.vx);   // releases soa_simd.vx
    free(soa_simd.vy);   // releases soa_simd.vy
    free(soa_simd.vz);   // releases soa_simd's heap memory
    return 0;            // returns the computed result
}
