from datetime import date
from typing import List, Dict, Optional

RequestType = Dict[str, any]

def create_request(requests: List[RequestType], tenant_name: str, flat_number: int, problem_desc: str, req_date: date) -> RequestType:
    """Создает новую заявку и добавляет её в список."""
    new_id = len(requests) + 1
    new_request = {
        "id": new_id,
        "tenant": tenant_name,
        "flat": flat_number,
        "problem": problem_desc,
        "date": req_date.isoformat(),
        "status": "Новая"
    }
    requests.append(new_request)
    return new_request

def find_requests_by_flat(requests: List[RequestType], flat_number: int) -> List[RequestType]:
    """Поиск всех заявок для конкретной квартиры."""
    return [req for req in requests if req["flat"] == flat_number]

def get_status_text(status: str) -> str:
    statuses = {
        "Новая": "Заявка принята в работу",
        "В работе": "Техник выехал",
        "Выполнена": "Проблема устранена"
    }
    return statuses.get(status, "Неизвестный статус")