from datetime import datetime

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
            raise InvalidDateFormatForEmissionException
        if slot_set.all().count() > 1:
            isoweekday = emission_date_obj.isoweekday()
            if isoweekday not in enabled_days:
                raise InvalidDateForEmissionException

            weekday = slot_set.filter(weekday=Slot.iso_to_custom_format(isoweekday))[
                0].weekday
        else:
            weekday = ""
        return weekday