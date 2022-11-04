import ipdb
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, status

from departments.models import Department
from departments.serializers import DepartmentSerializer
from solutions.exceptions import (
    UnauthorizedUserCreateSolutionError,
    UnauthorizedUserListAllSolutionsError,
    UnauthorizedUserListSolutionError,
)
from solutions.models import Solution
from solutions.permissions import IsAdmOrFromTicketDepartmentOrOwner
from solutions.serializers import (
    SolutionSerializer,
    SolutionSerializerDetailed,
    SolutionSerializerDetailedNoSupport,
)
from tickets.models import Ticket
from tickets.serializers import TicketSerializerDetailed
from utils.mixins import SerializerMapping


class ListCreateSolutionsView(SerializerMapping, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Solution.objects.all()
    serializer_map = {
        "GET": SolutionSerializerDetailedNoSupport,
        "POST": SolutionSerializer,
    }

    def perform_create(self, serializer):
        ticket_obj = Ticket.objects.get(id=self.request.data["ticket"])
        
        if (
            self.request.user != ticket_obj.support
            and self.request.user != ticket_obj.user
            and not self.request.user.is_superuser
        ):
             raise UnauthorizedUserCreateSolutionError
        
        ticket_obj.is_solved = True 
        ticket_obj.save()  
        serializer.save(ticket=ticket_obj, user=self.request.user)

    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        solution = Solution.objects.get(id=serializer.data["id"])
        serializer = SolutionSerializerDetailedNoSupport(solution)
        return Response(
             serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def list(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise UnauthorizedUserListAllSolutionsError

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ListSolutionView(SerializerMapping, generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Solution.objects.all()
    serializer_map = {
        "GET": SolutionSerializerDetailed,
        "POST": SolutionSerializer,
    }
    lookup_url_kwarg = "solution_id"

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        department_id = instance.ticket.support_department.id
        ticket_owner = instance.ticket.user

        def is_not_from_dept():
            if not request.user.department:
                return True
            return department_id != request.user.department.id

        if (
            not request.user.is_superuser
            and ticket_owner != request.user
            and is_not_from_dept()
        ):
            raise UnauthorizedUserListSolutionError

        return Response(serializer.data)


class ListAllSolutionFromDepartmentView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_url_kwarg = "department_id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        def is_not_from_dept():
            if not request.user.department:
                return True
            return instance.id != request.user.department.id

        if is_not_from_dept() and not request.user.is_superuser:
            raise UnauthorizedUserListSolutionError

        serializer = self.get_serializer(instance)
        solutions = Solution.objects.filter(ticket__support_department=instance)
        serializer = SolutionSerializerDetailedNoSupport(solutions, many=True)

        return Response(serializer.data)


class ListSolutionFromTicketView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmOrFromTicketDepartmentOrOwner]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializerDetailed
    lookup_url_kwarg = "ticket_id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        solution = Solution.objects.get(ticket=instance)
        serializer = SolutionSerializerDetailedNoSupport(solution)

        return Response(serializer.data)
