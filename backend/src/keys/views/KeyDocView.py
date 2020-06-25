import json
from datetime import datetime
from wsgiref.util import FileWrapper

import pytz
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.keydoc import KeyDoc
from ..serializers.KeyDocSerializer import KeyDocSerializer
from ..services.KeyDocService import KeyDocService
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

class KeyDocGenerate(APIView):
    def post(self, request):
        now = datetime.now()
        service = KeyDocService(user=request.user)
        out = service.generate_file()

        subject, from_email, to = "Documento para requisição de chaves", settings.EMAIL_HOST_USER, settings.ADMIN_EMAIL
        context = {
            "requester": request.user.author_name,
            "request_date": now.strftime("%Y-%m-%d, às %H:%M ") + settings.timezone
        }
        email_html_message = render_to_string(settings.KEYDOC_HTML, context)
        email_plaintext_message = render_to_string(settings.KEYDOC_TXT, context)

        msg = EmailMultiAlternatives(subject, email_plaintext_message, from_email, [to])
        msg.attach_alternative(email_html_message, "text/html")
        msg.attach_file(out, "application/pdf")
        msg.send()

        return Response(status=status.HTTP_200_OK)

class KeyDocInfo(APIView):
    def get(self, request):
        try:
            doc = KeyDoc.objects.latest('pk')
        except KeyDoc.DoesNotExist:
            return Response(status=status.HTTP_200_OK, data=json.dumps({"detail":"No document has been generated yet."}))

        serialized = KeyDocSerializer(doc)
        print(serialized.data)
        return Response(serialized.data, status=status.HTTP_200_OK)