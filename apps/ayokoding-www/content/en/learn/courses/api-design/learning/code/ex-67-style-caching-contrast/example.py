# pyright: strict
"""Example 67: Contrasting REST, GraphQL, and gRPC on Caching. (co-27)

REST's GET (Example 44) is cacheable by any HTTP-aware intermediary via
`Cache-Control`; GraphQL (Examples 57-62) rides over POST, which HTTP
caches never store by default; gRPC (Examples 63-66) uses a binary framing
HTTP caches cannot even parse -- this example states each fact explicitly.
"""

from dataclasses import dataclass  # => a small typed record describing each style's own caching story


@dataclass  # => co-27: one row per API style, describing its caching characteristics
class CachingProfile:  # => co-27: four fields, one row per style compared below
    style: str  # => the API style's own name
    http_method: str  # => the transport-level HTTP method it typically rides over
    cacheable_by_default: bool  # => co-27: can a generic HTTP cache store this response, unmodified?
    reason: str  # => WHY that is true or false for this style


REST_PROFILE = CachingProfile(  # => co-27: REST's own profile
    style="REST",  # => this row describes REST
    http_method="GET",  # => REST reads ride over GET (Example 3)
    cacheable_by_default=True,  # => co-27: GET + Cache-Control is exactly what caches understand
    reason="GET is safe/cacheable; Cache-Control (Example 44) is a first-class HTTP mechanism",  # => co-27
)  # => end of REST_PROFILE

GRAPHQL_PROFILE = CachingProfile(  # => co-27: GraphQL's own profile
    style="GraphQL",  # => this row describes GraphQL
    http_method="POST",  # => co-27: queries are typically sent as POST bodies, not GET query strings
    cacheable_by_default=False,  # => co-27: HTTP caches never store POST responses by default
    reason="the query lives in the POST body, invisible to a cache keyed on the URL",  # => co-27
)  # => end of GRAPHQL_PROFILE

GRPC_PROFILE = CachingProfile(  # => co-27: gRPC's own profile
    style="gRPC",  # => this row describes gRPC
    http_method="POST (HTTP/2, binary framing)",  # => co-27: gRPC always rides over HTTP/2 POST
    cacheable_by_default=False,  # => co-27: binary Protobuf frames are opaque to a generic HTTP cache
    reason="binary framing plus POST means no generic HTTP cache can parse or store it",  # => co-27
)  # => end of GRPC_PROFILE

PROFILES = [REST_PROFILE, GRAPHQL_PROFILE, GRPC_PROFILE]  # => co-27: all three, ready to compare
# => PROFILES has exactly 1 True and 2 False for cacheable_by_default -- only REST is cache-friendly
for profile in PROFILES:  # => print each style's own caching verdict
    print(f"{profile.style}: cacheable_by_default={profile.cacheable_by_default} ({profile.reason})")
    # => Output: REST=True, GraphQL=False, gRPC=False, each with its own stated reason
