# myapp/templatetags/custom_filters.py
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.translation import gettext as _

register = template.Library()

@register.filter
def currency(value):
    try:
        value = float(value)
        formatted_value = intcomma(value)
        return formatted_value.replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return value

@register.filter
def naturaltime_es(value):
    """
    Translates the output of naturaltime to Spanish.
    """
    try:
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return _(naturaltime(value))
    except ImportError:
        return value