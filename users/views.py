from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, status
from rest_framework.authtoken.views import ObtainAuthToken, Token

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
    serializer_class = UserPatchActivateSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.is_active:
            instance.is_active = True
            instance.save()
            user = UserPatchActivateSerializer(instance)
            return Response(user.data, status=status.HTTP_200_OK)
        raise RedundantUserActivateError


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
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
            # data = model_to_dict(instance)
            serializer = UserPatchActivateSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise RedundantUserDeleteError


class ListFromDateOlderToNewer(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdm]
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all().order_by("date_joined")
        return queryset

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                "user_id": user.id  
            })