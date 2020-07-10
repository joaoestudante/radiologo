import json
from datetime import datetime

import paramiko
from django.conf import settings
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.status as status
from rest_framework import authentication, permissions

from exceptions.radiologoexception import InvalidDateFormatForEmissionException, InvalidDateForEmissionException
from radiologo import celery_app
from .. import tasks
from ..models import Slot
from ..serializers.ProgramSerializer import ProgramSerializer
from ..models.program import Program
from django.shortcuts import get_object_or_404

from ..services.ProgramService import ProgramService
from ..services.RemoteService import RemoteService
from ..services.processing.ProcessingService import ProcessingService


class ListCreateProgramsView(APIView):

    def get(self, request):
        programs = [program for program in Program.objects.all()]
        serialized = ProgramSerializer(programs, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serialized = ProgramSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class GetUpdateDeleteProgramView(APIView):

    def get(self, request, pk):
        program = get_object_or_404(Program, pk=pk)
        serialized = ProgramSerializer(program)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        program = get_object_or_404(Program, pk=pk)
        serialized = ProgramSerializer(program, data=request.data, partial=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        program = get_object_or_404(Program, pk=pk)
        program.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UploadProgramView(APIView):

    def put(self, request, pk):
        program = Program.objects.get(pk=pk)

        ProcessingService.save_file(uploaded_file=request.data['file'], emission_date=request.data['date'], program=program)

        tasks.process_audio.delay(uploaded_file_path=settings.FILE_UPLOAD_DIR + request.data['file'].name,
                                  program_pk = program.pk,
                                  uploader=request.user.author_name,
                                  email=request.user.email,
                                  emission_date=request.data['date'])

        return Response(status=status.HTTP_200_OK)


class GetUpdateDeleteRSSView(APIView):
    def get(self, request, pk):
        program = get_object_or_404(Program, pk=pk)
        rss_feed_url = program.rss_feed_url
        rss_status = program.rss_feed_status
        return Response(status=status.HTTP_200_OK,
                        data=json.dumps({'feed_url': rss_feed_url, 'feed_status': rss_status}))

    def patch(self, request, pk):
        program = get_object_or_404(Program, pk=pk)
        # Current values
        current_url = program.rss_feed_url
        current_status = program.rss_feed_status
        # Check new values
        new_url = request.data['feed_url']
        new_status = request.data['feed_status']
        try:
            assert type(new_status) is bool
            validate = URLValidator()
            validate(new_url)
        except ValidationError:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except AssertionError:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        program.rss_feed_url = new_url
        program.rss_feed_status = new_status
        return Response(status=status.HTTP_201_CREATED,
                        data=json.dumps({'feed_url': program.rss_feed_url, 'feed_status': program.rss_feed_status}))

    def delete(self, request, pk):
        program = get_object_or_404(Program, pk=pk)
        program.rss_feed_url = ""
        program.rss_feed_status = False
        program.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetDeleteArchiveProgramView(APIView):
    def get(self, request, pk, date):
        program = get_object_or_404(Program, pk=pk)
        return RemoteService().download_archive_file(program, date)

    def delete(self, request, pk, date):
        program = get_object_or_404(Program, pk=pk)
        RemoteService().delete_archive_file(program, date)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetArchiveContentsView(APIView):
    def get(self, request, pk):
        program = get_object_or_404(Program, pk=pk)
        file_list = RemoteService().get_archive_contents(program.normalized_name())
        return Response(status=status.HTTP_200_OK, data=json.dumps(file_list))


class GetArchiveStatistics(APIView):
    def get(self, request):
        stats = RemoteService().get_archive_stats()
        return Response(status=status.HTTP_200_OK, data=json.dumps(stats))

class GetProgramAlreadyUploadedDates(APIView):
    def get(self, request, pk):
        program = Program.objects.get(pk=pk)
        dates = RemoteService().get_uploaded_dates(program)
        return Response(status=status.HTTP_200_OK, data=json.dumps(dates))