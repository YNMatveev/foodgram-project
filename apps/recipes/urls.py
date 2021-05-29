from django.urls import path
from recipes import views
from django.views.generic import RedirectView

app_name = 'recipes'

urlpatterns = [
    path('', RedirectView.as_view(url='recipes/')),
    path('recipes/', views.RecipeListView.as_view(), name='index'),
    path('recipes/create/', views.RecipeEditView.as_view(),
         name='new_recipe'),
    path('recipes/<int:id>/<slug:slug>/', views.RecipeDetailView.as_view(),
         name='recipe_details'),
    path('recipes/<int:id>/<slug:slug>/update/',
         views.RecipeEditView.as_view(), name='update_recipe'),
    path('recipes/<int:id>/<slug:slug>/delete/',
         views.RecipeEditView.as_view(), name='delete_recipe'),
    path('profile/<str:username>/', views.ProfileListView.as_view(),
         name='profile'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorites'),
    path('subscribes/', views.SubscribeListView.as_view(), name='subscribes'),
]
