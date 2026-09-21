from datetime import date

def input_int(prompt: str) -> int:
    """Запрос целого числа у пользователя с обработкой ошибок."""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Ошибка: введите корректное число.")

def input_date(prompt: str) -> date:
    """Запрос даты в формате ДД.ММ.ГГГГ."""
    while True:
        date_str = input(prompt)
        try:
            day, month, year = map(int, date_str.split('.'))
            return date(year, month, day)
        except (ValueError, TypeError):
            print("Ошибка: введите дату в формате ДД.ММ.ГГГГ")