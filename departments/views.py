from departments.exceptions import RedundantActivateError, RedundantDeleteError
from departments.models import Department
from departments.serializers import DepartmentSerializer
from django.forms import model_to_dict
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import Response, status
from users.permissions import IsAdm, IsAdmOrListOnly


class CreateDepartmentView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmOrListOnly]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PatchDeleteDepartmentView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdm]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    lookup_url_kwarg = "department_id"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_active:
            instance.is_active = False
            instance.save()
            data = model_to_dict(instance)
            return Response(data, status=status.HTTP_200_OK)
        raise RedundantDeleteError


class ReactivateDepartmentView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdm]
    queryset = Department.objects.all()
    lookup_url_kwarg = "department_id"
    serializer_class = DepartmentSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.is_active:
            instance.is_active = True
            instance.save()
            data = model_to_dict(instance)
            return Response(data, status=status.HTTP_200_OK)
        raise RedundantActivateError
