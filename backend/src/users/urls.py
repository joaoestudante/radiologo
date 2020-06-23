from django.urls import path, include

from .views.InviteView import InviteAcceptView, InviteListView, InviteResendView
from .views.UserView import ListCreateUsersView, GetUpdateDeleteUserView

urlpatterns = [
    path('', ListCreateUsersView.as_view()),
    path('<int:pk>/', GetUpdateDeleteUserView.as_view()),
    path('register/<str:token>/', InviteAcceptView.as_view()),
    path('invites/', InviteListView.as_view()),
    path('invites/resend/', InviteResendView.as_view()),
    path('password/', include('django_rest_passwordreset.urls', namespace='password_reset'))
]

# Password URL provides password/reset_password/ and password/reset_password/confirm/ to request a new password and
# change it, respectively