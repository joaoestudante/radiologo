import json
from datetime import datetime

from django.conf import settings
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
        emission_slots = list(program.slot_set.all())
        weekday = self.get_emission_weekday(emission_slots, program, request)

        ProcessingService.save_file(uploaded_file=request.data['file'], program_name=program.normalized_name(),
                                    emission_date=request.data['date'], weekday=weekday)

        tasks.process_audio.delay(uploaded_file_path=settings.FILE_UPLOAD_DIR + request.data['file'].name,
                                  uploader=request.user.author_name,
                                  program_name=program.normalized_name(),
                                  emission_date=request.data['date'],
                                  weekday=weekday,
                                  already_normalized=program.comes_normalized,
                                  adjust_duration=not program.ignore_duration_adjustment)

        return Response(status=status.HTTP_200_OK, data=json.dumps({"Nice": "Nice"}))

    def get_emission_weekday(self, emission_slots, program, request):
        try:
            emission_date_obj = datetime.strptime(request.data['date'], "%Y%m%d")
        except ValueError:
            raise InvalidDateFormatForEmissionException
        if len(emission_slots) > 1:
            isoweekday = emission_date_obj.isoweekday()
            if isoweekday not in program.enabled_days:
                raise InvalidDateForEmissionException

            weekday = program.slot_set.filter(weekday=Slot.iso_to_custom_format(isoweekday))[
                0].weekday
        else:
            weekday = ""
        return weekday
