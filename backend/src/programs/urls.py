from django.urls import path
from .views.ProgramView import ListCreateProgramsView, GetUpdateDeleteProgramView, UploadProgramView, \
    GetUpdateDeleteRSSView, DownloadProgramView

urlpatterns = [
    path('', ListCreateProgramsView.as_view()),
    path('<int:pk>/', GetUpdateDeleteProgramView.as_view(), name='programdetail'),
    path('<int:pk>/upload/', UploadProgramView.as_view(), name='programupload'),
    path('<int:pk>/upload_rss/', GetUpdateDeleteRSSView.as_view(), name='programuploadrss'),
    path('<int:pk>/download/<str:date>/', DownloadProgramView.as_view(), name='programdownload'),
]
