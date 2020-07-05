from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

from radiologo.emailservice import EmailService


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_service = EmailService(subject="Recuperação de password no Radiólogo", to=reset_password_token.user.email)
    email_service.send_password_recover(token=reset_password_token.key)
