# pyright: strict
"""Example 48: W3C Trace Context -- traceparent propagation. (co-26)

A W3C `traceparent` header (version-traceid-spanid-flags) carries the trace
identity across a service-to-service call so a request can be followed across
services. The downstream service extracts the SAME trace id. Source: W3C
Trace Context (Recommendation, 2021).
"""

from dataclasses import dataclass  # => a small typed record for a propagated context


@dataclass(frozen=True)  # => co-26: the identity propagated across one hop
class TraceContext:
    trace_id: str  # => the trace id -- the SAME across every hop in one request
    span_id: str  # => the span id -- a NEW one per hop
    flags: str  # => trace flags (e.g. sampled)


def make_traceparent(ctx: TraceContext) -> str:  # => co-26: serialize the context into the header
    return f"00-{ctx.trace_id}-{ctx.span_id}-{ctx.flags}"  # => version-traceid-spanid-flags


def parse_traceparent(header: str) -> TraceContext | None:  # => co-26: extract the context on the downstream side
    parts = header.split("-")  # => split the 4 dash-separated fields
    if len(parts) != 4:  # => malformed -> no context
        return None  # => reject
    _version, trace_id, span_id, flags = parts  # => the four fields
    return TraceContext(trace_id=trace_id, span_id=span_id, flags=flags)  # => the extracted context


# The upstream service starts a trace and propagates it to a downstream call.
upstream = TraceContext(trace_id="0af7651916cd43dd8448eb211c80319c", span_id="00f067aa0ba902b7", flags="01")  # => co-26
header = make_traceparent(upstream)  # => the traceparent header sent across the hop
print(f"upstream sends traceparent: {header}")  # => Output: the serialized header

# The downstream service receives the SAME trace id but records a NEW span id.
received = parse_traceparent(header)  # => co-26: extract on the downstream side
assert received is not None  # => type-narrow
downstream = TraceContext(trace_id=received.trace_id, span_id="e90a8f19a8bc4019", flags=received.flags)  # => new span, same trace
print(f"downstream trace_id: {downstream.trace_id}")  # => Output: the SAME trace id
print(f"downstream span_id:  {downstream.span_id} (new)")  # => Output: a NEW span id

assert downstream.trace_id == upstream.trace_id  # => co-26: the trace id is PRESERVED across the hop
assert downstream.span_id != upstream.span_id  # => co-26: each hop records its own span id
