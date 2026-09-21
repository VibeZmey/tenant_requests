from request_manager import create_request, find_requests_by_flat
from datetime import date


def test_create_request():
    """Проверка создания заявки."""
    requests_list = []
    req = create_request(requests_list, "Иванов И.И.", 101, "Нет света", date(2026, 9, 20))

    assert len(requests_list) == 1
    assert req["tenant"] == "Иванов И.И."
    assert req["flat"] == 101
    assert req["status"] == "Новая"


def test_find_by_flat():
    """Проверка поиска заявок."""
    requests_list = [
        {"id": 1, "flat": 101, "problem": "Тест1"},
        {"id": 2, "flat": 102, "problem": "Тест2"}
    ]

    found = find_requests_by_flat(requests_list, 101)
    assert len(found) == 1
    assert found[0]["problem"] == "Тест1"