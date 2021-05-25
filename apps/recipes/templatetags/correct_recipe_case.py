from django import template

register = template.Library()


@register.filter
def recipe_case(number):

    floor, remainder = divmod(number, 10)
    if remainder == 1 and floor != 1:
        word = 'рецепт'
    elif 1 < remainder <= 4 and floor != 1:
        word = 'рецепта'
    else:
        word = 'рецептов'

    return f'{number} {word}'
