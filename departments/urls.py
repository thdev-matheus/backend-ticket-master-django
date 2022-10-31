from django.urls import path

from departments import views

urlpatterns = [
    path("department/", views.CreateDepartmentView.as_view()),
    path("department/<pk>/", views.PatchDeleteDepartmentView.as_view()),
    path("department/<pk>/activate/", views.ReactivateDepartmentView.as_view()),
]