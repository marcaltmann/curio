from datetime import timedelta

from django import template

register = template.Library()


@register.filter
def duration(value):
    if not isinstance(value, timedelta):
        return value
    return str(timedelta(seconds=int(value.total_seconds())))
