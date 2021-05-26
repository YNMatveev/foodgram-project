import pdfkit
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from recipes.models import IngredientRecipeMap, Recipe
from shopping_list.models import Purchase


class PurchaseMixin():

    def get_shopping_list(self, request):
        if request.user.is_authenticated:
            obj, _ = Purchase.objects.get_or_create(user=request.user)
            return obj.shopping_list
        return request.session.get('shopping_list', default=[])

    def update_shopping_list(self, request, shopping_list):
        if request.user.is_authenticated:
            _ = Purchase.objects.update_or_create(
                user=request.user, defaults={'shopping_list': shopping_list})
        else:
            request.session['shopping_list'] = shopping_list


class ShoppingListView(PurchaseMixin, generic.TemplateView):

    template_name = 'shopping_list/shopping_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shopping_list = self.get_shopping_list(self.request)
        self.recipes = Recipe.objects.filter(id__in=shopping_list)
        context['recipes'] = self.recipes
        return context


class EmptyShoppingList(generic.TemplateView):
    template_name = 'shopping_list/empty.html'


class DownloadShoppingList(PurchaseMixin, generic.View):

    filename = 'required_ingredients.pdf'
    redirect_url = reverse_lazy('shopping_list:empty')
    template_name = 'shopping_list/download_list.html'
    context_name = 'ingredients'

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
        shopping_list = self.get_shopping_list(request)
        if not shopping_list:
            return redirect(self.redirect_url)

        required_ingredients = self.collect_ingredients(shopping_list)
        pdf = self.generate_pdf(required_ingredients)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = (f'attachment; '
                                           f'filename="{self.filename}"')
        return response
