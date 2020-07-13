import json
from datetime import datetime

import paramiko
from django.conf import settings
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.status as status
from rest_framework import authentication, permissions

from radiologo import celery_app
from radiologo.permissions import IsAdministration, IsRadiologoDeveloper, IsDirector, IsProgrammingRW
from .. import tasks

from ..services.RemoteService import RemoteService
from ..services.processing.ProcessingService import ProcessingService

class UploadTrackView(APIView):
    permission_classes = (
        IsAuthenticated, (
                IsAdministration | IsDirector | IsRadiologoDeveloper |
                IsProgrammingRW
        )
    )

    def put(self, request):
        """ Expects file, title, artist"""
        ProcessingService.save_file(uploaded_file=request.data['file'], \
                                    artist=request.data['artist'], title=request.data['title'])
        tasks.process_audio.delay(uploaded_file_path=settings.FILE_UPLOAD_DIR + request.data['file'].name, \
                                    artist=request.data['artist'], title=request.data['title'])
        return Response(status=status.HTTP_200_OK)

class GetDeleteTrackView(APIView):
    permission_classes = UploadTrackView.permission_classes

    """ Expects filename as name in URL path"""
    def get(self, request, name):
        # return RemoteService().download_playlist_file(filename = name)
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def delete(self, request, name):
        RemoteService().delete_playlist_file(filename = name)
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetPlaylistContentsView(APIView):
    def get(self, request):
        file_list = RemoteService().get_playlist_contents()
        return Response(status=status.HTTP_200_OK, data=file_list)
