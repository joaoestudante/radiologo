import os
import struct

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import signing
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.utils import timezone, crypto
from .user import CustomUser



class Invite(models.Model):
    invited_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sent_token = models.CharField(max_length=256, default="")
    accepted = models.BooleanField(default=False)
    last_date_sent = models.DateTimeField(default=timezone.now)

    def invited_user_author_name(self):
        return self.invited_user.author_name

    def generate_token(self):
        # Inspired by: https://github.com/aaugustin/django-sesame/

        raw_token = struct.pack(str("!i"), self.invited_user.pk) + crypto.pbkdf2(self.invited_user.email, "radiologo",
                                                                                 10000)
        url_ready_token = signing.TimestampSigner(salt="radiologo").sign(signing.b64_encode(raw_token).decode())
        self.sent_token = url_ready_token
        return url_ready_token

    def send(self):
        token = self.generate_token()
        subject, from_email, to = "Bem vindo à Rádio Zero", settings.EMAIL_HOST_USER, self.invited_user.email
        with open(settings.EMAIL_TXT, 'r') as txt:
            text_content = txt.read().replace("{{ REGISTER_LINK }}", settings.BASE_FRONTEND_URL + "register/" + token)
        with open(settings.EMAIL_HTML, 'r') as html:
            html_content = html.read().replace("{{ REGISTER_LINK }}", settings.BASE_FRONTEND_URL + "register/" + token)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        self.sent_token = token
        self.last_date_sent = timezone.now()
        self.save()

    @staticmethod
    def get_pk_from_token(token):
        data = signing.TimestampSigner(salt="radiologo").unsign(token)
        decoded = signing.b64_decode(data.encode())
        return (struct.unpack(str("!i"), decoded[:4])[0], decoded[4:])[0]
