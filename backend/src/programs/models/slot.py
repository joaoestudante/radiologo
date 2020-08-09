from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import gettext_lazy as _

from .program import Program

# This is our own format - it is not a standard
# Monday[EN] = Segunda[PT] = "Second"[EN] = 2
WEEKDAYS = (
    ('1', _('Sunday')),
    ('2', _('Monday')),
    ('3', _('Tuesday')),
    ('4', _('Wednesday')),
    ('5', _('Thursday')),
    ('6', _('Friday')),
    ('7', _('Saturday')),
)

allowed_slots = ("00:03",
                 "00:32",
                 "01:03",
                 "01:32",
                 "02:03",
                 "02:32",
                 "03:03",
                 "03:32",
                 "04:03",
                 "04:32",
                 "05:03",
                 "05:32",
                 "06:03",
                 "06:32",
                 "07:03",
                 "07:32",
                 "08:03",
                 "08:32",
                 "09:03",
                 "09:32",
                 "10:03",
                 "10:32",
                 "11:03",
                 "11:32",
                 "12:03",
                 "12:32",
                 "13:03",
                 "13:32",
                 "14:03",
                 "14:32",
                 "15:03",
                 "15:32",
                 "16:03",
                 "16:32",
                 "17:03",
                 "17:32",
                 "18:03",
                 "18:32",
                 "19:03",
                 "19:32",
                 "20:03",
                 "20:32",
                 "21:03",
                 "21:32",
                 "22:03",
                 "22:32",
                 "23:03",
                 "23:32")


def slot_wraps(start_index: int, slots_occupied: int) -> bool:
    return start_index + slots_occupied >= len(allowed_slots)


class Slot(models.Model):
    weekday = models.CharField(max_length=15, choices=WEEKDAYS)
    time = models.TimeField()
    program = models.ForeignKey(to=Program, on_delete=models.CASCADE)
    is_rerun = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        if (kwargs):
            kwargs["weekday"] = self.iso_to_custom_format(int(kwargs['weekday']))

        super().__init__(*args, **kwargs)

    def __str__(self):
        if self.is_rerun:
            return self.get_weekday_display() + ", " + self.time.strftime("%H:%M") + " - (" + str(
                self.program) + ", rerun)"
        else:
            return self.get_weekday_display() + ", " + self.time.strftime("%H:%M") + " - (" + str(self.program) + ")"

    @staticmethod
    def iso_to_custom_format(iso: int):
        return iso % 7 + 1

    @property
    def iso_weekday(self):
        """
        1 -> 7
        2 -> 1
        3 -> 2
        4 -> 3
        5 -> 4
        6 -> 5
        7 -> 6
        """
        return [7, 1, 2, 3, 4, 5, 6][int(self.weekday) - 1]

    @staticmethod
    def next_available(duration: int, time: datetime.time) -> str:
        current_index = allowed_slots.index(time.strftime("%H:%M"))

        if duration == 28:
            if slot_wraps(current_index, 1):  # 28 mins occupies 1 slot
                return allowed_slots[(current_index + 1) - len(allowed_slots)]
            return allowed_slots[current_index + 1]

        if duration == 57:
            if slot_wraps(current_index, 2):  # 57 mins occupies 2 slots
                return allowed_slots[(current_index + 2) - len(allowed_slots)]
            return allowed_slots[current_index + 2]

        if duration == 117:
            if slot_wraps(current_index, 4):  # 117 mins occupies 4 slots
                return allowed_slots[(current_index + 4) - len(allowed_slots)]
            return allowed_slots[current_index + 4]

    def internal_next_available(self):
        return self.next_available(self.program.max_duration, self.time)

    @staticmethod
    def slots_occupied(duration: int, time: datetime.time) -> tuple:
        start_index = allowed_slots.index(time.strftime("%H:%M"))
        end_index = allowed_slots.index(Slot.next_available(duration, time))

        if end_index < start_index:
            slots = []
            for i in range(start_index, len(allowed_slots)):
                slots.append(allowed_slots[i])
            for i in range(0, end_index):
                slots.append(allowed_slots[i])
            return tuple(slots)

        elif end_index == start_index:
            return allowed_slots[start_index]

        else:
            return allowed_slots[start_index:end_index]

    def internal_slots_occupied(self):
        return self.slots_occupied(self.program.max_duration, self.time)

    def end_time(self):
        now = datetime.now()
        return (datetime(year=now.year, month=now.month, day=now.day, hour=self.time.hour,
                         minute=self.time.minute) + timedelta(
            minutes=self.program.max_duration)).strftime("%H:%M")
      
    def end_time_obj(self):
        now = datetime.now()
        return (datetime(year=now.year, month=now.month, day=now.day, hour=self.time.hour,
                         minute=self.time.minute) + timedelta(
            minutes=self.program.max_duration)).time()

    @staticmethod
    def allowed_slots():
        return allowed_slots
