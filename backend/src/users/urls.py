from django.urls import path
from .views.UserView import ListCreateUsersView, GetUpdateDeleteUserView

urlpatterns = [
    path('', ListCreateUsersView.as_view()),
    path('<int:pk>/', GetUpdateDeleteUserView.as_view())
]