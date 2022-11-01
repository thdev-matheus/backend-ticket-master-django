from django.forms import model_to_dict
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Request, Response, status

from users.exceptions import RedundantUserActivateError, RedundantUserDeleteError
from users.models import User
from users.permissions import IsAdm
from users.serializers import UserPatchActivateSerializer, UserSerializer


class UserView(generics.ListCreateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdm]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReactivateUserView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdm]

    queryset = User.objects.all()
    lookup_url_kwarg = "user_id"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.is_active:
            instance.is_active = True
            instance.save()
            user = UserPatchActivateSerializer(instance)
            return Response(user.data, status=status.HTTP_200_OK)
        raise RedundantUserActivateError


class UserDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdm]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "user_id"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_active:
            instance.is_active = False
            instance.save()
            data = model_to_dict(instance)
            return Response(data, status=status.HTTP_200_OK)
        raise RedundantUserDeleteError
