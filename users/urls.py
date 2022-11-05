from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from . import views

urlpatterns = [
    path("register/", views.UserView.as_view()),
    path("users/", views.UserView.as_view()),
    path("users/<str:user_id>/", views.UserDetailView.as_view()),
    path("users/<str:user_id>/userActivate/", views.ReactivateUserView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("users/order/time/", views.ListFromDateOlderToNewer.as_view())
]
