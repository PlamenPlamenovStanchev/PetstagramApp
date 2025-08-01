from django import template

register = template.Library()

@register.filter
def placeholder(value, text_to_display):
    value.field.widget.attrs['placeholder'] = text_to_display
    return value