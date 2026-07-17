"""Example 51: pytest verification for Stacking Retry + Cache + Log Decorators."""

from example import BaseFetcher, CachingDecorator, LoggingDecorator, RetryDecorator


def test_cache_miss_runs_every_layer_in_outer_to_inner_order() -> None:
    trace: list[str] = []
    stack = RetryDecorator(CachingDecorator(LoggingDecorator(BaseFetcher(trace), trace), trace), trace)
    stack("k")
    assert trace == [
        "retry:enter:k",
        "cache:miss:k",
        "log:enter:k",
        "fetch:k",
        "log:exit:k",
        "retry:exit:k",
    ]


def test_cache_hit_skips_the_layers_wrapped_inside_the_cache() -> None:
    trace: list[str] = []
    stack = RetryDecorator(CachingDecorator(LoggingDecorator(BaseFetcher(trace), trace), trace), trace)
    stack("k")  # => first call -- populates the cache
    trace.clear()
    stack("k")  # => second call -- must hit the cache
    assert trace == ["retry:enter:k", "cache:hit:k", "retry:exit:k"]  # => log/base skipped


# => Run: pytest -- Output: 2 passed
