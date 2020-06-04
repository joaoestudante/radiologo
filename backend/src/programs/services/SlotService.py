from datetime import datetime

from ..models import Slot
from ..models.slot import allowed_slots
from exceptions.radiologoexception import RadiologoException


class SlotService:
    def __init__(self):
        pass

    def create_slot(self, iso_weekday, time, program_object):
        self.check_occupied_slot(iso_weekday, time)
        self.check_next_slots(iso_weekday, time, program_object)
        self.check_prev_slots(iso_weekday, time, program_object)
        s = Slot(weekday=iso_weekday, time=time, program=program_object)
        s.save()
        return s

    def check_occupied_slot(self, iso_weekday, time):
        matching_slots = Slot.objects.filter(weekday=Slot.iso_to_custom_format(iso_weekday),
                                             time=time).count()
        if matching_slots != 0:
            raise RadiologoException()
            # "There is already a program at the specified time"

    def check_next_slots(self, iso_weekday, time, program_object):
        day_slots = Slot.objects.filter(weekday=Slot.iso_to_custom_format(iso_weekday),
                                        time__lte=time.strftime("%H:%M"))

        for slot in day_slots:
            if time.strftime("%H:%M") in slot.internal_slots_occupied():
                raise RadiologoException()
            # "Slot cannot be registered: a program starting at " + " [" + " mins] would conflict with " + program_object.name + ", which starts at " + slot.time

    def check_prev_slots(self, iso_weekday, time, program_object):
        day_slots = Slot.objects.filter(weekday=Slot.iso_to_custom_format(iso_weekday),
                                        time__gte=time.strftime("%H:%M"))

        for slot in day_slots:
            if slot.time.strftime("%H:%M") in Slot.slots_occupied(program_object.max_duration, time):
                raise RadiologoException()