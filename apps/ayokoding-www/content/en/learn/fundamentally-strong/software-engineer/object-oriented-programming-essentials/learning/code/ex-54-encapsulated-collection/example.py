"""Example 54: Exposing a Read-Only View of an Internal Collection."""


class Playlist:  # => begins the Playlist class body
    def __init__(
        self,
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self._songs: list[
            str
        ] = []  # => internal, mutable storage -- never handed out directly

    def add(self, song: str) -> None:  # => defines the add() method
        self._songs.append(song)  # => the ONLY sanctioned way to grow the internal list

    @property  # => marks the next method as a computed attribute
    def songs(
        self,
    ) -> tuple[str, ...]:  # => returns an IMMUTABLE copy, not the internal list itself
        return tuple(
            self._songs
        )  # => a tuple cannot be appended to -- mutation cannot leak back


p: Playlist = Playlist()  # => constructs p
p.add("Song A")
view: tuple[str, ...] = p.songs  # => a snapshot copy, not a reference to _songs
print(view)  # => shows the current contents
# => Output: ('Song A',)
p.add("Song B")  # => mutates the internal list AFTER the view was taken
print(
    view, p.songs
)  # => the old view is frozen; a fresh .songs call reflects the new song
# => Output: ('Song A',) ('Song A', 'Song B')
# => `tuple(self._songs)` builds a genuinely separate, immutable copy on every access
