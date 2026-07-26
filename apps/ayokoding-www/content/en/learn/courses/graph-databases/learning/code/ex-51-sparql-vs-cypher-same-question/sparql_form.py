# Example 51a: "who does Ada know", answered in SPARQL over RDF triples. (co-24, co-02)
from rdflib import Graph  # => the RDF graph class this whole script revolves around

g = Graph()  # => an empty in-memory RDF graph
TURTLE_DATA = (
    "@prefix ex: <http://example.org/> .\n"  # => namespace prefix for our example IRIs
    "ex:Ada ex:knows ex:Charles .\n"  # => Ada's first known-fact triple
    "ex:Ada ex:knows ex:Babbage .\n"  # => Ada's second known-fact triple -- same fixture as Example 26
)  # => end of the Turtle fixture string
g.parse(data=TURTLE_DATA, format="turtle")  # => loads both triples above into g

SPARQL_QUERY = (
    "PREFIX ex: <http://example.org/> "  # => namespace prefix, needed by the query itself
    "SELECT ?n WHERE { ex:Ada ex:knows ?n }"  # => the OBJECT bound to ?n, for every matching triple
)  # => end of the SPARQL query string

for row in g.query(SPARQL_QUERY):  # => one result row per matching triple pattern
    print(row.n)  # => prints each bound URI, one per matching triple
