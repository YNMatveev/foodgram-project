from django.urls import path
from shopping_list import views


app_name = 'shopping_list'

urlpatterns = [
    path('', views.ShoppingListView.as_view(), name='main'),
    path('download/', views.DownloadShoppingList.as_view(), name='download'),
    path('download/empty', views.EmptyShoppingList.as_view(), name='empty')
]
