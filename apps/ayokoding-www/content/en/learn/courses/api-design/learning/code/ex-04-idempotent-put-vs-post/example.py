# pyright: strict
"""Example 4: PUT Is Idempotent, POST Is Not. (co-06)

RFC 9110 marks PUT idempotent and POST not idempotent. Calling the SAME PUT
request twice leaves the store in the SAME state it reached after the first
call; calling the SAME POST request twice creates a SECOND resource.
"""

STORE: dict[int, dict[str, str]] = {}  # => an in-memory resource store, keyed by id
NEXT_ID = [1]  # => a one-element list used as a mutable counter cell (co-06 setup only)


def put_article(article_id: int, title: str) -> None:  # => PUT /articles/{id} -- REPLACE semantics
    STORE[article_id] = {"title": title}  # => co-06: unconditionally SETS this exact key
    # => calling this twice with the same args leaves STORE[article_id] identical both times


def post_article(title: str) -> int:  # => POST /articles -- CREATE semantics
    new_id = NEXT_ID[0]  # => co-06: a NEW id is minted on every single call
    STORE[new_id] = {"title": title}  # => a brand-new entry, never overwriting an existing one
    NEXT_ID[0] += 1  # => advances the counter so the NEXT call gets a DIFFERENT id
    return new_id  # => the caller learns which id was just created


put_article(1, "Draft")  # => call 1: creates {1: {"title": "Draft"}}
put_article(1, "Draft")  # => call 2 (repeat): SAME id, SAME result -- idempotent
print(f"After PUT twice, store has {len(STORE)} entry: {STORE}")  # => Output: exactly 1 entry (co-06)
# => STORE is {1: {'title': 'Draft'}} -- two identical PUTs, one surviving entry

STORE.clear()  # => reset for the POST half of the contrast
NEXT_ID[0] = 1  # => reset the id counter too

id_a = post_article("Draft")  # => call 1: creates a NEW resource, id 1
# => id_a is 1 (type: int)
id_b = post_article("Draft")  # => call 2 (repeat): creates ANOTHER new resource, id 2
# => id_b is 2 (type: int) -- same title, but a DIFFERENT id: POST is not idempotent
print(f"After POST twice, store has {len(STORE)} entries: {STORE}")  # => Output: exactly 2 (co-06)
