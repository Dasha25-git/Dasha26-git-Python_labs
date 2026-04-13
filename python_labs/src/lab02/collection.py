from __future__ import annotations

from .model import Book


class Library:
    """Контейнер для хранения объектов Book."""

    def __init__(self, items: list[Book] | None = None) -> None:
        self._items: list[Book] = []
        if items is not None:
            for book in items:
                self.add(book)

    def add(self, book: Book) -> None:
        self._validate_book(book)
        if book in self._items:
            raise ValueError("Нельзя добавить дубликат книги в библиотеку.")
        self._items.append(book)

    def remove(self, book: Book) -> None:
        self._validate_book(book)
        if book not in self._items:
            raise ValueError("Книга не найдена в библиотеке.")
        self._items.remove(book)

    def remove_at(self, index: int) -> Book:
        return self._items.pop(index)

    def get_all(self) -> list[Book]:
        return self._items.copy()

    def find_by_title(self, title: str) -> list[Book]:
        if not isinstance(title, str):
            raise TypeError("title должен быть строкой.")
        query = title.strip().lower()
        return [book for book in self._items if query in book.title.lower()]

    def find_by_author(self, author: str) -> list[Book]:
        if not isinstance(author, str):
            raise TypeError("author должен быть строкой.")
        query = author.strip().lower()
        return [book for book in self._items if query in book.author.lower()]

    def sort_by_price(self, reverse: bool = False) -> None:
        self._items.sort(key=lambda book: book.price, reverse=reverse)

    def sort_by_year(self, reverse: bool = False) -> None:
        self._items.sort(key=lambda book: book.year, reverse=reverse)

    def get_available(self) -> Library:
        return Library([book for book in self._items if book.available])

    def get_expensive(self, min_price: float) -> Library:
        if not isinstance(min_price, (int, float)) or isinstance(min_price, bool):
            raise TypeError("min_price должен быть числом (int или float).")
        return Library([book for book in self._items if book.price >= float(min_price)])

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index: int) -> Book:
        return self._items[index]

    @staticmethod
    def _validate_book(book: Book) -> None:
        if not isinstance(book, Book):
            raise TypeError("Можно добавлять и удалять только объекты Book.")

