from django.shortcuts import render
from storage import load_requests, load_tenants, load_executors
from models.requests import find_request_by_id


def request_list(request):
    tenants = load_tenants("tenants.json")
    executors = load_executors("executors.json")
    requests_list = load_requests(tenants, executors, "requests.json")
    return render(request, "requests/request_list.html", {"requests": requests_list})


def request_detail(request, request_id: int):
    tenants = load_tenants("tenants.json")
    executors = load_executors("executors.json")
    requests_list = load_requests(tenants, executors, "requests.json")

    req = find_request_by_id(requests_list, request_id)
    return render(
        request,
        "requests/request_detail.html",
        {"req": req},
        status=404 if req is None else 200
    )