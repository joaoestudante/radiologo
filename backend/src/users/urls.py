from django.urls import path

from .views.InviteView import InviteAcceptView
from .views.UserView import ListCreateUsersView, GetUpdateDeleteUserView

urlpatterns = [
    path('', ListCreateUsersView.as_view()),
    path('<int:pk>/', GetUpdateDeleteUserView.as_view()),
    path('register/<str:token>/', InviteAcceptView.as_view()),
]