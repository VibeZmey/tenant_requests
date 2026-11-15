from django import template

from requests.models import RequestStatus

register = template.Library()
STATUS_LABELS = dict(RequestStatus.choices)


@register.filter
def status_label(value):
    return STATUS_LABELS.get(value, value)
