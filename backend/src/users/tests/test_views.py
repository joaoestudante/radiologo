import json
import re
import struct

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from django.core import mail, signing

from users.models import Invite
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
        user = get_user_model().objects.get(pk=1)
        self.assertTrue(user.is_registered)
        self.assertEquals(user.check_password("thisismypassword123"), True)