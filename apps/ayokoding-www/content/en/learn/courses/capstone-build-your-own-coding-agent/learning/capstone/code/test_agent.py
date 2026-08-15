from pathlib import Path

from agent import Action, run_fake


def test_fake_agent_refuses_workspace_escape(tmp_path: Path) -> None:
    assert run_fake(tmp_path, Action("read", "../outside"))["status"] == "denied"


def test_fake_agent_audits_approved_test(tmp_path: Path) -> None:
    assert run_fake(tmp_path, Action("test", "tests/test_local.py"))[
        "audit"
    ].startswith("approved")
