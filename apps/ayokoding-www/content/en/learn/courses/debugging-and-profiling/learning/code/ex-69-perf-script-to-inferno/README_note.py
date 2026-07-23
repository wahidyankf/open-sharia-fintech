"""Example 69: `inferno-collapse-perf` + `inferno-flamegraph` regenerate the
SAME flame graph as ex-68's Perl scripts, from `perf script` output -- same
real Linux-only unavailability as ex-67/ex-68 for the SOURCE data. The
DOWNSTREAM tool, `inferno-flamegraph`, is real, installed (via
`cargo install inferno`), and already independently verified against
gprof2dot in ex-53, and against cProfile's own ranking in ex-30 -- the
"same widest frame, tool-independent" property this example asks for is
the exact property ex-53 verifies, just with `perf` swapped for
`gprof2dot` as the second, independent tool (since `perf` itself cannot run
here).
"""
