from django.urls import path

from .views.InviteView import InviteAcceptView, InviteListView, InviteResendView
from .views.UserView import ListCreateUsersView, GetUpdateDeleteUserView

urlpatterns = [
    path('', ListCreateUsersView.as_view()),
    path('<int:pk>/', GetUpdateDeleteUserView.as_view()),
    path('register/<str:token>/', InviteAcceptView.as_view()),
    path('invites/', InviteListView.as_view()),
    path('invites/resend/', InviteResendView.as_view())
]