from django.urls import path, include
from users import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('confirmation/', views.ConfirmationView.as_view(),
         name='confirmation'),
    path('confirmation/<uidb64>/<token>/',
         views.ConfirmationCompleteView.as_view(),
         name='confirmation_complete'),
]

import django.contrib.auth.urls