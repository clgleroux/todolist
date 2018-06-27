import markdown

from django.utils.safestring import mark_safe

from django import template

register = template.Library()


@register.filter
def changemarkdown(value):
    return mark_safe(markdown.markdown(value))
