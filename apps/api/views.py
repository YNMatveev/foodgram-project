from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from recipes.models import Favorite, Ingredient, Subscribe
from rest_framework import filters, mixins, permissions, viewsets, status
from django.contrib.auth import get_user_model

from api.serializers import IngredientSerializer

User = get_user_model()


SUCCESS_MESSAGE = {'success': 'true'}
FAIL_MESSAGE = {'success': 'false'}


class ViewSetWithPermissions(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]


class FavoriteViewSet(ViewSetWithPermissions):

    def create(self, request):
        recipe_id = request.data.get('id')
        _, created = Favorite.objects.get_or_create(chooser=request.user,
                                                    recipe_id=recipe_id)
        if created:
            return JsonResponse(SUCCESS_MESSAGE, status=status.HTTP_200_OK)
        return JsonResponse(FAIL_MESSAGE, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        favorite = Favorite.objects.filter(chooser=request.user,
                                           recipe_id=pk)
        favorite.delete()
        return JsonResponse(SUCCESS_MESSAGE, status=status.HTTP_200_OK)


class SubscribeViewSet(ViewSetWithPermissions):

    def create(self, request):
        author_id = request.data.get('id')
        author = get_object_or_404(User, id=author_id)
        if author == request.user:
            return JsonResponse(FAIL_MESSAGE,
                                status=status.HTTP_400_BAD_REQUEST)

        _, created = Subscribe.objects.get_or_create(subscriber=request.user,
                                                     author=author)
        if created:
            return JsonResponse(SUCCESS_MESSAGE, status=status.HTTP_200_OK)
        return JsonResponse(FAIL_MESSAGE, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        subscribe = Subscribe.objects.filter(subscriber=request.user,
                                             author_id=pk)
        subscribe.delete()
        return JsonResponse(SUCCESS_MESSAGE, status=status.HTTP_200_OK)


class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class PurchaseViewSet(viewsets.ViewSet):

    def get(self, request):
        return JsonResponse(SUCCESS_MESSAGE, status=status.HTTP_200_OK)

    def create(self, request):
        assert 'id' in request.data, 'В запросе не указан id рецепта'
        recipe_id = int(request.data.get('id'))
        shopping_list = request.session.get('shopping_list', default=[])
        if recipe_id in shopping_list:
            return JsonResponse(FAIL_MESSAGE,
                                status=status.HTTP_400_BAD_REQUEST)

        shopping_list.append(recipe_id)
        request.session['shopping_list'] = shopping_list
        return JsonResponse(SUCCESS_MESSAGE, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        pk = int(pk)
        shopping_list = request.session.get('shopping_list', default=[])

        if pk not in shopping_list:
            return JsonResponse(FAIL_MESSAGE,
                                status=status.HTTP_400_BAD_REQUEST)

        shopping_list.remove(pk)
        request.session['shopping_list'] = shopping_list
        return JsonResponse(SUCCESS_MESSAGE, status=status.HTTP_200_OK)
