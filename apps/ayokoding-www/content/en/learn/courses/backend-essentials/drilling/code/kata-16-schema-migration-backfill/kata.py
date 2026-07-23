from typing import TypedDict


class TaskV1(TypedDict):  # => co-15: the SHAPE before the migration -- what existing rows already look like
    id: int
    title: str


class TaskV2(TypedDict):  # => co-15: the SHAPE after the migration -- one new nullable-with-default column
    id: int
    title: str
    archived: bool  # => the new column -- an ADDITIVE change, nothing removed or renamed


def migrate_add_archived(rows: list[TaskV1]) -> list[TaskV2]:  # => co-15: ALTER TABLE ... ADD COLUMN + backfill
    return [
        {"id": row["id"], "title": row["title"], "archived": False}  # => co-15: backfill every existing row
        for row in rows  # => a real migration would run one UPDATE, not a Python loop -- same idea though
    ]


existing_rows: list[TaskV1] = [  # => co-15: rows that existed BEFORE the migration ran
    {"id": 1, "title": "Write the report"},
    {"id": 2, "title": "Ship the release"},
]

migrated_rows = migrate_add_archived(existing_rows)
print(migrated_rows)  # => Output: [{'id': 1, 'title': 'Write the report', 'archived': False}, {'id': 2, 'title': 'Ship the release', 'archived': False}]

# => co-15: EVERY pre-existing row gained the new column with a safe default -- nothing became invalid
assert all(row["archived"] is False for row in migrated_rows)
assert [row["id"] for row in migrated_rows] == [1, 2]  # => co-15: identity and order fully preserved
assert len(migrated_rows) == len(existing_rows)  # => co-15: additive means no row is dropped or merged
print("kata-16 OK")
