from django.shortcuts import render, redirect
from recipes.models import IngredientRecipeMap, Recipe
from django.views import generic
from django.urls import reverse_lazy
import pdfkit
from django.template.loader import render_to_string, get_template
from django.http import HttpResponse
import os
from django.conf import settings


class ShoppingListView(generic.TemplateView):

    template_name = 'shopping_list/shopping_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shopping_list = self.request.session.get('shopping_list', default=[])
        self.recipes = Recipe.objects.filter(id__in=shopping_list)
        self.request.session['shopping_list'] = shopping_list
        context['recipes'] = self.recipes
        return context


class EmptyShoppingList(generic.TemplateView):
    template_name = 'shopping_list/empty.html'


class DownloadShoppingList(generic.View):

    filename = 'required_ingredients.pdf'
    redirect_url = reverse_lazy('shopping_list:empty')
    template_name = 'shopping_list/download_list.html'
    context_name = 'ingredients'

    print(reverse_lazy)

    def collect_ingredients(self, shopping_list):
        ingredients = IngredientRecipeMap.objects.filter(
            recipe_id__in=shopping_list).values_list(
                'ingredient__name', 'quantity', 'ingredient__units')

        required_ingredients = {}
        for item in ingredients:
            name, quantity, units = item
            key = f'{name} ({units}.)'
            required_ingredients.setdefault(key, 0)
            required_ingredients[key] += quantity

        return required_ingredients

    def generate_pdf(self, data):
        html = render_to_string(self.template_name,
                                {self.context_name: data})

        options = {'enable-local-file-access': None}

        pdf = pdfkit.from_string(html, False, options)

        return pdf

    def get(self, request):
        shopping_list = request.session.get('shopping_list', default=[])
        if not shopping_list:
            return redirect(self.redirect_url)

        required_ingredients = self.collect_ingredients(shopping_list)
        pdf = self.generate_pdf(required_ingredients)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = (f'attachment; '
                                           f'filename="{self.filename}"')
        return response


def download(request):
    shopping_list = request.session.get('shopping_list', default=[])
    if not shopping_list:
        return ('В списке покупок нет ни одного рецепта')

    ingredients = IngredientRecipeMap.objects.filter(
        recipe_id__in=shopping_list).values_list(
            'ingredient__name', 'quantity', 'ingredient__units')

    required_ingredients = {}
    for item in ingredients:
        name, quantity, units = item
        key = f'{name} ({units}.)'
        required_ingredients.setdefault(key, 0)
        required_ingredients[key] += quantity

    html = render_to_string('shopping_list/download_list.html',
                            {'ingredients': required_ingredients})

    options = {
        'enable-local-file-access': None
    }

    pdf = pdfkit.from_string(html, False, options)

    filename = "required_ingredients.pdf"

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    return response
