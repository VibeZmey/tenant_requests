from django.core.paginator import Paginator
from django.db.models import Count, Max, Min, Q
from django.shortcuts import get_object_or_404, render

from executors.models import Executor

from .forms import SORT_OPTIONS, RequestFilters
from .models import ACTIVE_STATUSES, Request, request_rows


def request_list(request):
    form = RequestFilters(request.GET)
    form.is_valid()
    data = form.cleaned_data
    filters = {
        field: data[field] for field in ("category", "status", "date")
        if data.get(field)
    }
    for field in ("tenant", "executor"):
        if data.get(field):
            filters[f"{field}_id"] = data[field]
    ordering = SORT_OPTIONS.get(data.get("sort"), SORT_OPTIONS["newest"])
    queryset = Request.objects.filter(**filters)
    if data.get("tenant_name"):
        queryset = queryset.filter(tenant__name__icontains=data["tenant_name"])
    if data.get("q"):
        query = data["q"]
        queryset = queryset.filter(Q(problem__icontains=query) | Q(tenant__name__icontains=query))
    requests = request_rows(queryset.order_by(*ordering))
    page = Paginator(requests, 10).get_page(request.GET.get("page"))
    return render(request, "requests/request_list.html", {
        "requests": page, "page_obj": page, "form": form,
    })


def request_detail(request, request_id):
    req = get_object_or_404(Request.objects.select_related("tenant", "executor"), pk=request_id)
    return render(request, "requests/request_detail.html", {"req": req})


def statistics(request):
    try:
        minimum = max(0, min(int(request.GET.get("minimum", 0)), 1000000))
    except ValueError:
        minimum = 0
    totals = Request.objects.aggregate(
        total=Count("pk"), done=Count("pk", filter=Q(status="Выполнена")),
        unassigned=Count("pk", filter=Q(executor__isnull=True)),
    )
    staff = Executor.objects.aggregate(
        total=Count("pk"), busy=Count("pk", filter=Q(is_busy=True)),
        free=Count("pk", filter=Q(is_busy=False)),
    )
    categories = Request.objects.values("category").annotate(
        total=Count("pk"), first_date=Min("date"), last_date=Max("date"),
    ).order_by("-total", "category")
    workload = Executor.objects.annotate(
        total=Count("requests"),
        active=Count("requests", filter=Q(requests__status__in=ACTIVE_STATUSES)),
    ).filter(total__gte=minimum).order_by("-total", "pk")
    return render(request, "requests/statistics.html", {
        "totals": totals, "staff": staff, "categories": categories,
        "workload": workload, "minimum": minimum,
    })
