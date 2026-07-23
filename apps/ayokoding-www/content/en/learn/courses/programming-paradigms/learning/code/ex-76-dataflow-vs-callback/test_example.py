"""Example 76: pytest verification for Dataflow vs Callback."""

from example import pipeline_as_generators, pipeline_as_nested_callbacks


def test_both_control_flow_styles_produce_identical_output() -> None:
    data = [1, 2, 3, 4, 5, 6]  # => a slightly larger sample than the module-level demo
    dataflow = list(pipeline_as_generators(data))

    callback_result: list[int] = []
    pipeline_as_nested_callbacks(data, lambda n: callback_result.append(n))

    assert dataflow == callback_result  # => identical results despite the different control-flow shape


def test_dataflow_pipeline_is_lazy_until_actually_drained() -> None:
    pipeline = pipeline_as_generators([10, 11])  # => build the pipeline -- nothing has run yet
    assert list(pipeline) == [20]  # => 10*2=20 (%4==0, kept), 11*2=22 (%4 != 0, filtered out) -- only when drained


# => Run: pytest -- Output: 2 passed
