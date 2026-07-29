# pyright: strict
"""Example 47: OpenTelemetry -- recording a span. (co-26)

OpenTelemetry is a vendor-neutral standard for traces, metrics, and logs. A
SPAN records one unit of work (e.g. a handler) and may have child spans.
This example simulates a tracer that records spans in-process and verifies
the span tree is captured. Source: opentelemetry.io.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-26: one recorded span in the trace
class Span:
    name: str  # => the operation this span represents
    parent: str | None  # => the parent span's name (None for the root)
    attributes: dict[str, str] = field(default_factory=dict[str, str])  # => typed span attributes


class Tracer:  # => co-26: collects spans in-process (stands in for the OTel SDK)
    def __init__(self) -> None:
        self.finished: list[Span] = []  # => spans recorded so far

    def start_as_current(self, name: str, parent: str | None = None) -> "_SpanScope":  # => begin a span
        return _SpanScope(self, name, parent)  # => a context manager that finishes the span on exit


class _SpanScope:  # => co-26: a span's lifetime -- finishes (records) on __exit__
    def __init__(self, tracer: Tracer, name: str, parent: str | None) -> None:
        self._tracer = tracer  # => the tracer to record into
        self._span = Span(name=name, parent=parent)  # => the span being recorded

    def __enter__(self) -> Span:  # => entering the scope returns the live span
        return self._span  # => callers may set attributes on it

    def __exit__(self, *_exc: object) -> None:  # => leaving the scope finishes (records) the span
        self._tracer.finished.append(self._span)  # => co-26: the span is now recorded


tracer = Tracer()  # => co-26: one trace's collector

with tracer.start_as_current("GET /orders") as root:  # => the root span -- the handler
    root.attributes["http.method"] = "GET"  # => a typed attribute on the root span
    with tracer.start_as_current("db.query", parent="GET /orders") as child:  # => a child span -- the DB call
        child.attributes["db.system"] = "sqlite"  # => a typed attribute on the child span

recorded = tracer.finished  # => the spans the tracer captured
for span in recorded:  # => print the recorded span tree
    print(f"span: {span.name}, parent={span.parent}, attrs={span.attributes}")  # => Output: two spans

# Spans are recorded as they END -- a child (db.query) ends before its parent (GET /orders).
names = {s.name for s in recorded}  # => co-26: both spans recorded (order = end-order, child first)
assert names == {"GET /orders", "db.query"}  # => co-26: both spans recorded
db_span = next(s for s in recorded if s.name == "db.query")  # => find the child span
assert db_span.parent == "GET /orders"  # => co-26: the child's parent is the root span
