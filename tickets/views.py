from django.forms import model_to_dict
from rest_framework import generics
from rest_framework.views import Response, status
from rest_framework.authentication import TokenAuthentication

from tickets.permissions import IsOwnerOrFromDepartment,OnlyAdmCanListAll,IsFromDepartment
from users.permissions import IsAdm

from tickets.models import Ticket
from tickets.serializers import TicketSerializer,TicketSerializerPatch,TicketSerializerNoDepartment
from tickets.exceptions import RedundantSolveError

from departments.models import Department
from departments.serializers import DepartmentSerializer

import ipdb

class ListCreateTicketsView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [OnlyAdmCanListAll]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketDetailedView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrFromDepartment]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializerPatch
    lookup_url_kwarg = "ticket_id"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if not instance.is_solved:
            instance.is_solved = True
            instance.save()
            data=model_to_dict(instance)
            return Response(data,status=status.HTTP_200_OK)
        raise RedundantSolveError

    def update(self, request, *args, **kwargs):
        
        instance = self.get_object()
        instance.support = request.user
        instance.save()
        raw_data = model_to_dict(instance)
        data = {
            "description": raw_data["description"],
            "is_solved": raw_data["is_solved"],
            "urgency": raw_data["urgency"],
            "support": {"id":request.user.id, "name":request.user.username}
        }
        return Response(data,status=status.HTTP_200_OK)
        

class ListTicketTotalsView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdm]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        all_depts = Department.objects.all()
        dpts_data = [] 
        for dept in all_depts:
            data = {
                "department_name" : dept.name,
                "total_open_tickets": 0
            }
            dpts_data.append(data)

        for ticket in serializer.data:
            for department in  dpts_data:
                if department["department_name"] == str(ticket["support_department"]["name"]) and not ticket["is_solved"]:
                    department["total_open_tickets"] += 1

        return Response(dpts_data)

class ListTicketsFromDepartmentView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsFromDepartment]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_url_kwarg = "department_id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        dpt_id = serializer.data["id"]
        tickets = Ticket.objects.all().filter(support_department = dpt_id, is_solved = False)
        serializer = TicketSerializer(tickets, many=True)
        
        return Response(serializer.data)

class ListMostUrgentTicketView(ListTicketsFromDepartmentView):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        dpt_id = serializer.data["id"]
        tickets = Ticket.objects.all().filter(support_department = dpt_id, is_solved = False, support__isnull=True, urgency="High")
        if not  tickets:
            tickets = Ticket.objects.all().filter(support_department = dpt_id, is_solved = False, urgency="Medium")
        if not tickets:
            tickets = Ticket.objects.all().filter(support_department = dpt_id, is_solved = False, urgency="Low")

        if tickets:
            tickets[0].support=request.user
            serializer = TicketSerializerNoDepartment(tickets[0])
            return Response(serializer.data)
        dpt_name = serializer.data["name"]
        return Response({"detail":f"No tickets to solve for the {dpt_name} department"})