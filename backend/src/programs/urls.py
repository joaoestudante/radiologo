from django.urls import path
from .views.ProgramView import ListCreateProgramsView, GetUpdateDeleteProgramView, UploadProgramView, \
    GetUpdateDeleteRSSView, GetDeleteArchiveProgramView, GetArchiveContentsView, GetArchiveStatistics

urlpatterns = [
    path('', ListCreateProgramsView.as_view()),
    path('<int:pk>/', GetUpdateDeleteProgramView.as_view(), name='programdetail'),
    path('<int:pk>/upload/', UploadProgramView.as_view(), name='programupload'),
    path('<int:pk>/upload_rss/', GetUpdateDeleteRSSView.as_view(), name='programuploadrss'),
    path('<int:pk>/archive/<str:date>/', GetDeleteArchiveProgramView.as_view(), name='programdownload'),
    path('<int:pk>/archive/', GetArchiveContentsView.as_view(), name='programarchive'),
    path('archive/stats/', GetArchiveStatistics.as_view(), name='programarchivestats'),
]
