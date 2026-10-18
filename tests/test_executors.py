from models import Executor
from models.executors import add_executor, find_free_executor


def test_executor_creation():
    executor = Executor(1, "Петров П.П.", "электрика")
    assert executor.id == 1
    assert executor.specialization == "электрика"
    assert not executor.is_busy


def test_can_handle():
    executor = Executor(1, "Петров П.П.", "электрика")
    assert executor.can_handle("электрика")
    assert not executor.can_handle("сантехника")


def test_find_free_executor():
    executors = [
        Executor(1, "Петров П.П.", "электрика"),
        Executor(2, "Сидоров С.С.", "сантехника", is_busy=True),
    ]
    found = find_free_executor(executors, "электрика")
    assert found is not None
    assert found.id == 1


def test_add_executor():
    executors = []
    executor = add_executor(executors, "Сидоров С.С.", "сантехника")
    assert len(executors) == 1
    assert executor.id == 1
