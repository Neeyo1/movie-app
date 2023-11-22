from django import template

register = template.Library()

@register.filter(name='zip')
def zip_lists(a, b):
    return zip(a, b)

@register.filter(name='range')
def filter_range(start, end):
    return range(start, end)