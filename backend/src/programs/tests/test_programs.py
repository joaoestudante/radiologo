from django.test import TestCase
from ..models import Slot, Program
from users.models import CustomUser
from users.services.UserService import UserService
from ..services.ProgramService import ProgramService
from ..services.SlotService import SlotService

from datetime import datetime, timedelta, date
import exceptions.radiologoexception as re


class ProgramTest(TestCase):
    def setUp(self):
        self.user_service = UserService()
        self.program_service = ProgramService()
        self.slot_service = SlotService()

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
        names = ["!programa!", "#.^çÇÁàéóíõã"]
        normalized_names = ["programa", "ccaaeoioa"]

        for index, name in enumerate(names):
            p1 = self.program_service.create_program(name=name, description=self.program_description,
                                                     authors=[self.author_1], max_duration=28, comes_normalized=True)
            self.assertEqual(p1.normalized_name(), normalized_names[index])
            p1.delete()

    def test_disabled_days(self):
        p1 = self.program_service.create_program(name=self.program_1_name, description=self.program_description,
                                                 authors=[self.author_1], max_duration=28, comes_normalized=True)
        self.slot_service.create_slot(iso_weekday=2, time=datetime.strptime("00:03", "%H:%M"), program_object=p1)
        self.assertEqual(p1.disabled_days, (1, 3, 4, 5, 6, 7))

    def test_enabled_days(self):
        p1 = self.program_service.create_program(name=self.program_1_name, description=self.program_description,
                                                 authors=[self.author_1], max_duration=28, comes_normalized=True)
        self.slot_service.create_slot(iso_weekday=2, time=datetime.strptime("00:03", "%H:%M"), program_object=p1)
        self.slot_service.create_slot(iso_weekday=3, time=datetime.strptime("00:03", "%H:%M"), program_object=p1)

        self.assertEqual(p1.enabled_days, (2, 3))

    def test_next_emission_date(self):
        p1 = self.program_service.create_program(name=self.program_1_name, description=self.program_description,
                                                 authors=[self.author_1], max_duration=28, comes_normalized=True)
        tomorrow = date.today() + timedelta(days=1)
        self.slot_service.create_slot(iso_weekday=tomorrow.isoweekday(), time=datetime.strptime("00:03", "%H:%M"),
                                      program_object=p1)
        self.assertEqual(p1.next_emission_date(), tomorrow.isoformat())

    def test_occupied_slots_28(self):
        p1 = self.program_service.create_program(name=self.program_1_name, description=self.program_description,
                                                 authors=[self.author_1], max_duration=28, comes_normalized=True)
        self.slot_service.create_slot(iso_weekday=2, time=datetime.strptime("00:03", "%H:%M"), program_object=p1)
        self.slot_service.create_slot(iso_weekday=3, time=datetime.strptime("00:03", "%H:%M"), program_object=p1)
        self.assertEqual(p1.occupied_slots, {2: ("00:03",), 3: ("00:03",)})

    def test_occupied_slots_57(self):
        p1 = self.program_service.create_program(name=self.program_1_name, description=self.program_description,
                                                 authors=[self.author_1], max_duration=57, comes_normalized=True)
        self.slot_service.create_slot(iso_weekday=2, time=datetime.strptime("00:03", "%H:%M"), program_object=p1)
        self.slot_service.create_slot(iso_weekday=3, time=datetime.strptime("00:03", "%H:%M"), program_object=p1)
        self.assertEqual(p1.occupied_slots, {2: ("00:03", "00:32"), 3: ("00:03", "00:32")})

    def test_occupied_slots_117(self):
        p1 = self.program_service.create_program(name=self.program_1_name, description=self.program_description,
                                                 authors=[self.author_1], max_duration=117, comes_normalized=True)
        self.slot_service.create_slot(iso_weekday=2, time=datetime.strptime("00:03", "%H:%M"), program_object=p1)
        self.slot_service.create_slot(iso_weekday=7, time=datetime.strptime("00:03", "%H:%M"), program_object=p1)
        self.assertEqual(p1.occupied_slots,
                         {2: ("00:03", "00:32", "01:03", "01:32"), 7: ("00:03", "00:32", "01:03", "01:32")})

    def test_day_occupied_slots(self):
        p1 = self.program_service.create_program(name=self.program_1_name, description=self.program_description,
                                                 authors=[self.author_1], max_duration=57, comes_normalized=True)
        p2 = self.program_service.create_program(name=self.program_2_name, description=self.program_description,
                                                 authors=[self.author_1], max_duration=57, comes_normalized=True)
        self.slot_service.create_slot(iso_weekday=2, time=datetime.strptime("00:03", "%H:%M"), program_object=p1)
        self.slot_service.create_slot(iso_weekday=2, time=datetime.strptime("21:03", "%H:%M"), program_object=p2)

        self.assertEqual(self.slot_service.occupied_slots_in_day(iso_weekday=2),
                         ("00:03", "00:32", "21:03", "21:32"))

    def test_week_occupied_slots(self):
        p1 = self.program_service.create_program(name=self.program_1_name, description=self.program_description,
                                                 authors=[self.author_1], max_duration=57, comes_normalized=True)
        p2 = self.program_service.create_program(name=self.program_2_name, description=self.program_description,
                                                 authors=[self.author_1], max_duration=28, comes_normalized=True)
        p3 = self.program_service.create_program(name="asd", description=self.program_description,
                                                 authors=[self.author_1], max_duration=57, comes_normalized=True)
        self.slot_service.create_slot(iso_weekday=2, time=datetime.strptime("00:03", "%H:%M"), program_object=p1)
        self.slot_service.create_slot(iso_weekday=2, time=datetime.strptime("02:03", "%H:%M"), program_object=p2)
        self.slot_service.create_slot(iso_weekday=3, time=datetime.strptime("21:03", "%H:%M"), program_object=p3)
        self.assertEqual(self.slot_service.occupied_slots_in_week(),
                         {1: (),
                          2: ("00:03", "00:32", "02:03"),
                          3: ("21:03", "21:32"),
                          4: (),
                          5: (),
                          6: (),
                          7: ()})