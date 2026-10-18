from django.shortcuts import render
from storage import load_executors
from models.executors import find_executor_by_id

def executor_list(request):
    executors = load_executors("executors.json")
    return render(request, "executors/executor_list.html", {"executors": executors})

def executor_detail(request, executor_id: int):
    executors = load_executors("executors.json")
    executor = find_executor_by_id(executors, executor_id)
    return render(
        request,
        "executors/executor_detail.html",
        {"executor": executor},
        status=404 if executor is None else 200
    )