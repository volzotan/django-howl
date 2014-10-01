from django import template

register = template.Library()

@register.filter
def div(x,y):
    return int(x)/int(y)