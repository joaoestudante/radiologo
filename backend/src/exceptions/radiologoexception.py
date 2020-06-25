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

class BadInviteTokenException(RadiologoException):
    status_code = 400
    default_detail = 'Invalid link, make sure it is exactly the one sent to you.'
    default_code = 'invalid_link'

class InvalidTokenException(RadiologoException):
    status_code = 400
    default_detail = 'Expired link, you should have received an updated one.'
    default_code = 'invalid_token'

class ExpiredTokenException(RadiologoException):
    status_code = 400
    default_detail = 'Expired link. Please contact the Departamento de Programação to ask for a new one.'
    default_code = 'expired_token'

class InviteAlreadyAcceptedException(RadiologoException):
    status_code = 400
    default_detail = 'Registration has already been made.'
    default_code = 'already_registered'

class NoNewMembersForKeyDocException(RadiologoException):
    status_code = 400
    default_detail = 'There are no new members registered since the latest generated document.'
    default_code = 'no_new_members'