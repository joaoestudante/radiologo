from datetime import datetime
from wsgiref.util import FileWrapper

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.keydoc import KeyDoc
from ..services.KeyDocService import KeyDocService
from django.core.mail import EmailMultiAlternatives


class KeyDocGenerate(APIView):
    def get(self, request):
        now = datetime.now()
        try:
            doc = KeyDoc.objects.get(pk=1)
            doc.creator = request.user
        except KeyDoc.DoesNotExist:
            doc = KeyDoc(creator=request.user)

        service = KeyDocService(doc)
        out = service.generate_file()

        subject, from_email, to = "Documento para requisição de chaves", settings.EMAIL_HOST_USER, settings.ADMIN_EMAIL
        context = {
            "requester": doc.creator.author_name,
            "request_date": now.isoformat()
        }
        email_html_message = render_to_string(settings.KEYDOC_HTML, context)
        email_plaintext_message = render_to_string(settings.KEYDOC_TXT, context)

        msg = EmailMultiAlternatives(subject, email_plaintext_message, from_email, [to])
        msg.attach_alternative(email_html_message, "text/html")
        msg.attach_file(out, "application/pdf")
        msg.send()

        return Response(status=status.HTTP_200_OK)
