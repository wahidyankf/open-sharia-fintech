from pathlib import Path

import pytest
from briefcheck import RecordError, main, parse_record, read_and_summarize, render, summarize


def test_summarize_accumulates_and_render_sorts() -> None:
    totals = summarize(["lin,1\n", "ada,2\n", "lin,3\n"])

    assert totals == {"ada": 2, "lin": 4}
    assert render(totals) == "ada: 2\nlin: 4"


def test_blank_input_and_blank_lines_are_safe() -> None:
    assert summarize(["\n", "  \n"]) == {}
    assert render({}) == ""


@pytest.mark.parametrize(
    ("line", "message"),
    [
        ("only-owner\n", "expected owner,count"),
        (",2\n", "owner must not be blank"),
        ("ada,nope\n", "count must be an integer"),
        ("ada,-1\n", "count must be a non-negative integer"),
    ],
)
def test_parse_record_explains_malformed_input(line: str, message: str) -> None:
    with pytest.raises(RecordError, match=message):
        parse_record(line, 3)


def test_read_and_summarize_uses_utf8_file(tmp_path: Path) -> None:
    records = tmp_path / "records.txt"
    records.write_text("zoe,1\nada,4\n", encoding="utf-8")

    assert read_and_summarize(records) == "ada: 4\nzoe: 1"


def test_main_reports_usage_and_validation_errors(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([]) == 2
    assert "usage:" in capsys.readouterr().err

    records = tmp_path / "bad.txt"
    records.write_text("ada,-2\n", encoding="utf-8")
    assert main([str(records)]) == 1
    assert "line 1" in capsys.readouterr().err
