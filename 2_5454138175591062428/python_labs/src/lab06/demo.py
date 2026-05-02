"""Демонстрация ЛР-6: Generics, TypeVar и Protocol."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.lab01.model import Book as Lab01Book
from src.lab03.models import AudioBook, EBook, PrintedBook
from src.lab06.container import Displayable, Scorable, TypedCollection


def print_header(title: str) -> None:
    print(f"\n{'=' * 12} {title} {'=' * 12}")


def print_lines(title: str, lines: list[object]) -> None:
    print(f"\n{title}:")
    for line in lines:
        print("-", line)


def make_lab01_books() -> list[Lab01Book]:
    return [
        Lab01Book("Война и мир", "Лев Толстой", 1869, 1225, 450.0),
        Lab01Book("Преступление и наказание", "Фёдор Достоевский", 1866, 672, 350.0),
        Lab01Book("Чистый код", "Роберт Мартин", 2008, 464, 1300.0),
    ]


def make_media_books() -> list[Displayable]:
    return [
        PrintedBook("Война и мир", "Лев Толстой", 1869, 1225, 450.0, "твёрдая", "A-01"),
        EBook("Чистый код", "Роберт Мартин", 2008, 464, 1300.0, "PDF", 8.6),
        AudioBook("Мастер и Маргарита", "Михаил Булгаков", 1967, 480, 650.0, "Сергей Чонишвили", 780),
    ]


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print_header("Сценарий 1. TypedCollection[Book] и проверка типа")
    books: TypedCollection[Lab01Book] = TypedCollection(Lab01Book)
    for book in make_lab01_books():
        books.add(book)

    for book in books.get_all():
        print("-", book.display())

    try:
        books.add("не книга")  # type: ignore[arg-type]
    except TypeError as error:
        print("Проверка типа при добавлении:", error)

    print_header("Сценарий 2. Методы коллекции из ЛР-2 с типами")
    print_lines("Поиск по названию 'код'", books.find_by_title("код"))
    print_lines("Поиск по автору 'достоевский'", books.find_by_author("достоевский"))
    print_lines("Доступные книги", books.get_available().get_all())
    print_lines("Дорогие книги от 500 RUB", books.get_expensive(500).get_all())
    books.sort_by_price()
    print_lines("После sort_by_price()", books.get_all())

    print_header("Сценарий 3. find/filter/map")
    found = books.find(lambda book: book.price < 500)
    not_found = books.find(lambda book: book.price > 3000)
    filtered = books.filter(lambda book: book.year >= 1900)
    titles: list[str] = books.map(lambda book: book.title)
    prices: list[float] = books.map(lambda book: book.price)
    print("find(price < 500):", found)
    print("find(price > 3000):", not_found)
    print_lines("filter(year >= 1900)", filtered)
    print_lines("map -> list[str]", titles)
    print_lines("map -> list[float]", prices)

    print_header("Сценарий 4. Protocol Displayable без наследования")
    displayable_books: TypedCollection[Displayable] = TypedCollection(Displayable)
    for book in make_media_books():
        displayable_books.add(book)
    print_lines("display_all()", displayable_books.display_all())

    print_header("Сценарий 5. Protocol Scorable с тем же TypedCollection")
    scorable_books: TypedCollection[Scorable] = TypedCollection(Scorable)
    for book in make_media_books():
        scorable_books.add(book)
    print_lines("score_all()", scorable_books.score_all())
    best = scorable_books.find(lambda book: book.score() > 2)
    print("find(score > 2):", best.display() if best is not None else None)


if __name__ == "__main__":
    main()

