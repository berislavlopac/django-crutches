import re
from django import template

register = template.Library()

CLASS_PATTERN = re.compile(r'\bclass="[\w\d]*"')

@register.filter
def extract(h, key):
    try:
        return h[key]
    except Exception:
        return False

@register.filter(name='cssclass')
def cssclass(value, arg):
    """
    Replace the attribute css class for Field 'value' with 'arg'.
    """
    attrs = value.field.widget.attrs
    orig = attrs['class'] if 'class' in attrs else None

    attrs['class'] = arg
    rendered = str(value)

    if orig:
        attrs['class']
    else:
        del attrs['class']

    return rendered

@register.filter
# truncate after a certain number of characters
def truncchar(value, arg):
    if len(value) < arg:
        return value
    else:
        return value[:arg] + '...'

@register.filter
# reverse a list
def reverse(list):
    try:
        return reversed(list)
    except Exception:
        return list
