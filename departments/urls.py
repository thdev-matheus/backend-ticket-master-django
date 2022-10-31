from django.urls import path

from departments import views

urlpatterns = [
    path("department/", views.CreateDepartmentView.as_view()),
    path("department/<department_id>/", views.PatchDeleteDepartmentView.as_view()),
    path("department/<department_id>/activate/", views.ReactivateDepartmentView.as_view()),
]