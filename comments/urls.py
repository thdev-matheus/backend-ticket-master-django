from django.urls import path

from comments import views

urlpatterns = [
<<<<<<< HEAD
    #path("comment/", views.ListAllCommentsView.as_view()),
=======
    # path("comment/", views.ListAllCommentsView.as_view()),
>>>>>>> 985e39a4d2a9fb9dd9edb6b6d9bd4221e8c73163
    path("comment/register/<ticket_id>/", views.CreateCommentView.as_view()),
    path("comment/<comment_id>/", views.GetIDPatchDeleteCommentView.as_view()),
    path("comment/user/<user_id>/", views.GetUserCommentsView.as_view()),
    path("comment/ticket/<ticket_id>/", views.GetTicketCommentsView.as_view()),
]
