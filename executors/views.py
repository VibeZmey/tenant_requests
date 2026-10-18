from django.shortcuts import render
from django.http import HttpResponse
from homepage.views import page
from storage import load_executors
from models.executors import find_executor_by_id


def executor_list(request):
    """Список всех исполнителей из JSON."""
    executors = load_executors("executors.json")

    items = ""
    for executor in executors:
        status = "Занят" if executor.is_busy else "Свободен"
        badge = "bg-danger" if executor.is_busy else "bg-success"

        text = f"{executor.name} — {executor.specialization}"
        items += f"""
        <li class="list-group-item d-flex justify-content-between align-items-center">
            <a href="/executors/{executor.id}/">{text}</a>
            <span class="badge {badge}">{status}</span>
        </li>
        """

    content = f"""
    <h1>Исполнители</h1>
    <ul class="list-group mt-3">{items}</ul>
    """
    return HttpResponse(page("Список исполнителей", content))


def executor_detail(request, executor_id: int):
    """Карточка конкретного исполнителя."""
    executors = load_executors("executors.json")
    executor = find_executor_by_id(executors, executor_id)

    if executor is None:
        content = """
        <h1 class="text-danger">Исполнитель не найден</h1>
        <a href="/executors/" class="btn btn-outline-secondary">← Назад</a>
        """
        return HttpResponse(page("Не найден", content), status=404)

    status = "Занят" if executor.is_busy else "Свободен"
    badge = "bg-danger" if executor.is_busy else "bg-success"

    content = f"""
    <div class="card mt-4" style="max-width: 400px;">
        <div class="card-body">
            <h5 class="card-title">{executor.name}</h5>
            <p class="card-text"><strong>ID:</strong> {executor.id}</p>
            <p class="card-text"><strong>Специализация:</strong> {executor.specialization}</p>
            <p class="card-text">
                <strong>Статус:</strong> <span class="badge {badge}">{status}</span>
            </p>
            <a href="/executors/" class="btn btn-outline-secondary">← К списку</a>
        </div>
    </div>
    """
    return HttpResponse(page(executor.name, content))