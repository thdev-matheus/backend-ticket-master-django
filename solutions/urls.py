from django.urls import path

from . import views

urlpatterns = [
    path(
        "solutions/",
        views.ListCreateSolutionsView.as_view(),
    ),
    path(
        "solutions/<solution_id>/",
        views.ListSolutionView.as_view(),
    ),
    path(
        "solutions/department/<department_id>/",
        views.ListAllSolutionFromDepartmentView.as_view(),
    ),
    path(
        "solution/ticket/<ticket_id>/",
        views.ListSolutionFromTicketView.as_view(),
    ),
]
