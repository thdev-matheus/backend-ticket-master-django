from django.forms import model_to_dict
from rest_framework import generics
from rest_framework.views import Request, Response, status
from rest_framework.authentication import TokenAuthentication

from tickets.permissions import IsOwnerOrFromDepartment, OnlyAdmCanListAll

from tickets.models import Ticket
from tickets.serializers import TicketSerializer

class ListCreateTicketsView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [OnlyAdmCanListAll]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


    