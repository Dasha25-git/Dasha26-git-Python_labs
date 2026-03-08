from __future__ import annotations


class Book:
    currency: str = "RUB"

    # Конструктор класса:
    def __init__(self, title: str, author: str, year: int, pages: int, price: float, available: bool = True,) -> None:
        
        # Валидация (т.е. перед тем, как сохранить значения в объект, убедимся, что они корректные)

        # непустые строки
        self._validate_nonempty_str(title, "title")
        self._validate_nonempty_str(author, "author")
        # диапазон целых чисел
        self._validate_int_range(year, "year", min_value=1450, max_value=2026)
        self._validate_int_range(pages, "pages", min_value=10, max_value=5000)
        # стоимость
        self._validate_price(price)
        # доступность - true/false
        self._validate_bool(available, "available")

        # Создаём поля объекта
        
        # удалим лишние пробелы
        self._title = title.strip()
        self._author = author.strip()

        self._year = year
        self._pages = pages
        self._price = float(price) # цена м.б. дробной
        self._available = available

    # property - декоратор. Исп. метод как атрибут. 
    # это значит, мы можем исп. свойство только для чтения (нельзя изменять)
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
    def available(self) -> bool:
        return self._available

    @property
    def price(self) -> float:
        return self._price

    # setter - разрешаем менять цену!
    @price.setter
    def price(self, value: float) -> None:
        self._validate_price(value)
        self._price = float(value)

    def __str__(self) -> str:
        if self._available:
            status = "доступна"
        else:
            status = "выдана"
        return (
            f"Книга: «{self._title}» — {self._author} ({self._year}), "
            f"{self._pages:,} стр., {self._price:,.2f} {self.currency}, статус: {status}"
        )
    
    # показываем, как должен выглядеть объект
    def __repr__(self) -> str:
        return (
            "Book("
            f"title={self._title!r}, author={self._author!r}, year={self._year!r}, "
            f"pages={self._pages!r}, price={self._price!r}, available={self._available!r}"
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

    def apply_discount(self, percent: float) -> float:
        
        if not isinstance(percent, (int, float)) or isinstance(percent, bool):
            raise TypeError("percent должен быть числом (int или float).")
        if percent <= 0 or percent >= 100:
            raise ValueError("percent должен быть в диапазоне (0, 100).")

        new_price = self._price * (1 - percent / 100)
        self.price = new_price
        return self._price

    def mark_borrowed(self) -> None:
        if not self._available:
            raise ValueError("Нельзя выдать книгу: она уже выдана.")
        self._available = False

    def mark_returned(self) -> None:
        
        if self._available:
            raise ValueError("Нельзя вернуть книгу: она уже доступна.")
        self._available = True
    
    # исп. static, т.к. эти методы ничего не меняют в объекте, только проверяют его значения
    @staticmethod
    def _validate_nonempty_str(value: object, field_name: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{field_name} должен быть строкой (str).")
        if not value.strip():
            raise ValueError(f"{field_name} не должен быть пустой строкой.")

    @staticmethod
    def _validate_bool(value: object, field_name: str) -> None:
        if not isinstance(value, bool):
            raise TypeError(f"{field_name} должен быть bool.")

    @staticmethod
    def _validate_int_range(
        value: object, field_name: str, *, min_value: int, max_value: int
    ) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(f"{field_name} должен быть целым числом (int).")
        if value < min_value or value > max_value:
            raise ValueError(
                f"{field_name} должен быть в диапазоне [{min_value}, {max_value}]."
            )

    @staticmethod
    def _validate_price(value: object) -> None:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError("price должен быть числом (int или float).")
        if value < 0:
            raise ValueError("price должен быть ≥ 0.")
        if value > 5000:
            raise ValueError("price слишком большой (макс. 5000).")