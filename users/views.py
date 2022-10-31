from rest_framework import generics

from users.models import User

from users.serializers import UserSerializer


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
