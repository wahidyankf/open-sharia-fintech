"""Example 54: pytest verification for Template Method vs Strategy."""

from example import (
    PipelineWithStrategy,
    ReversePipeline,
    UppercasePipeline,
    reverse_strategy,
    uppercase_strategy,
)


def test_template_method_behavior_is_fixed_per_subclass() -> None:
    assert UppercasePipeline().run("  hello  ") == "saved:HELLO"
    assert ReversePipeline().run("  hello  ") == "saved:olleh"


def test_strategy_swaps_behavior_at_runtime_on_one_instance() -> None:
    pipeline: PipelineWithStrategy = PipelineWithStrategy(uppercase_strategy)
    assert pipeline.run("  hello  ") == "saved:HELLO"
    pipeline.strategy = reverse_strategy  # => no new instance, no new subclass
    assert pipeline.run("  hello  ") == "saved:olleh"  # => same instance, new behavior


# => Run: pytest -- Output: 2 passed
