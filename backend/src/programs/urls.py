from django.urls import path
from .views.ProgramView import ListCreateProgramsView, GetUpdateDeleteProgramView

urlpatterns = [
    path('', ListCreateProgramsView.as_view()),
    path('<int:pk>/', GetUpdateDeleteProgramView.as_view(), name='programdetail')
]