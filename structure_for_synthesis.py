"""合成用の構造"""

from typing import List, Iterator


class X:
    def __init__(
        self, name: str, catalyst: str, connect_names: List[str], repo: "XRepository"
    ):
        self.name = name
        self.catalyst = catalyst
        self._connect_names = connect_names
        self._repo = repo

    @property
    def connect(self) -> List["X"]:
        return [self._repo[n] for n in self._connect_names if self._repo.exists(n)]

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, X):
            return False
        return self.name == other.name


class XRepository:
    def __init__(self):
        self._storage: dict[str, X] = {}

    def register(self, name: str, catalyst: str, connect_names: list[str]):
        self._storage[name] = X(name, catalyst, connect_names, self)
        return self

    def __getitem__(self, name: str) -> "X":
        return self._storage[name]

    def exists(self, name: str) -> bool:
        return name in self._storage

    def all(self):
        return [(key, self._storage[key]) for key in list(self._storage)]

    def __iter__(self) -> Iterator["X"]:
        return iter(self._storage.values())

    def __len__(self):
        return len(self._storage)
