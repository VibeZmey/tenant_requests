from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404, render

from requests.models import Request, request_rows

from .forms import AvailabilityFilters
from .models import Executor


def executor_list(request):
    params = request.GET.copy()
    if params.get("available") != "1":
        params.pop("available", None)
    form = AvailabilityFilters(params)
    form.is_valid()
    data = form.cleaned_data
    executors = Executor.objects.all()
    if data.get("available"):
        active = Request.objects.active().filter(executor_id=OuterRef("pk"))
        if data.get("date"):
            active = active.for_date(data["date"])
        executors = executors.filter(is_busy=False).exclude(Exists(active))
        if data.get("specialization"):
            executors = executors.filter(specialization=data["specialization"])
    return render(request, "executors/executor_list.html", {
        "executors": executors, "form": form,
    })


def executor_detail(request, executor_id=None, slug=None):
    lookup = {"pk": executor_id} if executor_id is not None else {"slug": slug}
    executor = get_object_or_404(Executor, **lookup)
    return render(request, "executors/executor_detail.html", {
        "executor": executor, "requests": request_rows(executor.requests.all()),
    })
