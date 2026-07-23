"""Example 82: pytest verification of nested-state events and the parent's shared transition."""

import pytest

from example import IllegalTransition, MediaPlayer


def test_play_enters_playing_with_normal_as_the_default_substate() -> None:
    player = MediaPlayer()
    player.send("play")
    assert player.state == "playing"
    assert player.substate == "normal"


def test_nested_state_event_toggles_the_child_substate() -> None:
    player = MediaPlayer()
    player.send("play")
    player.send("toggle_shuffle")  # => handled entirely at the CHILD level
    assert player.substate == "shuffle"
    player.send("toggle_shuffle")
    assert player.substate == "normal"


def test_parents_shared_transition_applies_from_either_substate() -> None:
    player = MediaPlayer()
    player.send("play")
    player.send("toggle_shuffle")  # => now in the "shuffle" substate
    assert player.substate == "shuffle"
    player.send("stop")  # => co-36: the PARENT's shared transition -- applies even from a non-default substate
    assert player.state == "stopped"
    assert player.substate is None


def test_volume_is_an_orthogonal_region_independent_of_play_state() -> None:
    player = MediaPlayer()
    player.adjust_volume(20)  # => works even while stopped
    assert player.volume == 70
    player.send("play")
    player.send("toggle_shuffle")
    player.adjust_volume(-10)  # => still works, regardless of substate
    assert player.volume == 60
    player.send("stop")
    assert player.volume == 60  # => the play-state transition never touched the orthogonal volume region


def test_toggle_shuffle_is_illegal_while_stopped() -> None:
    player = MediaPlayer()
    with pytest.raises(IllegalTransition):
        player.send("toggle_shuffle")  # => the child transition only exists inside Playing


# => Run: pytest -q -- Output: 5 passed
