from django import template

register = template.Library()


@register.filter
def form_input(field):
    return field.as_widget(attrs={'class': 'form__input'})
