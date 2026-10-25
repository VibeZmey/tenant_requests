from django.shortcuts import render
from db.database import fetch


def request_list(request):
    category = request.GET.get("category", "").strip()
    status = request.GET.get("status", "").strip()
    return render(request, "requests/request_list.html", {
        "requests": fetch("requests", (category, category, status, status)),
        "category": category, "status": status,
    })


def request_detail(request, request_id):
    req = fetch("request_detail", (request_id,), one=True)
    return render(request, "requests/request_detail.html", {
        "req": req,
    }, status=200 if req else 404)


def statistics(request):
    try:
        minimum = max(0, min(int(request.GET.get("minimum", 0)), 1000000))
    except ValueError:
        minimum = 0
    return render(request, "requests/statistics.html", {
        "totals": fetch("request_totals", one=True),
        "staff": fetch("executor_totals", one=True),
        "categories": fetch("category_stats"),
        "workload": fetch("executor_stats", (minimum,)), "minimum": minimum,
    })
