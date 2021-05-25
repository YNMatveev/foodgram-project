from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from recipes.models import Favorite, Subscribe, Ingredient
from api.serializers import IngredientSerializer
from rest_framework import filters


class FavoriteViewSet(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        recipe_id = request.data.get('id')
        _, created = Favorite.objects.get_or_create(chooser=request.user,
                                                    recipe_id=recipe_id)
        if created:
            return Response({'success: true'}, status.HTTP_201_CREATED)
        return Response({'success: false'}, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        favorite = Favorite.objects.filter(chooser=request.user,
                                           recipe_id=pk)
        if not favorite.exists():
            return Response({'success: false'}, status.HTTP_400_BAD_REQUEST)

        favorite.delete()
        return Response({'success: true'}, status.HTTP_200_OK)


class SubscribeViewSet(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        author_id = request.data.get('id')
        _, created = Subscribe.objects.get_or_create(subscriber=request.user,
                                                     author_id=author_id)
        if created:
            return Response({'success: true'}, status.HTTP_201_CREATED)
        return Response({'success: false'}, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        subscribe = Subscribe.objects.filter(subscriber=request.user,
                                             author_id=pk)
        if not subscribe.exists():
            return Response({'success: false'}, status.HTTP_400_BAD_REQUEST)

        subscribe.delete()
        return Response({'success: true'}, status.HTTP_200_OK)


class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class PurchaseViewSet(viewsets.ViewSet):

    def get(self, request):
        return Response({'success: true'}, status.HTTP_200_OK)

    def create(self, request):
        assert 'id' in request.data, 'В запросе не указан id рецепта'
        recipe_id = int(request.data.get('id'))
        shopping_list = request.session.get('shopping_list', default=[])
        if recipe_id in shopping_list:
            return Response({'success: false'}, status.HTTP_400_BAD_REQUEST)

        shopping_list.append(recipe_id)
        request.session['shopping_list'] = shopping_list
        return Response({'success: true'}, status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        pk = int(pk)
        shopping_list = request.session.get('shopping_list', default=[])

        if pk not in shopping_list:
            return Response({'success: false'}, status.HTTP_400_BAD_REQUEST)

        shopping_list.remove(pk)
        request.session['shopping_list'] = shopping_list
        return Response({'success: true'}, status.HTTP_200_OK)
