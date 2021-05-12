from django.shortcuts import render
from recipes.models import Recipe

# Create your views here.

DEFAULT_TAGS_FILTER = {'breakfast': True, 'lunch': True, 'dinner': True}


def get_tags_filter(request):
    change_tag = request.GET.get('change_filter')
    current_tags = request.session.get('tags', DEFAULT_TAGS_FILTER)
    current_tags = DEFAULT_TAGS_FILTER

    if change_tag:
        if current_tags[change_tag]:
            current_tags[change_tag] = False
        else:
            current_tags[change_tag] = True

    request.session['tags'] = current_tags

    return current_tags


def home_page(request):

    current_tags = get_tags_filter(request)
    condition = [tag for tag, status in current_tags.items() if status]

    recipes = Recipe.objects.all()

    return render(
         request,
         'index.html',
         {'tags': current_tags, 'recipes': recipes}
     )
