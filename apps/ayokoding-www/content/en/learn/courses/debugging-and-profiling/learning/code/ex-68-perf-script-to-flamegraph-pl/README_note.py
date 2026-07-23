"""Example 68: `stackcollapse-perf.pl` + `flamegraph.pl` convert REAL `perf
script` text output into a folded-stack SVG flame graph. `perf` itself is a
Linux-kernel-only tool (it reads /proc and the kernel's perf_events subsystem,
neither of which exist on Darwin/macOS) -- this example's honest limitation
carries forward from ex-67, since there is no `perf script` output to feed
these two Perl scripts on this host. ex-53, ex-21, and ex-30 already
demonstrate the SAME "folded stacks -> flame-graph SVG" pipeline end-to-end,
real and tool-independent, using the mini_sampler substitute's own collapsed
format (which is deliberately the same folded-stack text format
stackcollapse-perf.pl itself produces) -- see those examples for the real,
working half of this pipeline.
"""
