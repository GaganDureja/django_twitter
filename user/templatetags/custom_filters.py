from django import template

register = template.Library()

@register.filter(name='short_number')
def short_number(value):
    """
    Convert a large number to a short format like 5K, 1M, etc.
    """
    value = int(value)
    if value >= 1000000:
        return f"{value // 1000000}M"
    elif value >= 1000:
        return f"{value // 1000}K"
    else:
        return str(value)
