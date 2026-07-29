# pyright: strict
"""Example 26: ABAC -- an owner-only attribute policy. (co-17)

Attribute-Based Access Control (ABAC) decides access from RULES over
ATTRIBUTES (the requester's, the resource's, the environment's) rather than
a fixed role table. Here the policy is "the requester must OWN the resource"
-- flexible, but the rule set is harder to audit than RBAC. Source: NIST CSRC.
"""

from dataclasses import dataclass  # => a small typed domain + response record


@dataclass  # => the resource carries its OWN owner attribute -- the thing the policy reads
class Document:
    id: int  # => the resource identifier
    owner: str  # => co-17: an ATTRIBUTE of the resource -- who owns it


@dataclass  # => co-17: status plus a short message
class Response:
    status: int  # => 200 allowed, 403 denied
    body: dict[str, str]  # => a short message


DOCS: dict[int, Document] = {1: Document(1, "ada"), 2: Document(2, "grace")}  # => resources with owner attributes
REQUESTERS: dict[str, str] = {"ada-token": "ada", "grace-token": "grace"}  # => token -> requester identity attribute


def view_doc(token: str, doc_id: int) -> Response:  # => GET /docs/{id} -- the ABAC owner policy
    requester = REQUESTERS.get(token)  # => the requester's identity ATTRIBUTE
    if requester is None:  # => no identity attribute at all
        return Response(401, {"error": "unknown requester"})  # => 401
    doc = DOCS.get(doc_id)  # => the resource (with its owner attribute)
    if doc is None:  # => resource does not exist
        return Response(404, {"error": "not found"})  # => 404
    # co-17: the ABAC RULE -- requester attribute (identity) must EQUAL resource attribute (owner)
    if requester != doc.owner:  # => the rule evaluates to DENY -- a non-owner is rejected
        return Response(403, {"error": "only the owner may view"})  # => 403
    return Response(200, {"doc_id": str(doc_id), "viewed_by": requester})  # => 200, owner


owner = view_doc("ada-token", 1)  # => ada owns doc 1 -> allowed
print(f"owner views own doc:    status={owner.status}, body={owner.body}")  # => Output: 200

non_owner = view_doc("grace-token", 1)  # => grace does NOT own doc 1 -> denied by the attribute rule
print(f"non-owner views doc 1:  status={non_owner.status}, body={non_owner.body}")  # => Output: 403

assert owner.status == 200  # => co-17: the owner attribute matches -> allowed
assert non_owner.status == 403  # => co-17: a non-owner is denied by the rule (ABAC, not a role table)
