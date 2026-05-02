"""Иерархия классов книг для ЛР-3."""

from __future__ import annotations

from typing import Callable, Iterable, List, Type, TypeVar

from src.lab02.collection import Library
from src.lab02.model import Book as LabBook
from src.lab03.base import Book

TBook = TypeVar("TBook", bound=LabBook)


class PrintedBook(Book):
    """Печатная книга с физическим расположением в библиотеке."""

    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        pages: int,
        price: float,
        cover_type: str,
        shelf_code: str,
        condition: str = "available",
    ) -> None:
        super().__init__(title, author, year, pages, price, condition)
        self._validate_text(cover_type, "cover_type")
        self._validate_text(shelf_code, "shelf_code")
        self.cover_type = cover_type.strip()
        self.shelf_code = shelf_code.strip().upper()

    @staticmethod
    def _validate_text(value: object, field_name: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{field_name} должен быть строкой.")
        if not value.strip():
            raise ValueError(f"{field_name} не должен быть пустым.")

    def reserve_shelf_place(self) -> str:
        """Зарезервировать место на полке."""
        return f"Для печатной книги «{self.title}» закреплена полка {self.shelf_code}."

    def calculate_storage_cost(self) -> float:
        """Рассчитать стоимость хранения печатной книги."""
        cover_multiplier = 1.25 if self.cover_type.lower() == "твёрдая" else 1.0
        return round(self.pages * 0.08 * cover_multiplier, 2)

    def access_description(self) -> str:
        if not self.available:
            return f"Печатная книга «{self.title}» сейчас недоступна."
        return f"Печатная книга «{self.title}» доступна на полке {self.shelf_code}."

    def process(self) -> str:
        return (
            f"{self.title}: печатный экземпляр, чтение около "
            f"{self.calculate_reading_time():.1f} ч., хранение {self.calculate_storage_cost():.2f} RUB."
        )

    def __str__(self) -> str:
        return f"{super().__str__()}, обложка: {self.cover_type}, полка: {self.shelf_code}"


class EBook(Book):
    """Электронная книга с форматом файла и размером."""

    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        pages: int,
        price: float,
        file_format: str,
        file_size_mb: float,
        condition: str = "available",
    ) -> None:
        super().__init__(title, author, year, pages, price, condition)
        self._validate_text(file_format, "file_format")
        if not isinstance(file_size_mb, (int, float)) or isinstance(file_size_mb, bool):
            raise TypeError("file_size_mb должен быть числом.")
        if file_size_mb <= 0:
            raise ValueError("file_size_mb должен быть положительным.")
        self.file_format = file_format.strip().upper()
        self.file_size_mb = float(file_size_mb)

    @staticmethod
    def _validate_text(value: object, field_name: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{field_name} должен быть строкой.")
        if not value.strip():
            raise ValueError(f"{field_name} не должен быть пустым.")

    def generate_download_link(self) -> str:
        """Сформировать ссылку на скачивание."""
        slug = self.title.lower().replace(" ", "-")
        return f"https://library.local/ebooks/{slug}.{self.file_format.lower()}"

    def calculate_storage_cost(self) -> float:
        return round(self.file_size_mb * 0.12, 2)

    def calculate_reading_time(self, pages_per_hour: int = 45) -> float:
        return super().calculate_reading_time(pages_per_hour)

    def access_description(self) -> str:
        if not self.available:
            return f"Электронная книга «{self.title}» заблокирована для выдачи."
        return f"Электронная книга «{self.title}» доступна для скачивания в формате {self.file_format}."

    def process(self) -> str:
        return (
            f"{self.title}: электронная версия {self.file_format}, "
            f"файл {self.file_size_mb:.1f} МБ, ссылка {self.generate_download_link()}."
        )

    def __str__(self) -> str:
        return f"{super().__str__()}, формат: {self.file_format}, размер: {self.file_size_mb:.1f} МБ"


class AudioBook(Book):
    """Аудиокнига с диктором и длительностью записи."""

    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        pages: int,
        price: float,
        narrator: str,
        duration_minutes: int,
        condition: str = "available",
    ) -> None:
        super().__init__(title, author, year, pages, price, condition)
        self._validate_text(narrator, "narrator")
        if not isinstance(duration_minutes, int) or isinstance(duration_minutes, bool):
            raise TypeError("duration_minutes должен быть целым числом.")
        if duration_minutes <= 0:
            raise ValueError("duration_minutes должен быть положительным.")
        self.narrator = narrator.strip()
        self.duration_minutes = duration_minutes

    @staticmethod
    def _validate_text(value: object, field_name: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{field_name} должен быть строкой.")
        if not value.strip():
            raise ValueError(f"{field_name} не должен быть пустым.")

    def listen_preview(self, minutes: int = 5) -> str:
        """Прослушать фрагмент аудиокниги."""
        if not isinstance(minutes, int) or isinstance(minutes, bool):
            raise TypeError("minutes должен быть целым числом.")
        if minutes <= 0:
            raise ValueError("minutes должен быть положительным.")
        preview = min(minutes, self.duration_minutes)
        return f"Доступен фрагмент аудиокниги «{self.title}»: {preview} мин."

    def calculate_storage_cost(self) -> float:
        return round(self.duration_minutes * 0.05, 2)

    def calculate_reading_time(self, pages_per_hour: int = 35) -> float:
        return round(self.duration_minutes / 60, 1)

    def access_description(self) -> str:
        if not self.available:
            return f"Аудиокнига «{self.title}» сейчас недоступна."
        return f"Аудиокнига «{self.title}» доступна для прослушивания, диктор: {self.narrator}."

    def process(self) -> str:
        return (
            f"{self.title}: аудиоверсия, диктор {self.narrator}, "
            f"длительность {self.duration_minutes} мин."
        )

    def __str__(self) -> str:
        return f"{super().__str__()}, диктор: {self.narrator}, длительность: {self.duration_minutes} мин."


def sample_books() -> List[Book]:
    """Создать набор разных книг для демонстраций ЛР-3/4/5."""

    return [
        PrintedBook("Война и мир", "Лев Толстой", 1869, 1225, 450.0, "твёрдая", "A-01"),
        PrintedBook("Идиот", "Фёдор Достоевский", 1869, 640, 420.0, "мягкая", "B-14", condition="borrowed"),
        EBook("Чистый код", "Роберт Мартин", 2008, 464, 1300.0, "PDF", 8.6),
        EBook("Python. К вершинам мастерства", "Лучано Рамальо", 2022, 1014, 2100.0, "EPUB", 12.4),
        AudioBook("Мастер и Маргарита", "Михаил Булгаков", 1967, 480, 650.0, "Сергей Чонишвили", 780),
        AudioBook("1984", "Джордж Оруэлл", 1949, 328, 500.0, "Александр Клюквин", 645),
    ]


class MediaLibrary(Library):
    """Коллекция из ЛР-2, расширенная для иерархии книг."""

    def __init__(self, items: Iterable[LabBook] = ()) -> None:
        super().__init__()
        for book in items:
            self.add(book)

    def filter_by_type(self, book_type: Type[TBook]) -> "MediaLibrary":
        if not isinstance(book_type, type) or not issubclass(book_type, LabBook):
            raise TypeError("book_type должен быть классом-наследником Book.")
        return MediaLibrary(book for book in self if isinstance(book, book_type))

    def filter_by(self, predicate: Callable[[LabBook], bool]) -> "MediaLibrary":
        return MediaLibrary(book for book in self if predicate(book))

    def get_only_printed(self) -> "MediaLibrary":
        return self.filter_by_type(PrintedBook)

    def get_only_ebooks(self) -> "MediaLibrary":
        return self.filter_by_type(EBook)

    def get_only_audio(self) -> "MediaLibrary":
        return self.filter_by_type(AudioBook)

    def get_available_media(self) -> "MediaLibrary":
        return self.filter_by(lambda book: book.available)

    def sort_by_access_cost(self) -> "MediaLibrary":
        return MediaLibrary(sorted(self, key=lambda book: book.price))

    def process_all(self) -> List[str]:
        return [book.process() for book in self]
