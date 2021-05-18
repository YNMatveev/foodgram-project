from django.urls import path, include
from api import views
from rest_framework import routers


app_name = 'api'

router = routers.SimpleRouter()
router.register('favorites', views.FavoriteViewSet, basename='favorites')
router.register('subscriptions', views.SubscribeViewSet,
                basename='subscriptions')
router.register('ingredients', views.IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls))
]
