"""Generic-контейнеры и Protocol для ЛР-6."""

from __future__ import annotations

from typing import Callable, Generic, Iterator, Optional, Protocol, Type, TypeVar, runtime_checkable


T = TypeVar("T")
R = TypeVar("R")


@runtime_checkable
class Displayable(Protocol):
    """Protocol для объектов, которые умеют возвращать строковое представление."""

    def display(self) -> str:
        ...


@runtime_checkable
class Scorable(Protocol):
    """Protocol для объектов, которые умеют возвращать числовую оценку."""

    def score(self) -> float:
        ...


D = TypeVar("D", bound=Displayable)
S = TypeVar("S", bound=Scorable)


class TypedCollection(Generic[T]):
    """Generic-версия коллекции Library из ЛР-2."""

    def __init__(self, item_type: Optional[Type[T]] = None, items: Optional[list[T]] = None) -> None:
        self._item_type: Optional[Type[T]] = item_type
        self._items: list[T] = []
        if items is not None:
            for item in items:
                self.add(item)

    def add(self, item: T) -> None:
        self._validate_item(item)
        if item in self._items:
            raise ValueError("Нельзя добавить дубликат в типизированную коллекцию.")
        self._items.append(item)

    def remove(self, item: T) -> None:
        self._validate_item(item)
        if item not in self._items:
            raise ValueError("Элемент не найден в коллекции.")
        self._items.remove(item)

    def remove_at(self, index: int) -> T:
        return self._items.pop(index)

    def get_all(self) -> list[T]:
        return list(self._items)

    def find_by_title(self, title: str) -> list[T]:
        if not isinstance(title, str):
            raise TypeError("title должен быть строкой.")
        query = title.strip().lower()
        return [item for item in self._items if query in getattr(item, "title", "").lower()]

    def find_by_author(self, author: str) -> list[T]:
        if not isinstance(author, str):
            raise TypeError("author должен быть строкой.")
        query = author.strip().lower()
        return [item for item in self._items if query in getattr(item, "author", "").lower()]

    def sort_by_price(self, reverse: bool = False) -> None:
        self._items.sort(key=lambda item: getattr(item, "price"), reverse=reverse)

    def sort_by_year(self, reverse: bool = False) -> None:
        self._items.sort(key=lambda item: getattr(item, "year"), reverse=reverse)

    def get_available(self) -> "TypedCollection[T]":
        return TypedCollection(self._item_type, [item for item in self._items if getattr(item, "available", False)])

    def get_expensive(self, min_price: float) -> "TypedCollection[T]":
        if not isinstance(min_price, (int, float)) or isinstance(min_price, bool):
            raise TypeError("min_price должен быть числом (int или float).")
        return TypedCollection(self._item_type, [item for item in self._items if getattr(item, "price") >= float(min_price)])

    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for item in self._items:
            if predicate(item):
                return item
        return None

    def filter(self, predicate: Callable[[T], bool]) -> list[T]:
        return [item for item in self._items if predicate(item)]

    def map(self, transform: Callable[[T], R]) -> list[R]:
        return [transform(item) for item in self._items]

    def display_all(self: "TypedCollection[D]") -> list[str]:
        return [item.display() for item in self._items]

    def score_all(self: "TypedCollection[S]") -> list[float]:
        return [item.score() for item in self._items]

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)

    def __getitem__(self, index: int) -> T:
        return self._items[index]

    def _validate_item(self, item: T) -> None:
        if self._item_type is not None and not isinstance(item, self._item_type):
            expected = getattr(self._item_type, "__name__", str(self._item_type))
            raise TypeError(f"Можно добавлять только объекты типа {expected}.")

