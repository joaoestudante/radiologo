from django.test import TestCase
from ..models import Slot, Program
from users.models import CustomUser
from users.services.UserService import UserService
from ..services.ProgramService import ProgramService
from ..services.SlotService import SlotService

from datetime import datetime
import exceptions.radiologoexception as re


class ProgramTest(TestCase):
    def setUp(self):
        self.user_service = UserService()
        self.program_service = ProgramService()

        password = "1234"
        id_type = "CC"

        email_1 = "joao@asd.com"
        author_name_1 = "João"
        full_name_1 = "João Maria"
        id_number_1 = "111111111"
        ist_1 = "S"
        phone_1 = "123456789"

        author_name_2 = "António"
        full_name_2 = "António Oliveira"
        email_2 = "antonio@asd.com"
        id_number_2 = "222222222"
        ist_2 = "N"
        phone_2 = "123456780"

        self.author_1 = self.user_service.create_user(email_1, password, author_name_1, full_name_1, id_type,
                                                      id_number_1,
                                                      ist_1, phone_1)
        self.author_2 = self.user_service.create_user(email_2, password, author_name_2, full_name_2, id_type,
                                                      id_number_2,
                                                      ist_2, phone_2)


        self.program_1_name = "AAA"
        self.program_2_name = "BBB"
        self.program_description = "Description"

    def test_basic_program_creation(self):
        p1 = self.program_service.create_program(name=self.program_1_name, description=self.program_description,
                                                 authors=[self.author_1], max_duration=28, comes_normalized=True)
        self.assertEqual(self.program_1_name, p1.name)
        self.assertEqual(self.program_description, p1.description)
        self.assertEqual(self.author_1, p1.authors.all()[0])
        self.assertEqual(28, p1.max_duration)
        self.assertEqual(True, p1.comes_normalized)

    def test_name_normalization(self):
        pass

    def test_disabled_days(self):
        pass

    def test_enabled_days(self):
        pass

    def test_next_emission_date(self):
        pass

    def test_free_slots(self):
        pass
