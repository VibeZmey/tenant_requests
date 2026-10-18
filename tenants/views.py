from django.shortcuts import render
from storage import load_tenants
from models.tenants import find_tenant_by_id

def tenant_list(request):
    tenants = load_tenants("tenants.json")
    return render(request, "tenants/tenant_list.html", {"tenants": tenants})

def tenant_detail(request, tenant_id: int):
    tenants = load_tenants("tenants.json")
    tenant = find_tenant_by_id(tenants, tenant_id)
    return render(
        request,
        "tenants/tenant_detail.html",
        {"tenant": tenant},
        status=404 if tenant is None else 200
    )