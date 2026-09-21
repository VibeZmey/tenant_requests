from utils import input_int, input_date
from storage import load_data, save_data
from request_manager import create_request, find_requests_by_flat, get_status_text
from datetime import date

def show_menu() -> None:
    print("\n=== СИСТЕМА УПРАВЛЕНИЯ ЗАЯВКАМИ ===")
    print("1. Создать новую заявку")
    print("2. Посмотреть заявки по квартире")
    print("3. Показать все заявки")
    print("0. Выход")

def main() -> None:
    requests = load_data("requests.json")

    while True:
        show_menu()
        choice = input_int("Выберите действие: ")

        if choice == 1:
            name = input("ФИО жильца: ")
            flat = input_int("Номер квартиры: ")
            problem = input("Описание проблемы: ")
            req_date = input_date("Дата заявки (ДД.ММ.ГГГГ): ")

            new_req = create_request(requests, name, flat, problem, req_date)
            print(f"Заявка №{new_req['id']} успешно создана!")
            save_data("requests.json", requests)  # Сохраняем после изменения

        elif choice == 2:
            flat = input_int("Введите номер квартиры для поиска: ")
            found = find_requests_by_flat(requests, flat)
            if not found:
                print("Заявок не найдено.")
            else:
                for req in found:
                    print(f"№{req['id']}: {req['problem']} | Статус: {get_status_text(req['status'])}")

        elif choice == 3:
            if not requests:
                print("Список заявок пуст.")
            else:
                for req in requests:
                    print(f"№{req['id']} | Кв. {req['flat']} | {req['tenant']} | {req['date']}")

        elif choice == 0:
            print("До свидания!")
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()