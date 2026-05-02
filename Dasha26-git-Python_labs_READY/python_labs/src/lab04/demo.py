"""Демонстрация ЛР-4: ABC-интерфейсы."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.lab04.interfaces import Borrowable, Comparable, Printable, borrow_all, print_all, sort_comparable
from src.lab04.models import InterfaceLibrary, interface_sample_books


def print_header(title: str) -> None:
    print(f"\n{'=' * 12} {title} {'=' * 12}")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    library = InterfaceLibrary(interface_sample_books())

    print_header("Сценарий 1. Printable как тип")
    for line in print_all(library.get_printable()):
        print("-", line)

    print_header("Сценарий 2. Comparable и универсальная сортировка")
    for item in sort_comparable(library.get_comparable()):
        print("-", item.to_string())

    print_header("Сценарий 3. Фильтрация коллекции по интерфейсам")
    print(f"Printable: {len(library.get_printable())}")
    print(f"Comparable: {len(library.get_comparable())}")
    print(f"Borrowable: {len(library.get_borrowable())}")

    print_header("Сценарий 4. Borrowable без знания конкретного класса")
    available_for_borrow = [book for book in library.get_borrowable() if getattr(book, "available", False)]
    for line in borrow_all(available_for_borrow[:3], "Дарья"):
        print("-", line)

    print_header("Сценарий 5. isinstance() и множественная реализация")
    for book in library:
        print(
            f"{book.title}: Printable={isinstance(book, Printable)}, "
            f"Comparable={isinstance(book, Comparable)}, "
            f"Borrowable={isinstance(book, Borrowable)}"
        )


if __name__ == "__main__":
    main()
