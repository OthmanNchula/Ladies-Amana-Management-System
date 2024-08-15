from django import template

register = template.Library()

@register.filter
def range_filter(n):
    return range(n)
