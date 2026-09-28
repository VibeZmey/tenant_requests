from datetime import date

from models import Request, Tenant, Executor
from models.requests import (
    create_request,
    find_requests_by_flat,
    find_requests_by_category,
    determine_category,
)


def test_create_request():
    tenant = Tenant(1, "Иванов И.И.", 101)
    requests = []
    request = create_request(requests, tenant, "Нет света", date(2026, 9, 20))

    assert len(requests) == 1
    assert request.tenant is tenant
    assert request.problem == "Нет света"
    assert request.status == Request.STATUS_NEW
    assert request.category == "электрика"


def test_find_by_flat():
    tenants = [
        Tenant(1, "Иванов И.И.", 101),
        Tenant(2, "Петров П.П.", 102),
    ]
    requests = [
        Request(1, tenants[0], "Тест1", date(2026, 9, 20)),
        Request(2, tenants[1], "Тест2", date(2026, 9, 21)),
    ]
    found = find_requests_by_flat(requests, 101)
    assert len(found) == 1
    assert found[0].problem == "Тест1"


def test_assign_executor():
    tenant = Tenant(1, "Иванов И.И.", 101)
    executor = Executor(1, "Петров П.П.", "электрика")
    request = Request(1, tenant, "Нет света", date(2026, 9, 20))

    assert request.assign_executor(executor)
    assert request.executor is executor
    assert executor.is_busy
    assert request.status == Request.STATUS_IN_PROGRESS


def test_cancel_request():
    tenant = Tenant(1, "Иванов И.И.", 101)
    executor = Executor(1, "Петров П.П.", "электрика")
    request = Request(1, tenant, "Нет света", date(2026, 9, 20))
    request.assign_executor(executor)

    request.cancel()
    assert request.status == Request.STATUS_CANCELLED
    assert not executor.is_busy


def test_determine_category():
    assert determine_category("нет электричества") == "электрика"
    assert determine_category("протекает кран") == "сантехника"
    assert determine_category("что-то непонятное") == "прочее"


def test_find_by_category():
    tenant = Tenant(1, "Иванов И.И.", 101)
    requests = [
        Request(1, tenant, "Нет света", date(2026, 9, 20)),
        Request(2, tenant, "Протечка воды", date(2026, 9, 21)),
    ]
    found = find_requests_by_category(requests, "электрика")
    assert len(found) == 1