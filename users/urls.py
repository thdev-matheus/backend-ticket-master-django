from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.UserView.as_view()),
    path("users/", views.UserView.as_view()),
    path("users/<str:user_id>/", views.UserDetailView.as_view()),
    path("users/<str:user_id>/activate/", views.ReactivateUserView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("users/order/time/", views.ListFromDateOlderToNewer.as_view()),
]
