from django.shortcuts import render
from django.http import HttpResponse

def page(title: str, content: str) -> str:
    """Единый каркас HTML-страницы с подключением Bootstrap."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav bg-light p-3 mb-4 shadow-sm">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/tenants/">Жильцы</a>
        <a class="nav-link" href="/executors/">Исполнители</a>
        <a class="nav-link" href="/requests/">Заявки</a>
    </nav>
    <main class="container">
        {content}
    </main>
</body>
</html>"""

def index(request):
    content = """
    <div class="text-center mt-5">
        <h1 class="display-4">Система управления заявками</h1>
        <hr class="my-4">
        <a href="/requests/" class="btn btn-primary btn-lg me-2">Список заявок</a>
        <a href="/tenants/" class="btn btn-secondary btn-lg">Жильцы</a>
        <a href="/executors/" class="btn btn-success btn-lg">Исполнители</a>
    </div>
    """
    return HttpResponse(page("Главная", content))

def page_not_found(request, exception):
    """Обработчик ошибки 404."""
    content = """
    <div class="text-center mt-5">
        <h1 class="text-danger display-4">404</h1>
        <p class="lead">Страница не найдена.</p>
        <a href="/" class="btn btn-primary">На главную</a>
    </div>
    """
    return HttpResponse(page("404 - Не найдено", content), status=404)