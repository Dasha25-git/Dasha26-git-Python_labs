"""ABC-интерфейсы для ЛР-4."""

from __future__ import annotations

from abc import ABC, abstractmethod
from functools import cmp_to_key
from typing import Iterable, List


class Printable(ABC):
    """Контракт для объектов, которые можно вывести в отчёт."""

    @abstractmethod
    def to_string(self) -> str:
        """Вернуть строку для пользователя."""


class Comparable(ABC):
    """Контракт для объектов, которые умеют сравниваться."""

    @abstractmethod
    def compare_to(self, other: "Comparable") -> int:
        """Вернуть отрицательное число, ноль или положительное число."""


class Borrowable(ABC):
    """Контракт для объектов, которые можно выдать читателю."""

    @abstractmethod
    def borrow(self, reader_name: str) -> str:
        """Выдать объект читателю и вернуть описание операции."""


def print_all(items: Iterable[Printable]) -> List[str]:
    """Универсальная функция, работающая через интерфейс Printable."""

    return [item.to_string() for item in items]


def sort_comparable(items: Iterable[Comparable]) -> List[Comparable]:
    """Универсальная сортировка через интерфейс Comparable."""

    return sorted(items, key=cmp_to_key(lambda left, right: left.compare_to(right)))


def borrow_all(items: Iterable[Borrowable], reader_name: str) -> List[str]:
    """Универсальная выдача объектов через интерфейс Borrowable."""

    return [item.borrow(reader_name) for item in items]

