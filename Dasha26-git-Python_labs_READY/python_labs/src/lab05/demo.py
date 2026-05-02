"""Демонстрация ЛР-5: функции как аргументы и стратегии."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.lab03.models import EBook, sample_books
from src.lab05.collection import StrategyLibrary
from src.lab05.strategies import (
    AccessStrategy,
    DiscountStrategy,
    FormatLabelStrategy,
    by_price,
    by_title,
    by_year_then_title,
    is_available,
    is_ebook,
    is_long_reading,
    make_price_filter,
    make_type_filter,
    make_year_filter,
    reading_card,
    to_dict,
    to_summary,
)


def print_header(title: str) -> None:
    print(f"\n{'=' * 12} {title} {'=' * 12}")


def print_lines(title: str, lines: list[object]) -> None:
    print(f"\n{title}:")
    for line in lines:
        print("-", line)


def print_library(title: str, library: StrategyLibrary) -> None:
    print(f"\n{title} ({len(library)}):")
    for book in library:
        print("-", to_summary(book))


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    library = StrategyLibrary(sample_books())

    print_header("Сценарий 1. Три стратегии сортировки")
    print_library("По названию", library.sort_by(by_title))
    print_library("По цене", library.sort_by(by_price))
    print_library("По году и названию", library.sort_by(by_year_then_title))

    print_header("Сценарий 2. filter(), фабрики функций и lambda")
    ebooks = list(filter(is_ebook, library))
    print_lines("filter(is_ebook, library)", list(map(to_summary, ebooks)))
    print_library("Фабрика make_price_filter(700)", library.filter_by(make_price_filter(700)))
    print_library("Фабрика make_year_filter(2000)", library.filter_by(make_year_filter(2000)))
    named_result = library.filter_by(is_long_reading)
    lambda_result = library.filter_by(lambda book: book.calculate_reading_time() > 12)
    print(f"Именованная функция и lambda дали одинаковый размер: {len(named_result)} == {len(lambda_result)}")

    print_header("Сценарий 3. map() и преобразование коллекции")
    print_lines("map(lambda book: book.title, library)", list(map(lambda book: book.title, library)))
    print_lines("map(to_dict, library) первые 3", list(map(to_dict, library))[:3])
    print_lines("library.apply(reading_card())", library.apply(reading_card()))

    print_header("Сценарий 4. Полная цепочка filter -> sort -> apply")
    chain_result = (
        library
        .filter_by(is_available)
        .filter_by(make_price_filter(1500))
        .sort_by(by_price)
        .apply(AccessStrategy())
    )
    print_lines("Доступные книги до 1500 RUB по возрастанию цены", chain_result)

    print_header("Сценарий 5. Замена стратегии без изменения коллекции")
    print_lines("DiscountStrategy(15)", library.apply(DiscountStrategy(15)))
    print_lines("FormatLabelStrategy()", library.apply(FormatLabelStrategy()))

    print_header("Сценарий 6. Фильтрация по типу через фабрику")
    type_filter = make_type_filter(EBook)
    print_library("Только EBook", library.filter_by(type_filter))


if __name__ == "__main__":
    main()

