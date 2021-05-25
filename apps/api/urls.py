from django.urls import path, include
from api import views
from rest_framework import routers


app_name = 'api'

router_v1 = routers.SimpleRouter()
router_v1.register('favorites', views.FavoriteViewSet, basename='favorites')
router_v1.register('subscriptions', views.SubscribeViewSet,
                   basename='subscriptions')
router_v1.register('ingredients', views.IngredientViewSet,
                   basename='ingredients')
router_v1.register('purchases', views.PurchaseViewSet, basename='purchases')


urlpatterns = [
    path('v1/', include(router_v1.urls))
]
