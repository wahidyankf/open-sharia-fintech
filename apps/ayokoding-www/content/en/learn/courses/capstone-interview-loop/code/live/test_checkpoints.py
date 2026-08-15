import pytest

from checkpoints import add_checkpoint


def test_adds_a_green_increment_without_mutating_prior_progress() -> None:
    prior = ["clarified contract"]
    assert add_checkpoint(prior, "implemented narrow slice") == [
        "clarified contract",
        "implemented narrow slice",
    ]
    assert prior == ["clarified contract"]


def test_rejects_an_unnamed_increment() -> None:
    with pytest.raises(ValueError, match="checkpoint"):
        add_checkpoint([], "   ")
