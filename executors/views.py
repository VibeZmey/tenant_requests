from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404, render

from requests.models import ACTIVE_STATUSES, Request, request_rows

from .models import Executor


def executor_list(request):
    specialization = request.GET.get("specialization", "").strip()
    available = request.GET.get("available") == "1"
    executors = Executor.objects.all()
    if available:
        active = Request.objects.filter(executor_id=OuterRef("pk"), status__in=ACTIVE_STATUSES)
        executors = executors.filter(is_busy=False).exclude(Exists(active))
        if specialization:
            executors = executors.filter(specialization=specialization)
    return render(request, "executors/executor_list.html", {
        "executors": executors, "specialization": specialization, "available": available,
    })


def executor_detail(request, executor_id):
    executor = get_object_or_404(Executor, pk=executor_id)
    return render(request, "executors/executor_detail.html", {
        "executor": executor, "requests": request_rows(executor.requests.all()),
    })
