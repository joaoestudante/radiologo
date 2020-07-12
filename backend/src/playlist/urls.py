from django.urls import path
from .views.PlaylistView import GetPlaylistContentsView, UploadTrackView, GetDeleteTrackView

urlpatterns = [
    path('', GetPlaylistContentsView.as_view(), name='playlistcontents'),
    path('upload/', UploadTrackView.as_view(), name='trackupload'),
    path('track/<str:name>/', GetDeleteTrackView.as_view(), name='trackdownload'),
]
