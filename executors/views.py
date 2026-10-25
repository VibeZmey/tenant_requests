from django.shortcuts import render
from db.database import fetch


def executor_list(request):
    specialization = request.GET.get("specialization", "").strip()
    available = request.GET.get("available") == "1"
    executors = (fetch("available_executors", (specialization, specialization))
                 if available else fetch("executors"))
    return render(request, "executors/executor_list.html", {
        "executors": executors, "specialization": specialization, "available": available,
    })


def executor_detail(request, executor_id):
    executor = fetch("executor_detail", (executor_id,), one=True)
    return render(request, "executors/executor_detail.html", {
        "executor": executor,
    }, status=200 if executor else 404)
