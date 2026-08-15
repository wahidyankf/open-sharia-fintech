"""A deliberately narrow SQL-ish facade over WAL-backed rows."""

from __future__ import annotations

import re
from pathlib import Path

from btree import BTree
from recovery import committed_rows
from wal import append

INSERT = re.compile(r"insert into [a-z_]+ values \(([^,]+),([^,]+),([^\)]+)\)", re.I)
SELECT = re.compile(r"select \* from [a-z_]+(?: where ([a-z_]+) (=|>) ([^ ]+))?", re.I)


class MiniDatabase:
    def __init__(self, directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        self.wal_path = directory / "write-ahead.log"
        self.index = BTree()
        for key, row in committed_rows(self.wal_path).items():
            self.index.insert(key, row)

    def execute(self, statement: str) -> list[dict[str, str]]:
        normalized = " ".join(statement.strip().split())
        insert = INSERT.fullmatch(normalized)
        if insert:
            row = {
                "id": insert.group(1),
                "name": insert.group(2),
                "score": insert.group(3),
            }
            append(self.wal_path, {"kind": "commit", "row": row})
            self.index.insert(row["id"], row)
            return []
        select = SELECT.fullmatch(normalized)
        if not select:
            raise ValueError("only a small insert/select/where subset is supported")
        rows = [row for _, row in self.index.scan()]
        if select.group(1) is None:
            return rows
        column, operator, expected = select.group(1), select.group(2), select.group(3)
        if operator == "=":
            return [row for row in rows if row.get(column) == expected]
        return [row for row in rows if row.get(column, "") > expected]
