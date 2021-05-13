from django.shortcuts import render
from recipes.models import Recipe
from django.db.models import Q
import operator
from functools import reduce


# Create your views here.


def generate_conditions(tags):

    conditions = [
        Q(tags__icontains=item.value) for item in Recipe.Tag
        if item.name.lower() in tags
    ]

    return reduce(operator.or_, conditions)


def get_tags_filter(request):
    change_tag = request.GET.get('change_filter')
    current_tags = request.session.get(
        'tags', default=[item.name.lower() for item in Recipe.Tag])

    if change_tag:
        if change_tag in current_tags:
            current_tags.remove(change_tag)
        else:
            current_tags.append(change_tag)

    request.session['tags'] = current_tags

    return current_tags


def home_page(request):

    recipes = Recipe.objects.none()

    current_tags = get_tags_filter(request)

    if current_tags:
        condition = generate_conditions(current_tags)
        recipes = Recipe.objects.filter(condition)

    return render(
         request,
         'index.html',
         {'tags': current_tags, 'recipes': recipes}
     )
