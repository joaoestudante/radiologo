from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(settings.BASE_FRONTEND_URL + reverse('password_reset:reset-password-request'),
                                                   reset_password_token.key)
    }
    print("reset url will be: {}?token={}".format(settings.BASE_FRONTEND_URL + reverse('password_reset:reset-password-request'),
                                                  reset_password_token.key))

    email_html_message = render_to_string(settings.PASSWORD_RESET_HTML, context)
    email_plaintext_message = render_to_string(settings.PASSWORD_RESET_TXT, context)

    msg = EmailMultiAlternatives(
        "Recuperação de password no Radiólogo",
        email_plaintext_message,
        "radiologo@radiozero.pt",
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
