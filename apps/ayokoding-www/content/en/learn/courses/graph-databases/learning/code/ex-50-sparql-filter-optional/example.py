# Example 50: SPARQL OPTIONAL and FILTER. (co-24)
from rdflib import Graph  # => the RDF graph class this whole script revolves around

# Turtle fixture, built as concatenated lines rather than one triple-quoted block, so each
# line can carry its own inline comment -- the same pattern Example 44 uses for Cypher strings.
TURTLE_DATA = (
    "@prefix ex: <http://example.org/> .\n"  # => namespace prefix for our example IRIs
    "@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n"  # => the standard FOAF vocabulary prefix
    'ex:Ada foaf:name "Ada" ; foaf:mbox "ada@example.org" .\n'  # => Ada HAS an email triple
    'ex:Bob foaf:name "Bob" .\n'  # => Bob deliberately has NO mbox -- the asymmetry OPTIONAL tests
)  # => end of the Turtle fixture string

g = Graph()  # => an empty in-memory RDF graph
g.parse(data=TURTLE_DATA, format="turtle")  # => loads both people's triples into g

query = (
    "PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n"  # => the same namespace, needed again here
    "SELECT ?name ?mbox WHERE {\n"  # => opens the WHERE block -- the pattern to match
    "  ?x foaf:name ?name .\n"  # => REQUIRED triple: every result row must bind a name
    "  OPTIONAL { ?x foaf:mbox ?mbox }\n"  # => OPTIONAL triple: a missing mbox still keeps the row
    '  FILTER regex(?name, "Ada")\n'  # => narrows the results to names matching the regex "Ada"
    "}\n"  # => closes the WHERE block
)  # => end of the SPARQL query string

for row in g.query(query):  # => one result row per person surviving the FILTER
    print(
        row.name, row.mbox
    )  # => mbox prints as None whenever the OPTIONAL block found nothing
