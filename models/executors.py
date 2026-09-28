"""Сущность «Исполнитель»."""
from typing import List


class Executor:
    """Исполнитель - сотрудник, выполняющий заявки."""

    def __init__(
        self,
        executor_id: int,
        name: str,
        specialization: str,
        is_busy: bool = False,
    ) -> None:
        self.id = executor_id
        self.name = name
        self.specialization = specialization
        self.is_busy = is_busy

    @classmethod
    def from_data(cls, data: dict) -> "Executor":
        """Создать исполнителя из словаря JSON."""
        return cls(
            executor_id=data["id"],
            name=data["name"],
            specialization=data["specialization"],
            is_busy=data.get("is_busy", False),
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "specialization": self.specialization,
            "is_busy": self.is_busy,
        }

    def can_handle(self, problem_type: str) -> bool:
        """Проверить, может ли исполнитель взяться за тип проблемы."""
        return self.specialization.lower() == problem_type.lower()

    def __str__(self) -> str:
        status = "занят" if self.is_busy else "свободен"
        return (
            f"Исполнитель #{self.id}: {self.name} "
            f"[{self.specialization}] — {status}"
        )


# функции работы с коллекцией исполнителей

def add_executor(
    executors: List[Executor],
    name: str,
    specialization: str,
) -> Executor:
    """Создать исполнителя и добавить его в коллекцию."""
    new_id = max((e.id for e in executors), default=0) + 1
    executor = Executor(new_id, name, specialization)
    executors.append(executor)
    return executor


def find_executor_by_id(
    executors: List[Executor], executor_id: int
):
    """Найти исполнителя по идентификатору."""
    for executor in executors:
        if executor.id == executor_id:
            return executor
    return None


def find_free_executor(
    executors: List[Executor],
    problem_type: str,
):
    """Найти свободного исполнителя с подходящей специализацией."""
    for executor in executors:
        if not executor.is_busy and executor.can_handle(problem_type):
            return executor
    return None


def show_executors(executors: List[Executor]) -> None:
    """Вывести информацию обо всех исполнителях."""
    if not executors:
        print("Список исполнителей пуст.")
        return
    for executor in executors:
        print(executor)