"""Функции-стратегии и callable-объекты для ЛР-5."""

from __future__ import annotations

from typing import Any, Callable, Dict, Tuple

from src.lab02.model import Book
from src.lab03.models import AudioBook, EBook, PrintedBook


def by_title(book: Book) -> Tuple[str, str]:
    """Вернуть ключ сортировки по названию и автору."""

    return (book.title.lower(), book.author.lower())


def by_price(book: Book) -> float:
    """Вернуть ключ сортировки по цене."""

    return book.price


def by_year_then_title(book: Book) -> Tuple[int, str]:
    """Вернуть ключ сортировки по году издания и названию."""

    return (book.year, book.title.lower())


def is_available(book: Book) -> bool:
    """Проверить, доступна ли книга."""

    return book.available


def is_ebook(book: Book) -> bool:
    """Проверить, является ли книга электронной."""

    return isinstance(book, EBook)


def is_long_reading(book: Book) -> bool:
    """Проверить, требует ли книга больше 12 часов чтения или прослушивания."""

    return book.calculate_reading_time() > 12


def make_price_filter(max_price: float) -> Callable[[Book], bool]:
    """Создать фильтр книг не дороже указанной цены."""

    def predicate(book: Book) -> bool:
        return book.price <= max_price

    return predicate


def make_year_filter(min_year: int) -> Callable[[Book], bool]:
    """Создать фильтр книг, изданных не раньше указанного года."""

    def predicate(book: Book) -> bool:
        return book.year >= min_year

    return predicate


def make_type_filter(book_type: type) -> Callable[[Book], bool]:
    """Создать фильтр по классу книги."""

    def predicate(book: Book) -> bool:
        return isinstance(book, book_type)

    return predicate


def to_summary(book: Book) -> str:
    """Преобразовать книгу в короткое описание для вывода."""

    return (
        f"«{book.title}» — {book.author}, {book.year}, "
        f"{book.price:.2f} {book.currency}, доступна={book.available}"
    )


def to_dict(book: Book) -> Dict[str, Any]:
    """Преобразовать книгу в словарь для отчёта."""

    return {
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "price": book.price,
        "condition": book.condition,
        "type": book.__class__.__name__,
    }


def reading_card(hours_label: str = "ч.") -> Callable[[Book], str]:
    """Создать mapper для вывода времени чтения."""

    def mapper(book: Book) -> str:
        return f"«{book.title}»: примерно {book.calculate_reading_time():.1f} {hours_label}"

    return mapper


class DiscountStrategy:
    """Callable-стратегия расчёта цены со скидкой без изменения объекта."""

    def __init__(self, percent: float) -> None:
        self.percent = percent

    def __call__(self, book: Book) -> str:
        discounted = book.price * (1 - self.percent / 100)
        return f"«{book.title}»: {discounted:.2f} {book.currency} со скидкой {self.percent:g}%"


class AccessStrategy:
    """Callable-стратегия описания доступа к книге."""

    def __call__(self, book: Book) -> str:
        return book.access_description()


class FormatLabelStrategy:
    """Callable-стратегия, которая возвращает метку формата книги."""

    def __call__(self, book: Book) -> str:
        if isinstance(book, EBook):
            return f"«{book.title}»: электронная книга {book.file_format}"
        if isinstance(book, AudioBook):
            return f"«{book.title}»: аудиокнига, {book.duration_minutes} мин."
        if isinstance(book, PrintedBook):
            return f"«{book.title}»: печатная книга, полка {book.shelf_code}"
        return f"«{book.title}»: базовая книга"

