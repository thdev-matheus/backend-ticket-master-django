from django.urls import path

from tickets import views

urlpatterns = [
    path("tickets/", views.ListCreateTicketsView.as_view()),
    path("tickets/<ticket_id>/", views.ListPatchSolveTicketView.as_view()),
    path("summary/tickets/", views.ListTicketTotalsView.as_view()),
    path("tickets/department/<department_id>/", views.ListTicketsFromDepartmentView.as_view()),
    path("tickets/department/<department_id>/newest/", views.ListMostUrgentTicketView.as_view())
]