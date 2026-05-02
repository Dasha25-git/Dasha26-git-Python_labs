"""Коллекция, принимающая функции и стратегии."""

from __future__ import annotations

from typing import Any, Callable, Iterable, List

from src.lab02.model import Book
from src.lab03.models import MediaLibrary


class StrategyLibrary(MediaLibrary):
    """Библиотека с поддержкой sort_by, filter_by и apply."""

    def __init__(self, items: Iterable[Book] = ()) -> None:
        super().__init__(items)

    def sort_by(self, key_func: Callable[[Book], Any], reverse: bool = False) -> "StrategyLibrary":
        return StrategyLibrary(sorted(self, key=key_func, reverse=reverse))

    def filter_by(self, predicate: Callable[[Book], bool]) -> "StrategyLibrary":
        return StrategyLibrary(filter(predicate, self))

    def apply(self, func: Callable[[Book], Any]) -> List[Any]:
        return list(map(func, self))
