from django.urls import path
from . import views

from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path("register/", views.UserView.as_view()),
    path("users/", views.UserView.as_view()),
    path("users/<str:user_id>/", views.UserUpdateView.as_view()),
    path("login/", ObtainAuthToken.as_view()),   
]