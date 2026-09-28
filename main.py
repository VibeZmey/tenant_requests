"""Точка входа в приложение «Система управления заявками жильцов»."""
from typing import List, Optional

from models import Request, Tenant, Executor
from models.tenants import add_tenant, find_tenant_by_id, show_tenants
from models.executors import (
    add_executor,
    find_free_executor,
    show_executors,
)
from models.requests import (
    create_request,
    find_requests_by_flat,
    find_requests_by_category,
    show_requests,
)
from storage import (
    load_executors,
    load_requests,
    load_tenants,
    save_executors,
    save_requests,
    save_tenants,
)
from utils import input_int, input_date


def show_menu() -> None:
    print("\n=== СИСТЕМА УПРАВЛЕНИЯ ЗАЯВКАМИ ===")
    print("1. Создать новую заявку")
    print("2. Посмотреть заявки по квартире")
    print("3. Показать все заявки")
    print("4. Показать всех жильцов")
    print("5. Показать всех исполнителей")
    print("6. Назначить исполнителя на заявку")
    print("7. Завершить заявку")
    print("8. Отменить заявку")
    print("9. Поиск заявок по категории")
    print("10. Добавить жильца")
    print("11. Добавить исполнителя")
    print("0. Выход")


def create_new_request(
    requests: List[Request],
    tenants: List[Tenant],
) -> None:
    """Сценарий создания новой заявки."""
    tenant_id = input_int("ID жильца: ")
    tenant = find_tenant_by_id(tenants, tenant_id)
    if tenant is None:
        print("Жилец не найден.")
        return

    problem = input("Описание проблемы: ")
    req_date = input_date("Дата заявки (ДД.ММ.ГГГГ): ")

    request = create_request(requests, tenant, problem, req_date)
    print(f"Заявка №{request.id} создана! "
          f"Категория: {request.category}")


def assign_executor_to_request(
    requests: List[Request],
    executors: List[Executor],
) -> None:
    """Назначить исполнителя на заявку."""
    request_id = input_int("ID заявки: ")
    request = next((r for r in requests if r.id == request_id), None)
    if request is None:
        print("Заявка не найдена.")
        return

    executor = find_free_executor(executors, request.category)
    if executor is None:
        print("Нет свободных исполнителей подходящей специализации.")
        return

    if request.assign_executor(executor):
        print(f"Исполнитель {executor.name} назначен на заявку №{request.id}.")
    else:
        print("Не удалось назначить исполнителя.")


def complete_request(requests: List[Request]) -> None:
    """Завершить заявку."""
    request_id = input_int("ID заявки: ")
    request = next((r for r in requests if r.id == request_id), None)
    if request is None:
        print("Заявка не найдена.")
        return
    request.complete()
    print(f"Заявка №{request.id} завершена.")


def cancel_request(requests: List[Request]) -> None:
    """Отменить заявку."""
    request_id = input_int("ID заявки: ")
    request = next((r for r in requests if r.id == request_id), None)
    if request is None:
        print("Заявка не найдена.")
        return
    request.cancel()
    print(f"Заявка №{request.id} отменена.")


def search_by_category(requests: List[Request]) -> None:
    """Поиск заявок по категории."""
    category = input("Категория (электрика/сантехника/уборка/отопление/прочее): ")
    found = find_requests_by_category(requests, category)
    if not found:
        print("Заявок с такой категорией нет.")
        return
    for request in found:
        print(request)


def create_new_tenant(tenants: List[Tenant]) -> None:
    """Добавление нового жильца."""
    name = input("ФИО жильца: ")
    flat = input_int("Номер квартиры: ")
    phone = input("Телефон (необязательно): ")
    tenant = add_tenant(tenants, name, flat, phone)
    print(f"Жилец #{tenant.id} добавлен.")


def create_new_executor(executors: List[Executor]) -> None:
    """Добавление нового исполнителя."""
    name = input("ФИО исполнителя: ")
    specialization = input(
        "Специализация (электрика/сантехника/уборка/отопление): "
    )
    executor = add_executor(executors, name, specialization)
    print(f"Исполнитель #{executor.id} добавлен.")


def main() -> None:
    tenants: List[Tenant] = load_tenants()
    executors: List[Executor] = load_executors()
    requests: List[Request] = load_requests(tenants, executors)

    while True:
        show_menu()
        choice = input_int("Выберите действие: ")

        if choice == 1:
            create_new_request(requests, tenants)
        elif choice == 2:
            flat = input_int("Введите номер квартиры: ")
            found = find_requests_by_flat(requests, flat)
            if not found:
                print("Заявок не найдено.")
            else:
                for request in found:
                    print(request)
        elif choice == 3:
            show_requests(requests)
        elif choice == 4:
            show_tenants(tenants)
        elif choice == 5:
            show_executors(executors)
        elif choice == 6:
            assign_executor_to_request(requests, executors)
        elif choice == 7:
            complete_request(requests)
        elif choice == 8:
            cancel_request(requests)
        elif choice == 9:
            search_by_category(requests)
        elif choice == 10:
            create_new_tenant(tenants)
        elif choice == 11:
            create_new_executor(executors)
        elif choice == 0:
            save_tenants(tenants)
            save_executors(executors)
            save_requests(requests)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()