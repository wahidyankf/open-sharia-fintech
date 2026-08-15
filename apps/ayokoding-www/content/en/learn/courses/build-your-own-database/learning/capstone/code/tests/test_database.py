from __future__ import annotations

from pathlib import Path

from btree import BTree
from pager import PAGE_SIZE, Pager
from query import MiniDatabase
from recovery import committed_rows


def test_pager_round_trip_and_cache(tmp_path: Path) -> None:
    pager = Pager(tmp_path / "store.db", capacity=1)
    pager.write(1, b"row")
    assert pager.read(1).startswith(b"row")
    assert len(pager.read(1)) == PAGE_SIZE


def test_ordered_index_splits() -> None:
    tree = BTree(leaf_size=2)
    for key in ["3", "1", "2", "4"]:
        tree.insert(key, {"id": key})
    assert [key for key, _ in tree.scan()] == ["1", "2", "3", "4"]
    assert len(tree.leaf_chunks()) == 2


def test_committed_rows_survive_reopen_and_filter(tmp_path: Path) -> None:
    database = MiniDatabase(tmp_path)
    database.execute("insert into people values (2,ada,9)")
    database.execute("insert into people values (1,lin,3)")
    reopened = MiniDatabase(tmp_path)
    assert reopened.execute("select * from people where score > 4") == [
        {"id": "2", "name": "ada", "score": "9"}
    ]


def test_incomplete_wal_tail_is_not_replayed(tmp_path: Path) -> None:
    database = MiniDatabase(tmp_path)
    database.execute("insert into people values (1,ada,9)")
    database.wal_path.write_text(
        database.wal_path.read_text() + '{"kind":', encoding="utf-8"
    )
    assert committed_rows(database.wal_path) == {
        "1": {"id": "1", "name": "ada", "score": "9"}
    }
