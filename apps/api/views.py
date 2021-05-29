from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from recipes.models import Favorite, Ingredient, Subscribe
from rest_framework import filters, mixins, permissions, viewsets, status
from django.contrib.auth import get_user_model

from api.serializers import IngredientSerializer
from shopping_list.views import PurchaseMixin

User = get_user_model()


success_response = JsonResponse({'success': 'true'})
fail_response = JsonResponse({'success': 'false'},
                             status=status.HTTP_400_BAD_REQUEST)


class ViewSetWithPermissions(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]


class FavoriteViewSet(ViewSetWithPermissions):

    def create(self, request):
        recipe_id = request.data.get('id')
        _, created = Favorite.objects.get_or_create(chooser=request.user,
                                                    recipe_id=recipe_id)
        if created:
            return success_response
        return fail_response

    def destroy(self, request, pk=None):
        favorite = Favorite.objects.filter(chooser=request.user,
                                           recipe_id=pk)
        favorite.delete()
        return success_response


class SubscribeViewSet(ViewSetWithPermissions):

    def create(self, request):
        author_id = request.data.get('id')
        author = get_object_or_404(User, id=author_id)
        if author == request.user:
            return fail_response

        _, created = Subscribe.objects.get_or_create(subscriber=request.user,
                                                     author=author)
        if created:
            return success_response
        return fail_response

    def destroy(self, request, pk=None):
        subscribe = Subscribe.objects.filter(subscriber=request.user,
                                             author_id=pk)
        subscribe.delete()
        return success_response


class IngredientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class PurchaseViewSet(PurchaseMixin, viewsets.ViewSet):

    def create(self, request):
        assert 'id' in request.data, 'В запросе не указан id рецепта'
        recipe_id = int(request.data.get('id'))
        shopping_list = self.get_shopping_list(request)
        if recipe_id in shopping_list:
            return fail_response
        shopping_list.append(recipe_id)
        self.update_shopping_list(request, shopping_list)
        return success_response

    def destroy(self, request, pk=None):
        pk = int(pk)
        shopping_list = self.get_shopping_list(request)

        if pk not in shopping_list:
            return fail_response

        shopping_list.remove(pk)
        self.update_shopping_list(request, shopping_list)
        return success_response
