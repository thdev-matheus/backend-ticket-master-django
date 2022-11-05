from departments.models import Department
from departments.serializers import DepartmentSerializer
from django.forms import model_to_dict
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, status
from tickets.exceptions import (
    NoTicketsError,
    NoTicketsToSolveError,
    RedundantSolveError,
    UnathorizedListingError,
)
from tickets.models import Ticket
from tickets.permissions import (
    IsFromDepartment,
    IsOwnerOrFromDepartment,
    OnlyAdmCanListAll,
)
from tickets.serializers import (
    TicketSerializer,
    TicketSerializerDetailed,
    TicketSerializerNoDepartment,
    TicketSerializerNoSupport,
)
from users.models import User
from users.permissions import IsAdm


class ListCreateTicketsView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, OnlyAdmCanListAll]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class TicketDetailedView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrFromDepartment]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializerDetailed
    lookup_url_kwarg = "ticket_id"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.is_solved:
            instance.is_solved = True
            instance.save()
            data = model_to_dict(instance)
            return Response(data, status=status.HTTP_200_OK)
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
            "support": {"id": request.user.id, "name": request.user.username},
        }
        return Response(data, status=status.HTTP_200_OK)


class ListTicketTotalsView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdm]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializerDetailed

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        all_depts = Department.objects.all()
        dpts_data = []
        for dept in all_depts:
            data = {"department_name": dept.name, "total_open_tickets": 0}
            dpts_data.append(data)

        for ticket in serializer.data:
            for department in dpts_data:
                if (
                    department["department_name"]
                    == str(ticket["support_department"]["name"])
                    and not ticket["is_solved"]
                ):
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
        tickets = Ticket.objects.all().filter(
            support_department=dpt_id, is_solved=False
        )
        serializer = TicketSerializerNoDepartment(tickets, many=True)

        return Response(serializer.data)


class ListMostUrgentTicketView(ListTicketsFromDepartmentView):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        dpt_id = serializer.data["id"]
        tickets = Ticket.objects.all().filter(
            support_department=dpt_id,
            is_solved=False,
            support__isnull=True,
            urgency="High",
        )
        if not tickets:
            tickets = Ticket.objects.all().filter(
                support_department=dpt_id,
                is_solved=False,
                support__isnull=True,
                urgency="Average",
            )
        if not tickets:
            tickets = Ticket.objects.all().filter(
                support_department=dpt_id,
                is_solved=False,
                support__isnull=True,
                urgency="Low",
            )

        if tickets:
            tickets = sorted(tickets, key=lambda x: x.created_at)
            instance = Ticket.objects.get(id=tickets[0].id)
            instance.support = request.user
            instance.save()
            serializer = TicketSerializerNoDepartment(instance)
            return Response(serializer.data)

        dpt_name = serializer.data["name"]
        return Response(
            {
                "detail": f"No tickets left unattended for the {dpt_name} department to solve"
            }
        )


class ListTicketsFromUserView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrFromDepartment]
    serializer_class = TicketSerializerDetailed

    def get_queryset(self):
        user_obj = User.objects.get(id=self.kwargs.get("user_id"))
        queryset = Ticket.objects.filter(user=user_obj)

        if not queryset:
            raise NoTicketsError
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.user != queryset[0].user and not request.user.is_superuser:
            raise UnathorizedListingError

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ListTicketFromSupportUserView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializerNoSupport

    def get_queryset(self):
        user_obj = User.objects.get(id=self.kwargs.get("support_user_id"))
        queryset = Ticket.objects.filter(support=user_obj, is_solved=False)

        if not queryset:
            raise NoTicketsToSolveError
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.user != queryset[0].support and not request.user.is_superuser:
            raise UnathorizedListingError

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
