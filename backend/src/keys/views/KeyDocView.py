import json

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from radiologo.emailservice import EmailService
from ..models.keydoc import KeyDoc
from ..serializers.KeyDocSerializer import KeyDocSerializer
from ..services.KeyDocService import KeyDocService


class KeyDocGenerate(APIView):
    def post(self, request):
        service = KeyDocService(user=request.user)
        out = service.generate_file()

        email_service = EmailService(subject="Documento para requisição de chaves", to=settings.ADMIN_EMAIL)
        email_service.send_keydoc(author_name=request.user.author_name, doc=out)

        return Response(status=status.HTTP_200_OK)


class KeyDocInfo(APIView):
    def get(self, request):
        try:
            doc = KeyDoc.objects.latest('pk')
        except KeyDoc.DoesNotExist:
            return Response(status=status.HTTP_200_OK,
                            data=json.dumps({"detail": "No document has been generated yet."}))

        serialized = KeyDocSerializer(doc)
        return Response(serialized.data, status=status.HTTP_200_OK)
