# pyright: strict
"""Example 57: Defining a GraphQL Schema and Types. (co-24)

A GraphQL schema declares types and their fields ONCE, in a small
domain-specific language (SDL) -- distinct from OpenAPI's per-operation
paths (Example 12), a GraphQL schema describes DATA SHAPES, and every
operation later queries a subset of them.
"""

SDL_LINES = [  # => co-24: the SDL, built line by line so every line can be explained
    "type Article {",  # => co-24: opens the Article object type
    "  id: ID!",  # => co-24: a required (non-null, "!") scalar field
    "  title: String!",  # => co-24: another required scalar field
    "  author: Author!",  # => co-24: a required field whose type is ANOTHER declared object type
    "}",  # => closes Article
    "",  # => a blank line, purely for the generated SDL's own readability
    "type Author {",  # => co-24: opens the Author object type, referenced by Article above
    "  id: ID!",  # => co-24: Author's own required id field
    "  name: String!",  # => co-24: Author's own required name field
    "}",  # => closes Author
    "",  # => another blank line
    "type Query {",  # => co-24: the ROOT type -- every readable operation is a field here
    "  article(id: ID!): Article",  # => co-24: one query field, taking an id, returning an Article
    "}",  # => closes Query
]  # => end of SDL_LINES
SCHEMA_SDL = "\n".join(SDL_LINES)  # => co-24: assembles the full SDL text from its own annotated lines


def extract_type_names(sdl: str) -> list[str]:  # => co-24: a tiny structural parser, no library needed
    type_names: list[str] = []  # => collects every "type Name {" declaration found
    for line in sdl.splitlines():  # => co-24: scans the SDL line by line
        stripped = line.strip()  # => trims leading/trailing whitespace
        if stripped.startswith("type ") and stripped.endswith("{"):  # => co-24: matches "type X {"
            name = stripped.removeprefix("type ").removesuffix("{").strip()  # => extracts just "X"
            type_names.append(name)  # => co-24: records this type's own name
    return type_names  # => every type name the SDL declares, in declaration order


def sdl_parses(sdl: str) -> bool:  # => co-24: a minimal "does this look like valid SDL" check
    open_braces = sdl.count("{")  # => counts every opening brace
    close_braces = sdl.count("}")  # => counts every closing brace
    return open_braces == close_braces and open_braces > 0  # => co-24: balanced braces, non-empty


types = extract_type_names(SCHEMA_SDL)  # => co-24: parses the schema's own declared types
print(f"declared types: {types}")  # => Output: ['Article', 'Author', 'Query']

is_valid = sdl_parses(SCHEMA_SDL)  # => co-24: verifies the SDL is at least structurally well-formed
# => is_valid is True (type: bool) -- every "{" in SCHEMA_SDL has a matching "}"
print(f"SDL parses: {is_valid}")  # => Output: True
