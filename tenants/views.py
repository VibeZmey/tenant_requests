from django.shortcuts import render
from django.http import HttpResponse
from homepage.views import page
from storage import load_tenants
from models.tenants import find_tenant_by_id


def tenant_list(request):
    """Список всех жильцов из JSON."""
    tenants = load_tenants("tenants.json")

    items = ""
    for tenant in tenants:
        text = f"{tenant.name} - кв. {tenant.flat}"
        items += f'<li class="list-group-item"><a href="/tenants/{tenant.id}/">{text}</a></li>'

    content = f"""
    <h1>Жильцы</h1>
    <ul class="list-group mt-3">{items}</ul>
    """
    return HttpResponse(page("Список жильцов", content))


def tenant_detail(request, tenant_id: int):
    """Карточка конкретного жильца."""
    tenants = load_tenants("tenants.json")
    tenant = find_tenant_by_id(tenants, tenant_id)

    if tenant is None:
        content = """
        <h1 class="text-danger">Жилец не найден</h1>
        <a href="/tenants/" class="btn btn-outline-secondary">← Назад</a>
        """
        return HttpResponse(page("Не найден", content), status=404)

    content = f"""
    <div class="card mt-4" style="max-width: 400px;">
        <div class="card-body">
            <h5 class="card-title">{tenant.name}</h5>
            <p class="card-text"><strong>ID:</strong> {tenant.id}</p>
            <p class="card-text"><strong>Квартира:</strong> {tenant.flat}</p>
            <p class="card-text"><strong>Телефон:</strong> {tenant.phone}</p>
            <a href="/tenants/" class="btn btn-outline-secondary">← К списку</a>
        </div>
    </div>
    """
    return HttpResponse(page(tenant.name, content))