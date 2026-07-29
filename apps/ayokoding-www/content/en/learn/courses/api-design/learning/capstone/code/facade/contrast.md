# Capstone Step 4 -- REST vs. GraphQL Facade Contrast

_Traces to: `rest.py`'s/`limits.py`'s `STORE`, mirrored exactly in `graphql_facade.py`._ (co-27)

The identical Article data (`{"id": 2, "title": "Capstone Article"}`, created by `rest.py`'s Step 2
write) is served two ways from this capstone: `GET /v1/articles/2` over REST returns the article's
full, fixed shape (Example 1's own rule); `graphql_query(2, [...])` returns only the fields the
caller's own query names (Example 58's own rule) -- both against the SAME underlying `STORE`.

## What stays identical between the two facades

- **The data itself.** `graphql_facade.py`'s `STORE` is populated with the exact same values
  `rest.py` produced -- `data_matches` in that script asserts this explicitly, and the assertion
  passes.
- **The resource's identity.** Both facades address the article by the SAME id (`2`) -- neither
  facade invents a parallel identifier scheme for the same underlying entity.

## What differs between the two facades

| Concern            | REST (`rest.py`/`limits.py`)                                      | GraphQL (`graphql_facade.py`)                                    |
| ------------------ | ----------------------------------------------------------------- | ---------------------------------------------------------------- |
| Response shape     | Fixed -- every caller gets `id` + `title`, every time (Example 1) | Selective -- the caller's own query decides (Example 58)         |
| Over-fetching risk | A caller needing only `title` still receives `id` too             | None -- `narrow_response` in `graphql_facade.py` proves this     |
| Caching            | `GET` + `Cache-Control` -- cacheable by any HTTP intermediary     | Rides over POST in a real deployment -- not cacheable by default |
| Versioning         | `/v1/articles/{id}` -- Example 29's URI-path strategy             | Additive schema fields -- Example 68's own evolution rule        |
| Idempotent writes  | `Idempotency-Key` header (Examples 37-39, `rest.py`'s Step 2)     | A `Mutation` field -- Example 62's own shape                     |

## When each style wins, concretely

**REST wins here** because this capstone's own consumer is a public-facing client that always needs
both `id` and `title` together, benefits from HTTP-level caching on the read path (Example 44), and
gets clear versioning semantics for free from the URI path alone -- Example 69's own decision-matrix
scenario 1 ("public API consumed by many unknown third-party clients") applies directly.

**GraphQL would win instead** if this capstone had multiple, very different consumers each needing a
different subset of a LARGER resource shape (say, an article with a long body, tags, and comments) --
Example 69's scenario 2 ("many different screens with different data needs") is the shape of problem
where GraphQL's field selection earns its complexity over REST's fixed response.

For THIS capstone specifically -- one small resource, one consumer shape, a public API that benefits
from HTTP caching -- REST is the right primary contract, and the GraphQL facade above exists to prove
the SAME data remains servable through a second style without being duplicated or re-derived, exactly
the point Example 80's closing example made for the whole Advanced tier.
