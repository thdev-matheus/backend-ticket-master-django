from django.urls import path

from comments import views

urlpatterns = [
    # path("comment/", views.ListAllCommentsView.as_view()),
    path("comment/register/<ticket_id>/", views.CreateCommentView.as_view()),
    path("comment/<comment_id>/", views.GetIDPatchDeleteCommentView.as_view()),
    path("comment/user/<user_id>/", views.GetUserCommentsView.as_view()),
    path("comment/ticket/<ticket_id>/", views.GetTicketCommentsView.as_view()),
]
