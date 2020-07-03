from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class EmailService:
    def __init__(self, subject, to):
        self.to = to
        self.subject = subject

    def sendmail(self, context, html_template, txt_template):
        email_html_message = render_to_string(html_template, context)
        email_plaintext_message = render_to_string(txt_template, context)
        msg = EmailMultiAlternatives(self.subject, email_plaintext_message, settings.EMAIL_HOST_USER, [self.to])
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()
        print(email_plaintext_message)

    def send_upload_rejected(self, checker, program_name, emission_date):
        context = {
            "problems": checker.problems,
            "program_name": program_name,
            "emission_date": emission_date[:4] + "-" + emission_date[4:6] + "-" + emission_date[6:],
        }
        self.sendmail(context=context, html_template=settings.UPLOAD_REJECT_HTML, txt_template=settings.UPLOAD_REJECT_TXT)


    def send_upload_accepted(self, checker, program_name, emission_date):
        context = {
            "warnings": checker.warnings,
            "program_name": program_name,
            "emission_date": emission_date[:4] + "-" + emission_date[4:6] + "-" + emission_date[6:],
        }
        self.sendmail(context=context, html_template=settings.UPLOAD_ACCEPT_HTML, txt_template=settings.UPLOAD_ACCEPT_TXT)

    def send_upload_failed(self, program_name, emission_date):
        context = {
            "program_name": program_name,
            "emission_date": emission_date[:4] + "-" + emission_date[4:6] + "-" + emission_date[6:],
        }
        self.sendmail(context=context, html_template=settings.UPLOAD_FAIL_HTML, txt_template=settings.UPLOAD_FAIL_TXT)

    def send_invite(self, subject, ):
        pass

    def send_password_recover(self):
        pass

    def send_keydoc(self):
        pass