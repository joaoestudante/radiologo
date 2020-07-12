from django.test import TestCase
from datetime import datetime
from ..models import Program
from ..services.SlotService import SlotService

import exceptions.radiologoexception as re


class SlotTest(TestCase):
    def setUp(self):
        self.slot_service = SlotService()

        self.program_28 = Program(pk=1, name="Program28", max_duration=28)
        self.program_28.save()
        self.program_57 = Program(pk=2, name="Program57", max_duration=57)
        self.program_57.save()
        self.program_117 = Program(pk=3, name="Program117", max_duration=117)
        self.program_117.save()

    def test_creation(self):
        # Monday is 1 in ISO and 2 in our format
        slot = self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("00:03", "%H:%M"),
                                             program_object=self.program_28, is_rerun=False)
        self.assertEqual(2, slot.weekday)
        self.assertEqual(1, slot.iso_weekday)
        self.assertEqual(0, slot.time.hour)
        self.assertEqual(3, slot.time.minute)
        self.assertEqual(self.program_28, slot.program)

    # Tests for slots occupied AFTER the initial program slot:

    def test_repeated_creation(self):  # A different program can't be associated to the same slot
        self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("00:03", "%H:%M"),
                                      program_object=self.program_28, is_rerun=False)

        self.assertRaises(re.RadiologoException, self.slot_service.create_slot, iso_weekday=1,
                          time=datetime.strptime("00:03", "%H:%M"),
                          program_object=self.program_57, is_rerun=False)

    def test_program_forward_spacing_28(self):
        self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("00:03", "%H:%M"),
                                      program_object=self.program_28, is_rerun=False)

        self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("00:32", "%H:%M"),
                                      program_object=self.program_57, is_rerun=False)

    def test_program_forward_spacing_57(self):  # A 57 minute program occupies its slot and the next
        self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("00:03", "%H:%M"),
                                      program_object=self.program_57, is_rerun=False)

        self.assertRaises(re.RadiologoException, self.slot_service.create_slot, iso_weekday=1,
                          time=datetime.strptime("00:32", "%H:%M"),
                          program_object=self.program_28, is_rerun=False)
        self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("01:03", "%H:%M"),
                                      program_object=self.program_28, is_rerun=False)

    def test_program_forward_spacing_117(self):  # a 117 minute program occupies its slot, and the next 3
        self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("00:03", "%H:%M"),
                                      program_object=self.program_117, is_rerun=False)

        self.assertRaises(re.RadiologoException, self.slot_service.create_slot, iso_weekday=1,
                          time=datetime.strptime("00:32", "%H:%M"),
                          program_object=self.program_28, is_rerun=False)
        self.assertRaises(re.RadiologoException, self.slot_service.create_slot, iso_weekday=1,
                          time=datetime.strptime("01:03", "%H:%M"),
                          program_object=self.program_28, is_rerun=False)
        self.assertRaises(re.RadiologoException, self.slot_service.create_slot, iso_weekday=1,
                          time=datetime.strptime("01:32", "%H:%M"),
                          program_object=self.program_28, is_rerun=False)
        self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("02:03", "%H:%M"),
                                      program_object=self.program_28, is_rerun=False)  # all good here

    # Tests for slots occupied AFTER an initial slot and BEFORE another slot:

    def test_program_back_spacing_28(self):
        self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("23:32", "%H:%M"),
                                      program_object=self.program_57, is_rerun=False)

        self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("23:03", "%H:%M"),
                                      program_object=self.program_28, is_rerun=False)

    def test_program_back_spacing_57(self):
        self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("23:32", "%H:%M"),
                                      program_object=self.program_28, is_rerun=False)

        self.assertRaises(re.RadiologoException, self.slot_service.create_slot, iso_weekday=1,
                          time=datetime.strptime("23:03", "%H:%M"),
                          program_object=self.program_57, is_rerun=False)
        self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("22:32", "%H:%M"),
                                      program_object=self.program_57, is_rerun=False)

    def test_program_back_spacing_117(self):
        self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("23:32", "%H:%M"),
                                      program_object=self.program_28, is_rerun=False)

        self.assertRaises(re.RadiologoException, self.slot_service.create_slot, iso_weekday=1,
                          time=datetime.strptime("23:03", "%H:%M"),
                          program_object=self.program_117, is_rerun=False)
        self.assertRaises(re.RadiologoException, self.slot_service.create_slot, iso_weekday=1,
                          time=datetime.strptime("22:32", "%H:%M"),
                          program_object=self.program_117, is_rerun=False)
        self.assertRaises(re.RadiologoException, self.slot_service.create_slot, iso_weekday=1,
                          time=datetime.strptime("22:03", "%H:%M"),
                          program_object=self.program_117, is_rerun=False)
        self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("21:32", "%H:%M"),
                                      program_object=self.program_117, is_rerun=False)

    def test_next_available_wrap(self):
        slot_1 = self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("23:32", "%H:%M"),
                                               program_object=self.program_28, is_rerun=False)
        self.assertEqual(slot_1.internal_next_available(), "00:03")

    def test_next_available_28(self):
        slot_1 = self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("00:03", "%H:%M"),
                                               program_object=self.program_28, is_rerun=False)
        self.assertEqual(slot_1.internal_next_available(), "00:32")

    def test_next_available_57(self):
        slot_1 = self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("00:03", "%H:%M"),
                                               program_object=self.program_57, is_rerun=False)
        self.assertEqual(slot_1.internal_next_available(), "01:03")

    def test_next_available_117(self):
        slot_1 = self.slot_service.create_slot(iso_weekday=1, time=datetime.strptime("00:03", "%H:%M"),
                                               program_object=self.program_117, is_rerun=False)
        self.assertEqual(slot_1.internal_next_available(), "02:03")
