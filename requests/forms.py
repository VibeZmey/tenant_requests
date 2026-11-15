from django import forms

from .models import LEGACY_STATUS_CODES, RequestStatus

SORT_OPTIONS = {
    "newest": ("-date", "-pk"),
    "oldest": ("date", "pk"),
    "tenant": ("tenant__name", "pk"),
}


class RequestFilters(forms.Form):
    category = forms.CharField(label="Категория", required=False)
    q = forms.CharField(label="Проблема или имя жильца", required=False)
    tenant_name = forms.CharField(label="Имя жильца", required=False)
    status = forms.ChoiceField(
        label="Статус", required=False, choices=[("", "Все статусы"), *RequestStatus.choices],
    )
    date = forms.DateField(
        label="Дата", required=False, input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    tenant = forms.IntegerField(
        label="ID жильца", required=False, min_value=1, max_value=2**63 - 1,
    )
    executor = forms.IntegerField(
        label="ID исполнителя", required=False, min_value=1, max_value=2**63 - 1,
    )
    sort = forms.ChoiceField(label="Сортировка", required=False, choices=[
        ("newest", "Сначала новые"), ("oldest", "Сначала старые"), ("tenant", "По жильцу"),
    ])

    def __init__(self, data=None, **kwargs):
        if data is not None and data.get("status") in LEGACY_STATUS_CODES:
            data = data.copy()
            data["status"] = LEGACY_STATUS_CODES[data["status"]]
        super().__init__(data, **kwargs)
