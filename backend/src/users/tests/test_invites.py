from django.conf import settings
from django.test import TestCase
from django.core import mail

from ..models import CustomUser
from ..services.UserService import UserService
from ..models.invite import Invite


class InvitesTest(TestCase):
    def setUp(self):
        self.email_1 = "joao@asd.com"
        self.author_name_1 = "João"
        self.full_name_1 = "João Maria"
        self.id_number_1 = "111111111"
        self.ist_1 = "S"
        self.phone_1 = "123456789"
        self.password = "password"
        self.id_type = "CC"

        self.user_service = UserService()

    def test_invite_sent(self):
        author_1 = self.user_service.create_user(email=self.email_1, password=self.password,
                                                 author_name=self.author_name_1,
                                                 full_name=self.full_name_1, id_type=self.id_type,
                                                 id_number=self.id_number_1,
                                                 ist_student_options=self.ist_1, phone=self.phone_1)
        all_invites = Invite.objects.all()
        invite = all_invites[0]
        self.assertEqual(all_invites.count(), 1)
        self.assertEqual(invite.invited_user, author_1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Bem vindo à Rádio Zero")
        self.assertIn(settings.BASE_FRONTEND_URL + "register/" + invite.sent_token, mail.outbox[0].body)

    def test_not_sent_if_inactive(self):
        author_1 = self.user_service.create_user(email=self.email_1,
                                                 author_name=self.author_name_1,
                                                 full_name=self.full_name_1, id_type=self.id_type,
                                                 id_number=self.id_number_1,
                                                 ist_student_options=self.ist_1, phone=self.phone_1, is_active=False)

        self.assertEqual(Invite.objects.count(), 0)
        self.assertEqual(CustomUser.objects.count(), 1)