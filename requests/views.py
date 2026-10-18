from django.shortcuts import render
from django.http import HttpResponse
from homepage.views import page
from storage import load_requests, load_tenants, load_executors
from models.requests import find_request_by_id


def request_list(request):
    """Список заявок из JSON."""
    tenants = load_tenants("tenants.json")
    executors = load_executors("executors.json")
    requests = load_requests(tenants, executors, "requests.json")

    items = ""
    for req in requests:
        badge = "bg-success" if req.status == "Выполнена" else "bg-primary"
        if req.status == "Отменена":
            badge = "bg-secondary"

        text = f"Заявка №{req.id} (Кв. {req.tenant.flat}) - {req.problem}"
        items += f"""
        <li class="list-group-item d-flex justify-content-between align-items-center">
            <a href="/requests/{req.id}/">{text}</a>
            <span class="badge {badge}">{req.status}</span>
        </li>
        """

    content = f"""
    <h1>Заявки жильцов</h1>
    <ul class="list-group mt-3">{items}</ul>
    """
    return HttpResponse(page("Список заявок", content))


def request_detail(request, request_id: int):
    """Карточка конкретной заявки."""
    tenants = load_tenants("tenants.json")
    executors = load_executors("executors.json")
    requests = load_requests(tenants, executors, "requests.json")

    req = find_request_by_id(requests, request_id)

    if req is None:
        content = """
        <h1 class="text-danger">Заявка не найдена</h1>
        <a href="/requests/" class="btn btn-outline-secondary">← Назад</a>
        """
        return HttpResponse(page("Не найдено", content), status=404)

    executor_name = req.executor.name if req.executor else "Не назначен"

    content = f"""
    <div class="card mt-4">
        <div class="card-body">
            <h5 class="card-title">Заявка №{req.id}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{req.date.isoformat()}</h6>
            <p class="card-text"><strong>Проблема:</strong> {req.problem}</p>
            <p class="card-text"><strong>Категория:</strong> {req.category}</p>
            <p class="card-text"><strong>Жилец:</strong> {req.tenant.name} (кв. {req.tenant.flat})</p>
            <p class="card-text"><strong>Исполнитель:</strong> {executor_name}</p>
            <p class="card-text"><strong>Статус:</strong> {req.status}</p>
            <a href="/requests/" class="btn btn-outline-secondary">← К списку</a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Заявка №{req.id}", content))