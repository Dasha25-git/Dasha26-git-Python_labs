"""Базовый класс для ЛР-3.

Старый класс Book из ЛР-1/ЛР-2 не изменяется. Здесь создаётся расширение,
которое наследует исходный Book и добавляет общий интерфейс поведения для
новой иерархии.
"""

from __future__ import annotations

from src.lab02.model import Book as LabBook


class Book(LabBook):
    """Расширенный Book для наследников ЛР-3."""

    def calculate_reading_time(self, pages_per_hour: int = 35) -> float:
        """Рассчитать примерное время чтения в часах."""
        if not isinstance(pages_per_hour, int) or isinstance(pages_per_hour, bool):
            raise TypeError("pages_per_hour должен быть целым числом.")
        if pages_per_hour <= 0:
            raise ValueError("pages_per_hour должен быть положительным.")
        return round(self.pages / pages_per_hour, 1)

    def access_description(self) -> str:
        """Описать базовый способ доступа к книге."""
        if self.available:
            return f"«{self.title}» можно взять в библиотеке."
        return f"«{self.title}» сейчас недоступна: состояние '{self.condition}'."

    def display(self) -> str:
        """Единый метод отображения для полиморфных сценариев."""
        return str(self)

    def score(self) -> float:
        """Вернуть условную оценку книги для структурного протокола Scorable."""
        condition_bonus = 1.0 if self.available else 0.0
        reading_balance = max(0.0, 1 - self.calculate_reading_time() / 40)
        price_balance = max(0.0, 1 - self.price / 5000)
        return round(condition_bonus + reading_balance + price_balance, 2)

    def process(self) -> str:
        """Единая операция обработки книги."""
        return self.access_description()
