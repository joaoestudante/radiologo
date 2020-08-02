from datetime import datetime, date, timedelta

from exceptions.radiologoexception import InvalidDateFormatForEmissionException, InvalidDateForEmissionException
from ..models import Program, Slot


class ProgramService:
    def __init__(self):
        pass

    def create_program(self, authors, **extra_fields):
        p = Program(**extra_fields)
        p.save()
        p.authors.set(authors)
        return p

    def get_weekday_for_date(self, slot_set, enabled_days, date):
        try:
            emission_date_obj = datetime.strptime(date, "%Y%m%d")
        except ValueError:
            print("date is: " + date)
            raise InvalidDateFormatForEmissionException
        if slot_set.all().count() > 1:
            isoweekday = emission_date_obj.isoweekday()
            if isoweekday not in enabled_days:
                print("date is: " + date)
                raise InvalidDateForEmissionException

            weekday = slot_set.filter(weekday=Slot.iso_to_custom_format(isoweekday))[
                0].weekday
        else:
            weekday = ""
        return weekday

    def get_schedule(self):
        events = {"normal": [], "rerun": []}
        current_week_dates = []
        for i in range(1, 8):
            current_week_dates.append(
                (date.today() + timedelta(days=i - date.today().isoweekday())).isoformat()
            )
        for slot in Slot.objects.all():
            if slot.program.state == 'A':
                start = current_week_dates[slot.iso_weekday - 1] + " " + slot.time.strftime("%H:%M")
                end = current_week_dates[slot.iso_weekday - 1] + " " + slot.end_time()
                if slot.is_rerun:
                    events["rerun"].append(
                        {"name": slot.program.name + " - RE", "description": slot.program.description, "start": start,
                         "end": end})
                else:
                    events["normal"].append(
                        {"name": slot.program.name, "description": slot.program.description, "start": start,
                         "end": end})
        return events

    @staticmethod
    def get_week_slots_display(pk: int):
        disabled = {}
        possible_slots = Slot.allowed_slots()
        for i in range(1,8):
            disabled[i] = list(possible_slots)

        for program in Program.objects.filter(state__in=['A','H']).exclude(pk=pk):
            for day, slots in program.occupied_slots.items():
                for slot in slots:
                    disabled[day].remove(slot)

        return disabled
