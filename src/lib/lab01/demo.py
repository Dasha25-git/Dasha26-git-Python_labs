from model import Book


def main() -> None:
    book1 = Book(
        title="Мастер и Маргарита",
        author="Михаил Булгаков",
        year=1967,
        pages=416,
        price=600,
        available=True,
    )

    print(book1)

    print("repr:", repr(book1))

    book2 = Book(
        title="Мастер и Маргарита",
        author="Михаил Булгаков",
        year=1967,
        pages=500,  
        price=750,
        available=False,
    )
    print("book1 == book2:", book1 == book2)


    try:
        bad_book = Book(
            title="Мастер и Маргарита",      
            author="Михаил Булгаков",
            year=1967,        
            pages=5500,          
            price=600,        
            available="yes",  
        )
        print(bad_book)  
    except (TypeError, ValueError) as e:
        print("Ошибка при создании объекта:", e)

    print("\nИзменение цены через setter:")
    print("Старая цена:", f"{book1.price:,.2f} {Book.currency}")
    book1.price = 900
    print("Новая цена:", f"{book1.price:,.2f} {Book.currency}")

    try:
        book1.price = -100
    except (TypeError, ValueError) as e:
        print("\nПопытка поставить некорректную цену:", e)

    print("\nАтрибут класса currency:")
    print("Через класс:", Book.currency)
    print("Через экземпляр:", book1.currency)

    print("\nСкидка 20%:")
    book1.apply_discount(20)
    print(book1)

    print("\nВыдача книги:")
    book1.mark_borrowed()
    print(book1)

    print("\nВозврат книги:")
    book1.mark_returned()
    print(book1)

    try:
        book1.mark_returned()
    except ValueError as e:
        print("Проверка ограничения (return):", e)


if __name__ == "__main__":
    main()