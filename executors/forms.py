from django import forms


class AvailabilityFilters(forms.Form):
    specialization = forms.CharField(label="Специализация", required=False)
    available = forms.BooleanField(
        label="Только свободные", required=False, widget=forms.CheckboxInput(attrs={"value": "1"}),
    )
    date = forms.DateField(
        label="Дата заявки", required=False, input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"}),
    )
