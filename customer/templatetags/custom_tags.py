from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='starts_with_plus260')
@stringfilter
def starts_with_plus260(value):
    return value.startswith('+260')
