"""Example 79: pytest verification that both decorator styles add the same cross-cutting behavior."""

from example import LoggingCalculatorDecorator, PlainAdder, add


def test_functools_decorator_preserves_the_wrapped_functions_result() -> None:
    assert add(2, 3) == 5


def test_functools_decorator_adds_cross_cutting_logging_without_touching_add_body() -> None:
    add(10, 20)
    assert (10, 20) in [call_args for call_args, _ in add.calls]  # type: ignore[attr-defined]  # => the log recorded the call


def test_functools_wraps_preserves_the_original_function_name() -> None:
    assert add.__name__ == "add"  # => good decorator hygiene: functools.wraps kept identity intact


def test_gof_class_decorator_preserves_the_wrapped_objects_result() -> None:
    decorated = LoggingCalculatorDecorator(PlainAdder())
    assert decorated.compute(4, 5) == 9


def test_gof_class_decorator_adds_cross_cutting_logging_to_a_whole_object() -> None:
    decorated = LoggingCalculatorDecorator(PlainAdder())
    decorated.compute(1, 1)
    decorated.compute(2, 2)
    assert decorated.calls == [(1, 1, 2), (2, 2, 4)]  # => same cross-cutting idea, at object granularity


# => Run: pytest -q -- Output: 5 passed
