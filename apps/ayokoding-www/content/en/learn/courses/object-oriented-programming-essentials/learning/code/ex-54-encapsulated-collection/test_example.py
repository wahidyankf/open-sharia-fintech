"""Example 54: pytest verification for Exposing a Read-Only View of an Internal Collection."""

from example import Playlist


def test_returned_view_is_a_tuple_not_the_internal_list() -> None:
    p: Playlist = Playlist()
    p.add("Song A")
    view: tuple[str, ...] = p.songs
    assert view == ("Song A",)
    assert not hasattr(
        view, "append"
    )  # => a tuple has no mutating methods -- callers cannot leak in


def test_mutating_the_playlist_does_not_retroactively_change_a_taken_view() -> None:
    p: Playlist = Playlist()
    p.add("Song A")
    view: tuple[str, ...] = p.songs  # => a frozen snapshot at THIS point in time
    p.add("Song B")  # => mutates internal state after the snapshot was taken
    assert view == ("Song A",)  # => the old snapshot is untouched
    assert p.songs == ("Song A", "Song B")  # => a fresh call reflects the current state


# => Run: pytest -- Output: 2 passed
