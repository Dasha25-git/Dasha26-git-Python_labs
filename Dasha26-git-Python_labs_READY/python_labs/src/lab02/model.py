from __future__ import annotations

from .validate import (
    validate_condition,
    validate_int_range,
    validate_nonempty_str,
    validate_price,
)


class Book:
    currency: str = "RUB"

    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        pages: int,
        price: float,
        condition: str = "available",
    ) -> None:
        validate_nonempty_str(title, "title")
        validate_nonempty_str(author, "author")
        validate_int_range(year, "year", min_value=1450, max_value=2026)
        validate_int_range(pages, "pages", min_value=10, max_value=5000)
        validate_price(price)
        validate_condition(condition)

        self._title = title.strip()
        self._author = author.strip()
        self._year = year
        self._pages = pages
        self._price = float(price)
        self._condition = condition

    @property
    def title(self) -> str:
        return self._title

    @property
    def author(self) -> str:
        return self._author

    @property
    def year(self) -> int:
        return self._year

    @property
    def pages(self) -> int:
        return self._pages

    @property
    def price(self) -> float:
        return self._price

    @property
    def condition(self) -> str:
        return self._condition

    @property
    def available(self) -> bool:
        """Вычисляемое свойство: книга доступна, если condition == 'available'."""
        return self._condition == "available"

    @price.setter
    def price(self, value: float) -> None:
        validate_price(value)
        self._price = float(value)

    def mark_borrowed(self) -> None:
        """Выдать книгу (перевести в состояние 'borrowed')."""
        if self._condition != "available":
            raise ValueError(
                f"Нельзя выдать книгу в состоянии '{self._condition}'. "
                "Доступны только книги в состоянии 'available'."
            )
        self._condition = "borrowed"

    def mark_returned(self) -> None:
        """Вернуть книгу (перевести в состояние 'available')."""
        if self._condition != "borrowed":
            raise ValueError(
                f"Нельзя вернуть книгу в состоянии '{self._condition}'. "
                "Книга должна быть в состоянии 'borrowed'."
            )
        self._condition = "available"

    def mark_damaged(self) -> None:
        """Повредить книгу (перевести в состояние 'damaged')."""
        if self._condition not in ("available", "borrowed"):
            raise ValueError(
                f"Нельзя повредить книгу в состоянии '{self._condition}'. "
                "Повредить можно только доступную или выданную книгу."
            )
        self._condition = "damaged"

    def repair(self) -> None:
        """Отремонтировать книгу (перевести из 'damaged' в 'available')."""
        if self._condition != "damaged":
            raise ValueError(
                f"Нельзя отремонтировать книгу в состоянии '{self._condition}'. "
                "Ремонт возможен только для повреждённых книг."
            )
        self._condition = "available"

    def mark_lost(self) -> None:
        """Пометить книгу как утерянную (перевести в состояние 'lost')."""
        if self._condition == "lost":
            raise ValueError("Книга уже утеряна.")
        self._condition = "lost"

    def apply_discount(self, percent: float) -> float:
        """Применить скидку к цене. Только для доступных книг."""
        if self._condition != "available":
            raise ValueError(
                f"Нельзя применить скидку к книге в состоянии '{self._condition}'. "
                "Скидка доступна только для доступных книг."
            )
        if not isinstance(percent, (int, float)) or isinstance(percent, bool):
            raise TypeError("percent должен быть числом (int или float).")
        if percent <= 0 or percent >= 100:
            raise ValueError("percent должен быть в диапазоне (0, 100).")
        new_price = self._price * (1 - percent / 100)
        self.price = new_price
        return self._price

    def __str__(self) -> str:
        status_map = {
            "available": "доступна",
            "borrowed": "выдана",
            "damaged": "повреждена",
            "lost": "утеряна",
        }
        status = status_map.get(self._condition, self._condition)
        return (
            f"Книга: «{self._title}» — {self._author} ({self._year}), "
            f"{self._pages:,} стр., {self._price:,.2f} {self.currency}, статус: {status}"
        )

    def __repr__(self) -> str:
        return (
            "Book("
            f"title={self._title!r}, author={self._author!r}, year={self._year!r}, "
            f"pages={self._pages!r}, price={self._price!r}, condition={self._condition!r}"
            ")"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return (
            self._title.lower(),
            self._author.lower(),
            self._year,
        ) == (
            other._title.lower(),
            other._author.lower(),
            other._year,
        )

