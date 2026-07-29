"""Kata 7 -- Compose pagination + filter on an in-memory list (co-11)."""

from typing import TypedDict


class Row(TypedDict):  # => a typed row
    id: int
    status: str


class Page(TypedDict):  # => the paginated envelope (co-11)
    items: list[Row]
    total: int  # => the FILTERED count
    next: int | None  # => None at the end


def list_page(
    rows: list[Row], status: str | None, limit: int, offset: int
) -> Page:  # => co-11
    filtered = [
        r for r in rows if status is None or r["status"] == status
    ]  # => filter step
    total = len(filtered)  # => the filtered count, not the whole list (co-11)
    page = filtered[offset : offset + limit]  # => pagination step over the filtered set
    nxt = offset + limit  # => the next page's offset
    return {
        "items": page,
        "total": total,
        "next": nxt if nxt < total else None,
    }  # => None at end


def main() -> None:
    rows: list[Row] = [  # => 4 rows: 2 done, 2 todo
        {"id": 1, "status": "done"},
        {"id": 2, "status": "todo"},
        {"id": 3, "status": "done"},
        {"id": 4, "status": "todo"},
    ]
    p = list_page(rows, status="done", limit=1, offset=0)  # => first page of done-only
    print(
        [r["id"] for r in p["items"]], p["total"], p["next"]
    )  # => [1] 2 1 -- total is the FILTERED count
    assert [r["id"] for r in p["items"]] == [1]
    assert p["total"] == 2  # => 2 done rows total, even though only 1 is on this page


if __name__ == "__main__":
    main()
