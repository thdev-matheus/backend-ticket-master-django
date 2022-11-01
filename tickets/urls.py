from django.urls import path

from tickets import views

urlpatterns = [
    path("tickets/", views.ListCreateTicketsView.as_view()),
    
]