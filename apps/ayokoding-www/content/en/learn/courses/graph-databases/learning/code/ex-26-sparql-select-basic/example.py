# Example 26: A Basic SPARQL SELECT. (co-24, co-02)
# rdflib is a pure-Python RDF library with a built-in SPARQL 1.1 engine -- `pip install rdflib`.
# This script is fully self-contained: it builds the same triples as Example 25 in-memory,
# then answers the identical "who does Ada know" question Example 6 answered in Cypher.
from rdflib import Graph  # => the RDF graph class this whole script revolves around

# The triple data itself, as an inline Turtle string -- self-contained, no external file needed.
TURTLE_DATA = """
@prefix ex: <http://example.org/> .
ex:Ada ex:knows ex:Charles .
ex:Ada ex:knows ex:Babbage .
"""  # => two ex:knows triples, matching Example 6's two KNOWS edges exactly

g = Graph()  # => an empty in-memory RDF graph
g.parse(data=TURTLE_DATA, format="turtle")  # => loads both triples above into g

query = """
PREFIX ex: <http://example.org/>
SELECT ?name WHERE { ex:Ada ex:knows ?name }
"""
# => WHERE matches the triple pattern (ex:Ada, ex:knows, ?name) -- ?name is the query's variable
# => PREFIX ex: is a shorthand -- without it every triple would need the full URI spelled out

for row in g.query(query):  # => one result row per triple that fits the pattern
    print(row.name)  # => prints the OBJECT bound to ?name for each matching triple
# => two print calls fire, one per matching triple -- Charles, then Babbage
