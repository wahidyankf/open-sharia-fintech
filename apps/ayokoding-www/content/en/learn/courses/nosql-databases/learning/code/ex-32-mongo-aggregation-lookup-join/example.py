"""Example 32: MongoDB Aggregation $lookup Correlated Subquery."""  # => co-19: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => enables the explicit MongoClient[dict[str, Any]] type parameter below (DD-39, pyright --strict)

from pymongo import MongoClient  # => co-19: pymongo, the official typed Python driver

Document = dict[str, Any]  # => co-19: pymongo's own convention for "a MongoDB document" -- every field's own type varies per-document


def seed_authors_and_books(client: MongoClient[Document]) -> None:  # => two collections, joined server-side below
    """Reset and seed 2 authors (each with its own min_year floor) and 3 books, referencing authors by name."""  # => documents the contract
    authors = client["nosqldb"]["authors"]  # => the "one" side of the relation
    books = client["nosqldb"]["books"]  # => the "many" side of the relation
    authors.delete_many({})  # => resets state -- this example is fully self-contained
    books.delete_many({})  # => resets the books side too
    authors.insert_many(
        [  # => co-19: 2 authors, each carries its OWN min_year -- the correlated pipeline reads this per-author
            {"name": "Ada", "min_year": 2015},  # => Ada's floor excludes her own older book, seeded below
            {"name": "Grace", "min_year": 1950},  # => Grace's floor is low enough to keep her only book
        ]
    )  # => 2 authors seeded, each with a different min_year threshold
    books.insert_many(
        [  # => co-19: 3 books, "author" is the join key, "year" is what the correlated pipeline filters on
            {"title": "NoSQL 101", "author": "Ada", "year": 2020},  # => Ada's book 1 -- published AFTER her min_year (2015), so it survives the filter
            {"title": "CAP Theorem Explained", "author": "Ada", "year": 2010},  # => Ada's book 2 -- published BEFORE her min_year (2015), the pipeline drops it
            {"title": "Compilers 101", "author": "Grace", "year": 1957},  # => Grace's only book -- published after her low min_year (1950), survives
        ]
    )  # => 3 books seeded; a plain equality join would return all 3, the correlated pipeline below returns only 2


def authors_with_recent_books(client: MongoClient[Document]) -> list[Document]:  # => co-19: a server-side CORRELATED subquery, one round trip
    """Run a $lookup pipeline attaching only each author's own books published at/after her own min_year."""  # => documents the contract
    authors = client["nosqldb"]["authors"]  # => the collection $lookup pipelines FROM
    pipeline = [  # => co-19: MongoDB 5.0+ correlated $lookup syntax -- localField/foreignField PLUS let/pipeline together
        {  # => stage 1 -- the whole $lookup stage dict starts here
            "$lookup": {  # => co-19: the server-side join stage -- no separate client-side query needed
                "from": "books",  # => co-19: the FOREIGN collection to join against
                "localField": "name",  # => co-19: still runs the automatic name == author equality match first
                "foreignField": "author",  # => co-19: the foreign collection's field matched against localField
                "let": {"min_year": "$min_year"},  # => co-19: captures THIS author's own min_year, exposed to the sub-pipeline as $$min_year
                "pipeline": [  # => co-19: the sub-pipeline is what makes this a CORRELATED subquery, not a plain equality join
                    {"$match": {"$expr": {"$gte": ["$year", "$$min_year"]}}},  # => co-19: keeps only books at/after THIS CORRELATED author's own min_year
                ],  # => runs once PER author, using that author's own let-bound $$min_year each time
                "as": "books",  # => co-19: the joined, filtered results attach under this NEW array field
            }  # => closes the $lookup operator's own options dict
        },  # => closes stage 1
        {"$sort": {"name": 1}},  # => sorts authors alphabetically for deterministic output
    ]  # => 2 stages, run server-side -- the correlated join, filter, AND sort all happen before any row reaches this client
    return list(authors.aggregate(pipeline))  # => co-19: ONE round trip returns EVERY author with only her qualifying books attached


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    client = MongoClient("mongodb://localhost:27017")  # => connects to a local MongoDB instance
    seed_authors_and_books(client)  # => sets up the 2-author, 3-book fixture
    joined = authors_with_recent_books(client)  # => runs the correlated $lookup join
    assert len(joined) == 2  # => co-19: both authors present, each with its own filtered books array
    for author in joined:  # => prints each author with its joined, filtered book titles
        titles = [book["title"] for book in author["books"]]  # => co-19: extracts titles from the JOINED array field
        print(f"{author['name']}: {titles}")  # => Output line, one per author
    assert len(joined[0]["books"]) == 1  # => co-19: Ada's filtered array keeps only her post-2015 book
    assert len(joined[1]["books"]) == 1  # => co-19: Grace's filtered array keeps her only (post-1950) book
    client.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
