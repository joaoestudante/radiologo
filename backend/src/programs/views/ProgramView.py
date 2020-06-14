from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.status as status
from rest_framework import authentication, permissions
from ..serializers.ProgramSerializer import ProgramSerializer

from ..models.program import Program

class ListCreateProgramsView(APIView):
    authentication_classes = []
    permission_classes = []

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
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk):
        program = Program.objects.get(pk=pk)
        serialized = ProgramSerializer(program)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        program = Program.objects.get(pk=pk)
        serialized = ProgramSerializer(program, data=request.data, partial=True)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        program = Program.objects.get(pk=pk)
        program.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
