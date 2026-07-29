# pyright: strict
"""Example 78: Measuring gRPC vs REST Round-Trip. (co-27)

No real network call runs in a self-contained script -- so this example
measures a HONEST proxy instead: encoded PAYLOAD SIZE, the dominant factor
in round-trip time on a real network. JSON (REST) stands in for text-based
encoding; a compact fixed-width encoding stands in for Protobuf's binary framing.
"""

import json  # => stdlib: measures REST's actual JSON encoding size
import struct  # => stdlib: builds a compact binary encoding, standing in for Protobuf

ARTICLE: dict[str, object] = {"id": 1, "title": "Hello", "views": 42}  # => co-27: same data, encoded two ways


def rest_json_size(article: dict[str, object]) -> int:  # => co-27: REST's own encoding -- JSON text
    encoded = json.dumps(article).encode("utf-8")  # => co-27: a normal JSON payload, as bytes over the wire
    return len(encoded)  # => co-27: the number of bytes REST actually sends


def grpc_binary_size(article_id: int, title: str, views: int) -> int:  # => co-27: a Protobuf-like binary stand-in
    title_bytes = title.encode("utf-8")  # => the variable-length string field
    fixed_part = struct.pack(">ii", article_id, views)  # => co-27: two fixed-width 4-byte integers, no field names
    return len(fixed_part) + len(title_bytes)  # => co-27: no repeated key names, unlike JSON's "id":/"title":


json_bytes = rest_json_size(ARTICLE)  # => co-27: measures REST's own encoded size
print(f"REST (JSON) payload size: {json_bytes} bytes")  # => Output: includes repeated field-name text

binary_bytes = grpc_binary_size(1, "Hello", 42)  # => co-27: measures the binary stand-in's encoded size
print(f"gRPC (binary) payload size: {binary_bytes} bytes")  # => Output: smaller -- no repeated field names

savings_percent = round((1 - binary_bytes / json_bytes) * 100)  # => co-27: the proxy for latency advantage
# => savings_percent is a positive int -- smaller payloads mean fewer bytes to serialize/transmit/parse
print(f"binary encoding is ~{savings_percent}% smaller")  # => Output: a concrete, honest, reproducible number
