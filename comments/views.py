from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from tickets.models import Ticket
from users.models import User

from .models import Comment
from .permissions import IsOwnerOrFromComment, isSameDepartamentOrOwnerTicket
from .serializers import CommentSerializer


class CreateCommentView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = "ticket_id"

    def perform_create(self, serializer):
        user_obj = User.objects.get(id=self.request.user.id)
        ticket_obj = Ticket.objects.get(id=self.kwargs.get("ticket_id"))
        serializer.save(ticket=ticket_obj, user=user_obj)


class GetIDPatchDeleteCommentView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrFromComment]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = "comment_id"


class GetUserCommentsView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        user_obj = User.objects.get(id=self.kwargs.get("user_id"))
        queryset = Comment.objects.filter(user=user_obj)
        return queryset


class GetTicketCommentsView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [isSameDepartamentOrOwnerTicket]
    serializer_class = CommentSerializer

    def get_queryset(self):
        ticket_obj = Ticket.objects.get(id=self.kwargs.get("ticket_id"))
        queryset = Comment.objects.filter(ticket=ticket_obj)
        return queryset
