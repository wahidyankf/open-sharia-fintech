# pyright: strict
"""Example 62: A Mutation Writes Data. (co-24)

GraphQL separates read operations (`Query`, Examples 58-61) from write
operations (`Mutation`) at the SCHEMA level -- a mutation both performs a
side effect and returns a value, the same "write, then return the result"
shape REST's POST (Example 5) already uses.
"""

ARTICLES: dict[str, dict[str, object]] = {}  # => co-24: the store a mutation writes into
NEXT_ID = [1]  # => a mutable counter cell -- mints a fresh id per created article


def create_article_mutation(title: str) -> dict[str, object]:  # => co-24: mutation createArticle(title)
    new_id = str(NEXT_ID[0])  # => a fresh id for this specific article
    article: dict[str, object] = {"id": new_id, "title": title}  # => co-24: explicit dict[str, object]
    ARTICLES[new_id] = article  # => co-24: the SIDE EFFECT -- writes into the store
    NEXT_ID[0] += 1  # => advances the counter for the NEXT mutation
    return article  # => co-24: mutations still RETURN a value, just like a query does


result = create_article_mutation("Hello, GraphQL")  # => co-24: runs the mutation once
print(f"mutation result: {result}")  # => Output: {'id': '1', 'title': 'Hello, GraphQL'}

print(f"stored articles: {len(ARTICLES)}")  # => Output: 1 -- co-24: the side effect actually happened
# => a Query field would never be allowed to mutate ARTICLES -- the schema separates the two by name
