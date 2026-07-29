# pyright: strict
"""Example 70: Writing the OpenAPI Spec Before Any Code. (co-09, co-14)

Contract-first means the OpenAPI document (Example 12) is authored and
agreed upon BEFORE a single handler is written -- the spec becomes the
design decision itself, and Example 71's handler is later WRITTEN TO
MATCH it, not the other way around.
"""

from typing import Any  # => the spec is arbitrary nested JSON

SPEC_WRITTEN_FIRST: dict[str, Any] = {  # => co-09: this dict exists BEFORE any handler code does
    "paths": {  # => co-14: every field a future handler must return is decided HERE
        "/articles/{id}": {  # => co-09: the ONE resource path this spec covers
            "get": {  # => co-09: the operation's own declared response shape
                "responses": {  # => co-09: every status code this operation can return
                    "200": {  # => a successful GET
                        "content": {  # => co-09: media types the 200 response can be returned as
                            "application/json": {  # => co-09: the ONE media type this spec declares
                                "schema": {  # => co-14: the FIELDS a conforming response must have
                                    "type": "object",  # => co-14: the response body is a JSON object
                                    "required": ["id", "title"],  # => co-14: these two fields are MANDATORY
                                    "properties": {"id": {"type": "integer"}, "title": {"type": "string"}},  # => co-14
                                }  # => end of schema
                            }  # => end of application/json
                        }  # => end of content
                    }  # => end of the 200 response
                }  # => end of responses
            }  # => end of the get operation
        }  # => end of /articles/{id}
    }  # => end of paths
}  # => end of SPEC_WRITTEN_FIRST


def required_fields(spec: dict[str, Any], path: str, method: str) -> list[str]:  # => co-09: reads the contract
    operation = spec["paths"][path][method]  # => the specific operation's own definition
    schema = operation["responses"]["200"]["content"]["application/json"]["schema"]  # => its response schema
    return list(schema["required"])  # => co-14: exactly the fields a handler MUST produce


fields_the_handler_must_return = required_fields(SPEC_WRITTEN_FIRST, "/articles/{id}", "get")
# => co-09: this list is now the DESIGN -- it exists before Example 71's handler is written
print(f"handler must return: {fields_the_handler_must_return}")  # => Output: ['id', 'title']
