# Example 76: SPARQL CONSTRUCT a Derived Graph. (co-24)
from rdflib import Graph  # => the RDF graph class this whole script revolves around

g = Graph()  # => an empty in-memory RDF graph
TURTLE_DATA = (
    "@prefix ex: <http://example.org/> .\n"  # => namespace prefix for our example IRIs
    "ex:Ada ex:knows ex:Charles .\n"  # => hop 1 of the chain: Ada -> Charles
    "ex:Charles ex:knows ex:Babbage .\n"  # => hop 2 of the chain: Charles -> Babbage
)  # => end of the Turtle fixture string -- a 2-hop chain of ex:knows triples
g.parse(data=TURTLE_DATA, format="turtle")  # => loads both triples above into g

query = (
    "PREFIX ex: <http://example.org/>\n"  # => namespace prefix, needed by the query itself
    "CONSTRUCT { ?a ex:knowsIndirectly ?c }\n"  # => the NEW triple shape this query builds
    "WHERE {\n"  # => opens the WHERE block -- the 2-hop pattern to match
    "  ?a ex:knows ?b .\n"  # => first hop of the chain
    "  ?b ex:knows ?c .\n"  # => second hop of the chain -- shares ?b with the line above
    "}\n"  # => closes the WHERE block
)  # => end of the SPARQL CONSTRUCT query string
# => CONSTRUCT builds a NEW triple, ex:knowsIndirectly, for every 2-hop ex:knows chain matched

derived = g.query(query)  # => derived is itself a graph of newly CONSTRUCTed triples
for triple in derived:  # => one loop iteration per new triple CONSTRUCT built
    print(
        triple
    )  # => each printed row IS a new (subject, predicate, object) triple, not a binding
