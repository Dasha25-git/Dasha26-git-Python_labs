"""Модуль с функциями валидации для класса Book."""


def validate_nonempty_str(value: object, field_name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} должен быть строкой (str).")
    if not value.strip():
        raise ValueError(f"{field_name} не должен быть пустой строкой.")


def validate_int_range(
    value: object,
    field_name: str,
    *,
    min_value: int,
    max_value: int,
) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{field_name} должен быть целым числом (int).")
    if value < min_value or value > max_value:
        raise ValueError(f"{field_name} должен быть в диапазоне [{min_value}, {max_value}].")


def validate_price(value: object) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError("price должен быть числом (int или float).")
    if value < 0:
        raise ValueError("price должен быть >= 0.")
    if value > 5000:
        raise ValueError("price слишком большой (макс. 5000).")


def validate_condition(value: object) -> None:
    allowed = ("available", "borrowed", "damaged", "lost")
    if not isinstance(value, str):
        raise TypeError("condition должен быть строкой.")
    if value not in allowed:
        raise ValueError(f"condition должен быть одним из: {', '.join(allowed)}.")

