from django import template

register = template.Library()


@register.filter(name='required_field')
def required_field(field, mark='*'):
    """If the field is required, return the markup"""
    if field.field.required:
        return '<span class="required_field">' + mark + '</span>'
    else:
        return ''
