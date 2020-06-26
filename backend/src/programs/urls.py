from django.urls import path
from .views.ProgramView import ListCreateProgramsView, GetUpdateDeleteProgramView, UploadProgramView

urlpatterns = [
    path('', ListCreateProgramsView.as_view()),
    path('<int:pk>/', GetUpdateDeleteProgramView.as_view(), name='programdetail'),
    path('<int:pk>/upload/', UploadProgramView.as_view(), name='programupload'),
]