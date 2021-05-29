from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import JsonResponse
from recipes.models import Favorite, Ingredient, Subscribe
from rest_framework import filters, mixins, permissions, status, viewsets

from shopping_list.views import PurchaseMixin
from api.serializers import IngredientSerializer

User = get_user_model()


success_response = JsonResponse({'success': 'true'})
fail_response = JsonResponse({'success': 'false'},
                             status=status.HTTP_400_BAD_REQUEST)


class CreateDeleteView(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]

    model = None
    user_field = None
    object_field = None

    def get_kwargs(self, user, obj_id):
        return {
            f'{self.user_field}': user,
            f'{self.object_field}_id': obj_id
        }

    def create(self, request):
        obj_id = request.data.get('id')
        kwargs = self.get_kwargs(request.user, obj_id)
        try:
            self.model.objects.create(**kwargs)
        except IntegrityError:
            return fail_response
        return success_response

    def destroy(self, request, pk=None):
        obj_id = pk
        kwargs = self.get_kwargs(request.user, obj_id)
        obj = self.model.objects.filter(**kwargs)
        result = obj.delete()
        if result:
            return success_response
        return fail_response


class FavoriteViewSet(CreateDeleteView):

    model = Favorite
    user_field = 'chooser'
    object_field = 'recipe'


class SubscribeViewSet(CreateDeleteView):

    model = Subscribe
    user_field = 'subscriber'
    object_field = 'author'


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
