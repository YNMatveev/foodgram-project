from django.urls import path
from recipes import views
from django.views.generic import RedirectView

app_name = 'recipes'

urlpatterns = [
    path('', RedirectView.as_view(url='recipes/')),
    path('recipes/', views.home_page, name='index'),
]
