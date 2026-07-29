# pyright: strict
"""Example 63: Writing a .proto Service + Messages. (co-26)

A `.proto` file declares message types and a service's RPC methods in
Protocol Buffers' own IDL -- structurally similar to Example 57's GraphQL
SDL, but describing RPC METHODS rather than a queryable graph of types.
"""

PROTO_LINES = [  # => co-26: the .proto source, built line by line so every line can be explained
    'syntax = "proto3";',  # => co-26: proto3 REQUIRES this exact declaration, first line
    "",  # => a blank line, purely for the generated source's own readability
    "message ArticleRequest {",  # => co-26: opens the request message
    "  string id = 1;",  # => co-26: field "id", assigned WIRE NUMBER 1 (never reused across versions)
    "}",  # => closes ArticleRequest
    "",  # => another blank line
    "message ArticleResponse {",  # => co-26: opens the response message
    "  string id = 1;",  # => co-26: field "id", wire number 1
    "  string title = 2;",  # => co-26: field "title", wire number 2
    "}",  # => closes ArticleResponse
    "",  # => another blank line
    "service ArticleService {",  # => co-26: opens the service -- a NAMED group of RPC methods
    "  rpc GetArticle (ArticleRequest) returns (ArticleResponse);",  # => co-26: ONE unary RPC method
    "}",  # => closes ArticleService
]  # => end of PROTO_LINES
PROTO_SOURCE = "\n".join(PROTO_LINES)  # => co-26: assembles the full .proto text from its own annotated lines


def extract_service_methods(proto_source: str) -> list[str]:  # => co-26: a tiny structural parser
    methods: list[str] = []  # => collects every "rpc MethodName (" declaration found
    for line in proto_source.splitlines():  # => co-26: scans the .proto source line by line
        stripped = line.strip()  # => trims leading/trailing whitespace
        if stripped.startswith("rpc "):  # => co-26: matches an RPC method declaration
            method_name = stripped.removeprefix("rpc ").split(" ")[0]  # => extracts just the method name
            methods.append(method_name)  # => co-26: records this RPC's own name
    return methods  # => every RPC method name the service declares


def proto_compiles(proto_source: str) -> bool:  # => co-26: a minimal "does this look valid" check
    has_syntax_decl = "syntax = " in proto_source  # => co-26: proto3 requires an explicit syntax line
    balanced_braces = proto_source.count("{") == proto_source.count("}")  # => structural sanity check
    return has_syntax_decl and balanced_braces  # => both conditions must hold


methods = extract_service_methods(PROTO_SOURCE)  # => co-26: parses the service's own declared methods
print(f"declared RPC methods: {methods}")  # => Output: ['GetArticle']

compiles = proto_compiles(PROTO_SOURCE)  # => co-26: verifies the .proto source is at least well-formed
# => compiles is True (type: bool) -- syntax line present, and every brace closes
print(f".proto compiles: {compiles}")  # => Output: True
