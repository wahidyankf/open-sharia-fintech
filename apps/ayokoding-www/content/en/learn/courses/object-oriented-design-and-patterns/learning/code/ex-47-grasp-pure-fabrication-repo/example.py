"""Example 47: A Repository -- a Pure Fabrication for Persistence."""

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass(frozen=True)  # => a genuine DOMAIN concept -- knows nothing about storage
class User:  # => begins the User class body
    user_id: int  # => a required field, part of the generated __init__
    email: str  # => a required field, part of the generated __init__

    def __post_init__(self) -> None:  # => runs automatically right after construction
        if "@" not in self.email:  # => a DOMAIN rule -- belongs on the domain object itself
            raise ValueError("email must contain @")  # => rejects an invalid User at construction time


class UserRepository:  # => a PURE FABRICATION -- no analyst would ever call this a "domain concept"
    def __init__(self) -> None:  # => invented purely to keep User cohesive and decoupled from IO
        self._storage: dict[int, User] = {}  # => the ONLY place storage details live

    def save(self, user: User) -> None:  # => defines the save() method
        self._storage[user.user_id] = user  # => the IO-flavored operation, isolated HERE

    def find_by_id(self, user_id: int) -> User | None:  # => defines the find_by_id() method
        return self._storage.get(user_id)  # => returns this value to the caller


repo: UserRepository = UserRepository()  # => constructs repo
repo.save(User(user_id=1, email="ada@example.com"))  # => persistence lives ONLY in the repo

found: User | None = repo.find_by_id(1)  # => User itself never touched a dict, a file, or a DB
print(found)  # => the domain object, retrieved via the fabricated persistence seam
# => Output: User(user_id=1, email='ada@example.com')

missing: User | None = repo.find_by_id(99)  # => an id that was never saved
print(missing)  # => confirms a clean, storage-flavored "not found" result
# => Output: None
# => `UserRepository` exists ONLY to keep persistence out of `User` -- it is invented, not discovered in the domain
