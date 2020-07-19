import json
from datetime import datetime

from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from programs.models import Program, Slot
from programs.serializers import ProgramSerializer
from programs.services.ProgramService import ProgramService
from programs.services.SlotService import SlotService
from users.models import CustomUser
from users.services.UserService import UserService


class ListCreateProgramsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        program_service = ProgramService()
        p1 = program_service.create_program(authors=list(get_user_model().objects.all()), name="P1", max_duration=57)
        p2 = program_service.create_program(authors=list(get_user_model().objects.all()), name="P2")
        p3 = program_service.create_program(authors=list(get_user_model().objects.all()), name="P3")

        slot_service = SlotService()
        midnight = datetime.strptime("00:03", "%H:%M")
        slot_service.create_slot(1, midnight, p1, False)
        slot_service.create_slot(2, midnight, p2, False)
        slot_service.create_slot(3, midnight, p3, False)

        logged_in_user = CustomUser(email="logged@in.com",
                                    password="password",
                                    author_name="aaa",
                                    full_name="aaaa", id_type="CC",
                                    id_number="123",
                                    ist_student_options="Y", phone="1234",
                                    role="DI")
        logged_in_user.save()
        token = RefreshToken.for_user(logged_in_user).access_token
        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(token)
        }

    def test_listing(self):
        response = self.client.get("/programs/", format='json', **self.auth_headers)
        programs = Program.objects.all()
        serialized_programs = ProgramSerializer(programs, many=True)
        self.assertEqual(response.data, serialized_programs.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_new_creation(self):
        response = self.client.post("/programs/", data=json.dumps({
            "name": "P4",
            "max_duration": 28,
            "slot_set": [
                {
                    "iso_weekday": "4",
                    "time": "00:03",
                    "is_rerun":False
                }
            ],
            "authors": []
        }),
                                    content_type='application/json', **self.auth_headers)

        self.assertEqual(Program.objects.count(), 4)
        serialized_p4 = ProgramSerializer(Program.objects.get(name="P4"))
        self.assertEqual(response.data, serialized_p4.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_creation(self):
        response = self.client.post("/programs/", data=json.dumps({
            "name": "P3",
            "max_duration": 28,
            "slot_set": [
                {
                    "iso_weekday": "4",
                    "time": "00:03"
                }
            ],
            "authors": []
        }),
                                    content_type='application/json', **self.auth_headers)
        self.assertEqual(Program.objects.count(), 3)
        self.assertEqual(Slot.objects.count(), 3)
        # Also assert exception error

    def test_same_slot_creation(self):
        response = self.client.post("/programs/", data=json.dumps({
            "name": "P4",
            "max_duration": 28,
            "slot_set": [
                {
                    "iso_weekday": "1",
                    "time": "00:03"
                }
            ],
            "authors": []
        }),

                                    content_type='application/json', **self.auth_headers)
        self.assertEqual(Program.objects.count(), 3)
        self.assertEqual(Slot.objects.count(), 3)

    def test_conflicting_slot_creation(self):
        response = self.client.post("/programs/", data=json.dumps({
            "name": "P4",
            "max_duration": 28,
            "slot_set": [
                {
                    "iso_weekday": "1",
                    "time": "00:32"
                }
            ],
            "authors": []
        }),

                                    content_type='application/json', **self.auth_headers)
        self.assertEqual(Program.objects.count(), 3)
        self.assertEqual(Slot.objects.count(), 3)


class GetUpdateDeleteProgramsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        program_service = ProgramService()
        self.p1 = program_service.create_program(authors=list(get_user_model().objects.all()), name="P1",
                                                 max_duration=57)
        self.p2 = program_service.create_program(authors=list(get_user_model().objects.all()), name="P2")
        self.p3 = program_service.create_program(authors=list(get_user_model().objects.all()), name="P3")

        slot_service = SlotService()
        midnight = datetime.strptime("00:03", "%H:%M")
        slot_service.create_slot(1, midnight, self.p1, False)
        slot_service.create_slot(2, midnight, self.p2, False)
        slot_service.create_slot(3, midnight, self.p3, False)

        user_service = UserService()
        user_service.create_user(email="a@asd.com", password="password", author_name="A1",
                                                      full_name="AA1", id_type="CC",
                                                      id_number="123456789",
                                                      ist_student_options="Y", phone="999999999")
        logged_in_user = CustomUser(email="logged@in.com",
                                    password="password",
                                    author_name="aaa",
                                    full_name="aaaa", id_type="CC",
                                    id_number="123",
                                    ist_student_options="Y", phone="1234",
                                    role="DI")
        logged_in_user.save()
        token = RefreshToken.for_user(logged_in_user).access_token
        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + str(token)
        }


    def test_existing_program(self):
        response = self.client.get("/programs/1/", format='json', **self.auth_headers)
        serialized_program = ProgramSerializer(self.p1)
        self.assertEqual(response.data, serialized_program.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_existing_program(self):
        response = self.client.get("/programs/99/", format='json', **self.auth_headers)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Not found.', code='not_found')})

    def test_update_program(self):
        response = self.client.patch("/programs/1/", data=json.dumps({
            "max_duration": 28,
            "slot_set": [{
                "iso_weekday": "1",
                "time": "00:32"
            }],
            "authors": [
                {
                    "id":1,
                    "author_name":"doesn't matter"
                }
            ]
        }), content_type='application/json', **self.auth_headers)

        program = Program.objects.get(pk=1)
        author = get_user_model().objects.get(pk=1)

        self.assertEqual(program.max_duration, 28)
        Slot.objects.get(weekday=Slot.iso_to_custom_format(1), time="00:32") # no exception here
        self.assertRaises(Slot.DoesNotExist, Slot.objects.get, weekday=Slot.iso_to_custom_format(1), time="00:03")
        self.assertEqual(list(program.authors.all()), [author])
        self.assertEqual(list(author.program_set.all()), [program])

    def test_delete_program(self):
        response = self.client.delete("/programs/1/", **self.auth_headers)
        self.assertEqual(Program.objects.count(), 2)
        self.assertEqual(Slot.objects.count(), 2)
        self.assertRaises(Program.DoesNotExist, Program.objects.get, pk=1)