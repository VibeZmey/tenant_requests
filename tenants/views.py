from django.db.models import CharField, Q
from django.db.models.functions import Cast
from django.shortcuts import get_object_or_404, render

from requests.models import request_rows

from .models import Tenant


def tenant_list(request):
    q = request.GET.get("q", "").strip()
    try:
        page = max(1, min(int(request.GET.get("page", 1)), 1000000))
    except ValueError:
        page = 1
    tenants = Tenant.objects.all()
    if q:
        tenants = tenants.alias(flat_text=Cast("flat", CharField())).filter(
            Q(name__icontains=q) | Q(flat_text=q)
        )
    else:
        tenants = tenants[(page - 1) * 20:page * 20]
    return render(request, "tenants/tenant_list.html", {
        "tenants": tenants, "q": q, "page": page,
        "next_page": page + 1, "previous_page": max(1, page - 1),
    })


def tenant_detail(request, tenant_id):
    tenant = get_object_or_404(Tenant, pk=tenant_id)
    return render(request, "tenants/tenant_detail.html", {
        "tenant": tenant, "requests": request_rows(tenant.requests.all()),
    })
