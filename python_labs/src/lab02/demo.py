"""Демонстрация работы контейнера Library и модели Book."""

from __future__ import annotations

import sys

from .collection import Library
from .model import Book


def print_books(title: str, books: list[Book] | Library) -> None:
    print(f"\n{title}")
    for book in books:
        print(f"- {book}")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 72)
    print("Лабораторная работа №2. Контейнер Library для объектов Book")
    print("=" * 72)

    library = Library()

    book1 = Book("Война и мир", "Лев Толстой", 1869, 1225, 450.0)
    book2 = Book("Преступление и наказание", "Фёдор Достоевский", 1866, 672, 350.0)
    book3 = Book("Мастер и Маргарита", "Михаил Булгаков", 1967, 480, 500.0)
    book4 = Book("Идиот", "Фёдор Достоевский", 1869, 640, 420.0, condition="borrowed")
    book5 = Book("Чистый код", "Роберт Мартин", 2008, 464, 1300.0)

    print("\nСценарий 1. Создание книг, добавление в библиотеку, вывод через for")
    for book in (book1, book2, book3, book4, book5):
        library.add(book)

    for book in library:
        print(book)

    print("\nПоказываем ошибку при добавлении дубликата:")
    duplicate = Book("Война и мир", "Лев Толстой", 1869, 1400, 470.0)
    try:
        library.add(duplicate)
    except ValueError as error:
        print(f"Ошибка: {error}")

    print("\nСценарий 2. Поиск, len() и индексация")
    found_by_title = library.find_by_title("код")
    found_by_author = library.find_by_author("достоевский")
    print_books("Результат поиска по названию 'код':", found_by_title)
    print_books("Результат поиска по автору 'достоевский':", found_by_author)
    print(f"\nКоличество книг в библиотеке: {len(library)}")
    print(f"Книга по индексу [0]: {library[0]}")

    print("\nСценарий 3. Сортировка, фильтрация и удаление")
    library.sort_by_price()
    print_books("После сортировки по цене:", library)

    library.sort_by_year(reverse=True)
    print_books("После сортировки по году (по убыванию):", library)

    available_books = library.get_available()
    expensive_books = library.get_expensive(500)
    print_books("Новая коллекция доступных книг:", available_books)
    print_books("Новая коллекция дорогих книг (от 500 RUB):", expensive_books)

    removed_book = library.remove_at(1)
    print(f"\nУдалена по индексу книга: {removed_book}")
    library.remove(book1)
    print(f"После удаления '{book1.title}' по объекту осталось книг: {len(library)}")
    print_books("Итоговое содержимое библиотеки:", library)

    print("\nДемонстрация завершена успешно.")


if __name__ == "__main__":
    main()
