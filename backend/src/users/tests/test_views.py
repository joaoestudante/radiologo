import json
import re
import struct

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from django.core import mail, signing
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Invite, CustomUser
from users.serializers.InviteSerializer import InviteSerializer
from users.services.UserService import UserService


class InviteAcceptTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.email_1 = "joao@asd.com"
        self.author_name_1 = "João"
        self.full_name_1 = "João Maria"
        self.id_number_1 = "111111111"
        self.ist_1 = "S"
        self.phone_1 = "123456789"
        self.id_type = "CC"

        self.user_service = UserService()

        logged_in_user = CustomUser(email="logged@in.com",
                                    password="password",
                                    author_name="aaa",
                                    full_name="aaaa", id_type=self.id_type,
                                    id_number="123",
                                    ist_student_options=self.ist_1, phone="1234",
                                    department="AD", role="DI")
        logged_in_user.save()
        token = RefreshToken.for_user(logged_in_user).access_token
        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(token)
        }


    def test_accept(self):
        author_1 = self.user_service.create_user(email=self.email_1,
                                                 author_name=self.author_name_1,
                                                 full_name=self.full_name_1, id_type=self.id_type,
                                                 id_number=self.id_number_1,
                                                 ist_student_options=self.ist_1, phone=self.phone_1)
        self.assertEquals(author_1.check_password(""), False)
        token = re.findall("register/[a-zA-Z0-9:/\-_]+", mail.outbox[0].body)[0].replace('register/', '')
        self.client.post('/users/register/' + token + "/", data=json.dumps({"password": "thisismypassword123"}),
                         content_type='application/json')
        user = get_user_model().objects.get(email=self.email_1)
        self.assertTrue(user.is_registered)
        self.assertTrue(user.check_password("thisismypassword123"))

    def test_resend(self):
        # Send an invite, resend the invite, make sure the first one is unusable and the second one works

        author_1 = self.user_service.create_user(email=self.email_1,
                                                 author_name=self.author_name_1,
                                                 full_name=self.full_name_1, id_type=self.id_type,
                                                 id_number=self.id_number_1,
                                                 ist_student_options=self.ist_1, phone=self.phone_1)

        invites_list = self.client.get('/users/invites/', format='json', **self.auth_headers)
        author_name = dict(invites_list.data[0])["invited_user_author_name"]
        user = get_user_model().objects.get(author_name=author_name)
        invite = Invite.objects.get(invited_user=user)

        self.assertFalse(invite.accepted)
        self.assertEqual(len(mail.outbox), 1)
        first_token = invite.sent_token

        self.client.post('/users/invites/resend/', data=json.dumps({"invited_user_author_name": author_name}),
                         content_type='application/json', **self.auth_headers)
        self.assertEqual(len(mail.outbox), 2)

        # Use the first token, should error out
        invite = Invite.objects.get(pk=1)
        second_token = invite.sent_token
        self.client.post('/users/register/' + first_token, data=json.dumps({"password": "thisismypassword1234"}),
                         content_type='application/json')
        # Tried to use the first token, password was not set
        user = get_user_model().objects.get(author_name=author_name)
        self.assertFalse(user.check_password("password123"))

        # Use the second token, invite is accepted and password is set
        self.client.post('/users/register/' + second_token + "/", data=json.dumps({"password": "thisismypassword1234"}),
                         content_type='application/json')
        invite = Invite.objects.get(pk=1)
        self.assertTrue(invite.accepted)
        user = get_user_model().objects.get(author_name=author_name)
        self.assertTrue(user.check_password("thisismypassword1234"))
