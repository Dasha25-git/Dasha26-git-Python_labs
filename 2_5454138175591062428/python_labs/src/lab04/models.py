"""Классы книг, реализующие интерфейсы ЛР-4."""

from __future__ import annotations

from typing import Iterable, List, Type, TypeVar

from src.lab02.model import Book
from src.lab03.models import AudioBook, EBook, MediaLibrary, PrintedBook
from src.lab04.interfaces import Borrowable, Comparable, Printable, print_all, sort_comparable

TInterface = TypeVar("TInterface")


def _compare_numbers(left: float, right: float) -> int:
    return (left > right) - (left < right)


class InterfacePrintedBook(PrintedBook, Printable, Comparable, Borrowable):
    """Печатная книга с реализацией нескольких интерфейсов."""

    @property
    def interface_priority(self) -> float:
        return self.calculate_storage_cost()

    def to_string(self) -> str:
        return (
            f"PRINT: «{self.title}», {self.author}, полка {self.shelf_code}, "
            f"хранение {self.calculate_storage_cost():.2f} RUB"
        )

    def compare_to(self, other: Comparable) -> int:
        other_priority = getattr(other, "interface_priority", 0)
        return _compare_numbers(self.interface_priority, other_priority)

    def borrow(self, reader_name: str) -> str:
        if not self.available:
            return f"«{self.title}» нельзя выдать: состояние '{self.condition}'."
        self.mark_borrowed()
        return f"Печатная книга «{self.title}» выдана читателю {reader_name}."


class InterfaceEBook(EBook, Printable, Comparable, Borrowable):
    """Электронная книга с реализацией нескольких интерфейсов."""

    @property
    def interface_priority(self) -> float:
        return self.file_size_mb

    def to_string(self) -> str:
        return (
            f"EBOOK: «{self.title}», формат {self.file_format}, "
            f"размер {self.file_size_mb:.1f} МБ, ссылка {self.generate_download_link()}"
        )

    def compare_to(self, other: Comparable) -> int:
        other_priority = getattr(other, "interface_priority", 0)
        return _compare_numbers(self.interface_priority, other_priority)

    def borrow(self, reader_name: str) -> str:
        if not self.available:
            return f"Электронная книга «{self.title}» недоступна."
        return f"Читателю {reader_name} отправлена ссылка: {self.generate_download_link()}."


class InterfaceAudioBook(AudioBook, Printable, Comparable, Borrowable):
    """Аудиокнига с реализацией нескольких интерфейсов."""

    @property
    def interface_priority(self) -> float:
        return self.duration_minutes / 60

    def to_string(self) -> str:
        return (
            f"AUDIO: «{self.title}», диктор {self.narrator}, "
            f"длительность {self.duration_minutes} мин."
        )

    def compare_to(self, other: Comparable) -> int:
        other_priority = getattr(other, "interface_priority", 0)
        return _compare_numbers(self.interface_priority, other_priority)

    def borrow(self, reader_name: str) -> str:
        if not self.available:
            return f"Аудиокнига «{self.title}» недоступна."
        return f"Читателю {reader_name} открыт доступ к аудиокниге «{self.title}»."


def interface_sample_books() -> List[Printable]:
    """Создать книги, реализующие интерфейсы."""

    return [
        InterfacePrintedBook("Война и мир", "Лев Толстой", 1869, 1225, 450.0, "твёрдая", "A-01"),
        InterfacePrintedBook("Идиот", "Фёдор Достоевский", 1869, 640, 420.0, "мягкая", "B-14", condition="borrowed"),
        InterfaceEBook("Чистый код", "Роберт Мартин", 2008, 464, 1300.0, "PDF", 8.6),
        InterfaceEBook("Python. К вершинам мастерства", "Лучано Рамальо", 2022, 1014, 2100.0, "EPUB", 12.4),
        InterfaceAudioBook("Мастер и Маргарита", "Михаил Булгаков", 1967, 480, 650.0, "Сергей Чонишвили", 780),
        InterfaceAudioBook("1984", "Джордж Оруэлл", 1949, 328, 500.0, "Александр Клюквин", 645),
    ]


class InterfaceLibrary(MediaLibrary):
    """Библиотека, которая работает с объектами через интерфейсы."""

    def __init__(self, items: Iterable[Book] = ()) -> None:
        super().__init__(items)

    def filter_by_interface(self, interface_type: Type[TInterface]) -> List[TInterface]:
        return [book for book in self if isinstance(book, interface_type)]

    def get_printable(self) -> List[Printable]:
        return self.filter_by_interface(Printable)

    def get_comparable(self) -> List[Comparable]:
        return self.filter_by_interface(Comparable)

    def get_borrowable(self) -> List[Borrowable]:
        return self.filter_by_interface(Borrowable)

    def render_printable(self) -> List[str]:
        return print_all(self.get_printable())

    def sort_via_comparable(self) -> List[Comparable]:
        return sort_comparable(self.get_comparable())
