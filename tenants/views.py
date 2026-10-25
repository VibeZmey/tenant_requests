from django.shortcuts import render
from db.database import fetch


def tenant_list(request):
    q = request.GET.get("q", "").strip()
    try:
        page = max(1, min(int(request.GET.get("page", 1)), 1000000))
    except ValueError:
        page = 1
    tenants = (fetch("tenant_search", ("%" + q + "%", q)) if q
               else fetch("tenants", (20, (page - 1) * 20)))
    return render(request, "tenants/tenant_list.html", {
        "tenants": tenants, "q": q, "page": page,
        "next_page": page + 1, "previous_page": max(1, page - 1),
    })


def tenant_detail(request, tenant_id):
    tenant = fetch("tenant_detail", (tenant_id,), one=True)
    return render(request, "tenants/tenant_detail.html", {
        "tenant": tenant, "requests": fetch("tenant_requests", (tenant_id,)),
    }, status=200 if tenant else 404)
