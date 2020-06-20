from rest_framework.exceptions import APIException


class RadiologoException(APIException):
    pass

class StartingTimeConflictException(RadiologoException):
    status_code = 400
    default_detail = 'Could not register program for this starting time, conflicts with another.'
    default_code = 'start_slot_error'

class SlotDurationConflictException(RadiologoException):
    status_code = 400
    default_detail = 'Could not register program for this starting time, conflicts with another.'
    default_code = 'slot_conflict_error'