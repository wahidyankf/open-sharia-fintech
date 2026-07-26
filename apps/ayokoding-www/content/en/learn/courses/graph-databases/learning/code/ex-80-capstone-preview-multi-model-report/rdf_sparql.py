# Example 80b: RDF/SPARQL representation (co-24).
from rdflib import Graph  # => the RDF graph class this whole script revolves around

g = Graph()  # => an empty in-memory RDF graph
g.parse(
    data="@prefix ex: <http://example.org/> . ex:Ada ex:knows ex:Charles .",
    format="turtle",
)
# => loads the SAME single fact as the Cypher form above, as one RDF triple
for row in g.query(
    "PREFIX ex: <http://example.org/> SELECT ?n WHERE { ex:Ada ex:knows ?n }"
):
    print(row.n)  # => a bound triple-pattern OBJECT (a URI), not a node object
