from django import template
from django.db.models import DateTimeField

register = template.Library()

@register.filter
def get_field_value(animal, verbose_name):
    model = animal._meta.model
    for field in model._meta.fields:
        if field.verbose_name == verbose_name:
            value = getattr(animal, field.name)
            if value is not None and value != '':
                if isinstance(field, DateTimeField):
                    return value.strftime('%d/%m/%Y às %H:%M')
                if isinstance(value, bool):
                    return 'Ativo' if value else 'Inativo'
                return value
            else:
                return '-'
    return '-'
