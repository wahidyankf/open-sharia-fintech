# pyright: strict
"""Example 22: A Generated Typed Client, Modeled by Hand. (co-11)

A real codegen tool reads the spec's `Article` schema and emits a typed
client class automatically. This example plays that role by hand: the
dataclass's field NAMES and TYPES are derived directly from the schema, so
a call against it type-checks exactly the way a generated client would.
"""

from dataclasses import dataclass  # => the "generated" type is expressed as a dataclass
from typing import Any  # => the schema itself stays arbitrary nested JSON

ARTICLE_SCHEMA: dict[str, Any] = {  # => co-11: the schema codegen would read
    "type": "object",  # => the top-level instance shape
    "properties": {"id": {"type": "integer"}, "title": {"type": "string"}},  # => the two fields
    "required": ["id", "title"],  # => both fields are mandatory
}


@dataclass  # => co-11: hand-written HERE, but its shape is DERIVED from ARTICLE_SCHEMA above
class Article:  # => what a codegen tool would emit as the response type
    id: int  # => matches schema.properties.id.type == "integer"
    title: str  # => matches schema.properties.title.type == "string"


class GeneratedArticlesClient:  # => co-11: the typed client shape a codegen tool would emit
    def get_article(self, article_id: int) -> Article:  # => a typed method, not a raw dict
        # => a real client would perform an HTTP call here; this stands in with fixed data
        return Article(id=article_id, title="Hello, API Design")  # => a fully typed return value


def schema_field_names(schema: dict[str, Any]) -> set[str]:  # => co-11: what the SPEC declares
    return set(schema["properties"].keys())  # => the set of field names the spec defines


def dataclass_field_names(cls: type[Article]) -> set[str]:  # => co-11: what the CLIENT actually has
    return {f for f in cls.__dataclass_fields__}  # => the set of field names the class defines


client = GeneratedArticlesClient()  # => co-11: exactly what a generated client usage looks like
article = client.get_article(1)  # => a fully TYPED call -- article.title, not article["title"]
print(f"typed client call: id={article.id}, title={article.title!r}")  # => Output: id/title shown

schema_fields = schema_field_names(ARTICLE_SCHEMA)  # => the SOURCE OF TRUTH's own field names
# => schema_fields is {'id', 'title'} (type: set[str])
client_fields = dataclass_field_names(Article)  # => the GENERATED type's own field names
# => client_fields is {'id', 'title'} (type: set[str]) -- matches schema_fields exactly
print(f"schema fields == client fields: {schema_fields == client_fields}")  # => Output: True
