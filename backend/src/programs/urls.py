from django.urls import path

from .views.ProgramView import ListCreateProgramsView, GetUpdateDeleteProgramView, UploadProgramView, \
    GetUpdateDeleteRSSView, GetDeleteArchiveProgramView, GetArchiveContentsView, GetArchiveStatistics, \
    GetProgramAlreadyUploadedDates, GetWeeklySchedule, GetArchiveNextUpload, GetFreeSlots

urlpatterns = [
    path('', ListCreateProgramsView.as_view()),
    path('<int:pk>/', GetUpdateDeleteProgramView.as_view(), name='programdetail'),
    path('<int:pk>/upload/', UploadProgramView.as_view(), name='programupload'),
    path('<int:pk>/upload/uploaded-dates/', GetProgramAlreadyUploadedDates.as_view(), name='programuploadeddates'),
    path('<int:pk>/upload/rss/', GetUpdateDeleteRSSView.as_view(), name='programuploadrss'),
    path('<int:pk>/archive/next-upload/', GetArchiveNextUpload.as_view(), name='programnextupload'),
    path('free-slots/', GetFreeSlots.as_view(), name='freeslots'),
    # previous path has to be before the url with <str:date> to avoid conflicts
    path('<int:pk>/archive/<str:date>/', GetDeleteArchiveProgramView.as_view(), name='programdownload'),
    path('<int:pk>/archive/', GetArchiveContentsView.as_view(), name='programarchive'),
    path('archive/stats/', GetArchiveStatistics.as_view(), name='programarchivestats'),
    path('schedule/', GetWeeklySchedule.as_view(), name='programschedule'),
]
