"""Example 15: Classify the NoSQL Families."""  # => co-01: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from enum import Enum, auto  # => co-01: an Enum makes "one of these four families" a checkable type, not a bare string


class Family(Enum):  # => co-01: the four non-graph families this topic teaches
    KEY_VALUE = auto()  # => co-01: opaque values addressed by a single key -- Redis/Valkey
    DOCUMENT = auto()  # => co-01: semi-structured, schema-on-read records -- MongoDB
    WIDE_COLUMN = auto()  # => co-01: partition + clustering key rows -- Cassandra, DynamoDB
    GRAPH = auto()  # => co-01: nodes and edges -- Neo4j, explicitly OUT OF SCOPE for this topic


PRODUCT_FAMILY: dict[str, Family] = {  # => co-01: the reference answer key this example verifies against
    "Redis": Family.KEY_VALUE,  # => co-01: single opaque values addressed by a key -- the simplest family
    "MongoDB": Family.DOCUMENT,  # => co-01: nested, semi-structured JSON-like records -- the flexible-shape family
    "Cassandra": Family.WIDE_COLUMN,  # => co-01: rows keyed by partition + clustering columns -- NOT a document store
    "DynamoDB": Family.WIDE_COLUMN,  # => co-01: DynamoDB is wide-column-shaped, not document-shaped, despite JSON items
    "Neo4j": Family.GRAPH,  # => co-01: named here ONLY to show the boundary -- graph-databases is a sibling topic
}  # => co-01: 5 products, 4 families -- Redis/MongoDB/Cassandra/DynamoDB in-scope, Neo4j's GRAPH deliberately out


def classify(product: str) -> Family:  # => a pure lookup -- classification is a fact about the product, not a guess
    """Return the NoSQL family a product belongs to."""  # => documents the contract, no runtime output
    return PRODUCT_FAMILY[product]  # => co-01: KeyError on an unrecognized product -- fail loudly, never guess


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    for product, expected in PRODUCT_FAMILY.items():  # => co-01: verifies every entry in the reference answer key
        actual = classify(product)  # => runs the classification for this one product
        assert actual == expected  # => co-01: the lookup must agree with itself -- a sanity check on the table
        print(f"{product}: {actual.name}")  # => Output (one line per product): Redis: KEY_VALUE / MongoDB: DOCUMENT / Cassandra: WIDE_COLUMN / DynamoDB: WIDE_COLUMN / Neo4j: GRAPH
    print("All 5 products classified correctly against the reference answer key")  # => Output: All 5 products classified correctly against the reference answer key


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
