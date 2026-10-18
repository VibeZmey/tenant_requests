
"""Сущность «Заявка» и правила её обработки."""
from datetime import date
from typing import List, Optional

from .tenants import Tenant
from .executors import Executor

# Тип проблемы категория
PROBLEM_CATEGORIES = {
    "электрика": ["нет света", "электричество", "проводка", "розетка"],
    "сантехника": ["вода", "кран", "труба", "унитаз", "протечка"],
    "уборка": ["мусор", "грязь", "уборка"],
    "отопление": ["батарея", "отопление", "холодно"],
}


def determine_category(problem: str) -> str:
    """Определить категорию проблемы по её описанию."""
    text = problem.lower()
    for category, keywords in PROBLEM_CATEGORIES.items():
        if any(word in text for word in keywords):
            return category
    return "прочее"


class Request:
    """Заявка жильца на устранение проблемы."""

    STATUS_NEW = "Новая"
    STATUS_IN_PROGRESS = "В работе"
    STATUS_DONE = "Выполнена"
    STATUS_CANCELLED = "Отменена"

    def __init__(
        self,
        request_id: int,
        tenant: Tenant,
        problem: str,
        req_date: date,
        category: Optional[str] = None,
        status: str = STATUS_NEW,
        executor: Optional[Executor] = None,
    ) -> None:
        self.id = request_id
        self.tenant = tenant
        self.problem = problem
        self.date = req_date
        self.category = category or determine_category(problem)
        self.status = status
        self.executor = executor

    # поведение объекта

    def cancel(self) -> None:
        """Отменить заявку."""
        self.status = self.STATUS_CANCELLED
        if self.executor is not None:
            self.executor.is_busy = False

    def assign_executor(self, executor: Executor) -> bool:
        """Назначить исполнителя. Возвращает успех операции."""
        if self.status != self.STATUS_NEW:
            return False
        if executor.is_busy:
            return False
        self.executor = executor
        executor.is_busy = True
        self.status = self.STATUS_IN_PROGRESS
        return True

    def complete(self) -> None:
        """Завершить заявку."""
        self.status = self.STATUS_DONE
        if self.executor is not None:
            self.executor.is_busy = False

    def get_status_text(self) -> str:
        """Расшифровка статуса для пользователя."""
        return {
            self.STATUS_NEW: "Заявка принята в работу",
            self.STATUS_IN_PROGRESS: "Техник выехал",
            self.STATUS_DONE: "Проблема устранена",
            self.STATUS_CANCELLED: "Заявка отменена",
        }.get(self.status, "Неизвестный статус")

    def __str__(self) -> str:
        executor_text = (
            f", исполнитель: {self.executor.name}"
            if self.executor else ""
        )
        return (
            f"Заявка №{self.id} | Кв. {self.tenant.flat} | "
            f"{self.tenant.name} | {self.problem} "
            f"[{self.category}] | {self.date.isoformat()} | "
            f"Статус: {self.status}{executor_text}"
        )

    # преобразования

    @classmethod
    def from_data(
        cls,
        data: dict,
        tenants: List[Tenant],
        executors: List[Executor],
    ) -> Optional["Request"]:
        """Создать объект Request из JSON, восстановив связи."""
        tenant = next(
            (t for t in tenants if t.id == data["tenant_id"]), None
        )
        if tenant is None:
            return None

        executor = None
        if data.get("executor_id") is not None:
            executor = next(
                (e for e in executors if e.id == data["executor_id"]),
                None,
            )

        return cls(
            request_id=data["id"],
            tenant=tenant,
            problem=data["problem"],
            req_date=date.fromisoformat(data["date"]),
            category=data.get("category"),
            status=data.get("status", cls.STATUS_NEW),
            executor=executor,
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "tenant_id": self.tenant.id,
            "problem": self.problem,
            "date": self.date.isoformat(),
            "category": self.category,
            "status": self.status,
            "executor_id": self.executor.id if self.executor else None,
        }


# функции работы с коллекцией заявок

def create_request(
    requests: List[Request],
    tenant: Tenant,
    problem: str,
    req_date: date,
) -> Request:
    """Создать новую заявку и добавить её в коллекцию."""
    new_id = max((r.id for r in requests), default=0) + 1
    request = Request(new_id, tenant, problem, req_date)
    requests.append(request)
    return request


def find_requests_by_flat(
    requests: List[Request], flat: int
) -> List[Request]:
    """Найти все заявки по номеру квартиры."""
    return [r for r in requests if r.tenant.flat == flat]


def find_requests_by_category(
    requests: List[Request], category: str
) -> List[Request]:
    """Найти заявки по категории."""
    return [r for r in requests if r.category == category]


def show_requests(requests: List[Request]) -> None:
    """Вывести все заявки."""
    if not requests:
        print("Список заявок пуст.")
        return
    for request in requests:
        print(request)

def find_request_by_id(requests: List[Request], request_id: int) -> Optional[Request]:
    """Найти заявку по идентификатору (добавлено для ПР5)."""
    for req in requests:
        if req.id == request_id:
            return req
    return None