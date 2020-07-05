from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse


class EmailService:
    def __init__(self, subject: str, to: str):
        self.to = to
        self.subject = subject

    def sendmail(self, context, html_template, txt_template, attachment_path=None):
        email_html_message = render_to_string(html_template, context)
        email_plaintext_message = render_to_string(txt_template, context)
        msg = EmailMultiAlternatives(self.subject, email_plaintext_message, settings.EMAIL_HOST_USER, [self.to])
        msg.attach_alternative(email_html_message, "text/html")
        if attachment_path is not None:
            msg.attach_file(attachment_path, "application/pdf")
        msg.send()

    def send_upload_rejected(self, checker, program_name, emission_date):
        context = {
            "problems": checker.problems,
            "program_name": program_name,
            "emission_date": emission_date[:4] + "-" + emission_date[4:6] + "-" + emission_date[6:],
        }
        self.sendmail(context=context, html_template=settings.UPLOAD_REJECT_HTML,
                      txt_template=settings.UPLOAD_REJECT_TXT)

    def send_upload_accepted(self, checker, program_name, emission_date):
        context = {
            "warnings": checker.warnings,
            "program_name": program_name,
            "emission_date": emission_date[:4] + "-" + emission_date[4:6] + "-" + emission_date[6:],
        }
        self.sendmail(context=context, html_template=settings.UPLOAD_ACCEPT_HTML,
                      txt_template=settings.UPLOAD_ACCEPT_TXT)

    def send_upload_failed(self, program_name, emission_date):
        context = {
            "program_name": program_name,
            "emission_date": emission_date[:4] + "-" + emission_date[4:6] + "-" + emission_date[6:],
        }
        self.sendmail(context=context, html_template=settings.UPLOAD_FAIL_HTML, txt_template=settings.UPLOAD_FAIL_TXT)

    def send_invite(self, token):
        context = {"REGISTER_LINK": settings.BASE_FRONTEND_URL + "/register/" + token}
        self.sendmail(context=context, html_template=settings.EMAIL_HTML, txt_template=settings.EMAIL_TXT)

    def send_password_recover(self, token):
        context = {
            'current_user': token.user,
            'username': token.user.username,
            'email': token.user.email,
            'reset_password_url': "{}?token={}".format(
                settings.BASE_FRONTEND_URL + reverse('password_reset:reset-password-request'),
                token.key)
        }
        self.sendmail(context=context, html_template=settings.PASSWORD_RESET_HTML,
                      txt_template=settings.PASSWORD_RESET_TXT)

    def send_keydoc(self, author_name, doc):
        context = {
            "requester": author_name,
            "request_date": datetime.now().strftime("%Y-%m-%d, %H:%M ") + settings.TIME_ZONE
        }
        self.sendmail(context=context, html_template=settings.KEYDOC_HTML,
                      txt_template=settings.KEYDOC_TXT, attachment_path=doc)
