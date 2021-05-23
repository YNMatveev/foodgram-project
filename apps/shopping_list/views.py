from django.shortcuts import render
from recipes.models import Favorite, Recipe, Subscribe
from django.views import generic
from django.urls import reverse_lazy


class ShoppingListView(generic.TemplateView):

    template_name = 'shopping_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shopping_list = self.request.session.get('shopping_list', default=[])
        self.recipes = Recipe.objects.filter(id__in=shopping_list)
        self.request.session['shopping_list'] = shopping_list
        context['recipes'] = self.recipes
        return context
