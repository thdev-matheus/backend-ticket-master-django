from departments import views
from django.urls import path

urlpatterns = [
    path(
        "department/",
        views.CreateDepartmentView.as_view(),
    ),
    path(
        "department/<department_id>/",
        views.PatchDeleteDepartmentView.as_view(),
    ),
    path(
        "department/<department_id>/activate/",
        views.ReactivateDepartmentView.as_view(),
    ),
]
