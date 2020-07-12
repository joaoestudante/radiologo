from datetime import datetime

from ..models import Slot
from ..models.slot import allowed_slots
from exceptions.radiologoexception import RadiologoException, StartingTimeConflictException, \
    SlotDurationConflictException
from ..models import Program


class SlotService:
    def __init__(self):
        pass

    def create_slot(self, iso_weekday: int, time: datetime.time, program_object: Program, is_rerun:bool):
        self.check_occupied_slot(iso_weekday, time)
        self.check_next_slots(iso_weekday, time, program_object)
        self.check_prev_slots(iso_weekday, time, program_object)
        s = Slot(weekday=iso_weekday, time=time, is_rerun=is_rerun, program=program_object)
        s.save()
        return s

    def check_occupied_slot(self, iso_weekday, time):
        matching_slots = Slot.objects.filter(weekday=Slot.iso_to_custom_format(iso_weekday),
                                             time=time).count()
        if matching_slots != 0:
            raise StartingTimeConflictException("There is already a program at the specified time")

    def check_next_slots(self, iso_weekday, time, program_object):
        day_slots = Slot.objects.filter(weekday=Slot.iso_to_custom_format(iso_weekday),
                                        time__lte=time.strftime("%H:%M"))

        for slot in day_slots:
            if time.strftime("%H:%M") in slot.internal_slots_occupied():
                raise SlotDurationConflictException(
                    detail="'{}' wants to start at {} and would conflict with {} starting "
                           "at {}. Try starting it at {}.".format(
                        program_object.name,
                        time.strftime("%H:%M"),
                        slot.program.name,
                        slot.time.strftime("%H:%M"),
                        slot.internal_next_available()))

    def check_prev_slots(self, iso_weekday, time, program_object):
        day_slots = Slot.objects.filter(weekday=Slot.iso_to_custom_format(iso_weekday),
                                        time__gte=time.strftime("%H:%M"))

        for slot in day_slots:
            if slot.time.strftime("%H:%M") in Slot.slots_occupied(program_object.max_duration, time):
                raise SlotDurationConflictException(
                    detail="'{}' wants to start at {} and would conflict with {} starting at {}.".format(
                        program_object.name,
                        time.strftime("%H:%M"),
                        slot.program.name,
                        slot.time.strftime("%H:%M")))

    def occupied_slots_in_day(self, iso_weekday) -> tuple:
        total_times = []
        for slot in Slot.objects.filter(weekday=Slot.iso_to_custom_format(iso_weekday)):
            total_times.extend(slot.internal_slots_occupied())
        return tuple(total_times)

    def occupied_slots_in_week(self) -> dict:
        result = {}
        for i in range(1, 8):
            result[i] = self.occupied_slots_in_day(i)
        return result
