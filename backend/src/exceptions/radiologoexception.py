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


class InvalidDateFormatForEmissionException(RadiologoException):
    status_code = 400
    default_detail = 'This date does not have the required format for emissions (should be YYYYMMDD)'
    default_code = 'bad_date_format_emission'


class InvalidDateForEmissionException(RadiologoException):
    status_code = 400
    default_detail = 'The date chosen does not belong to the program\'s authorized emission days.'
    default_code = 'forbidden_date'


class FileBeingProcessedException(RadiologoException):
    status_code = 400
    default_detail = 'The file you are trying to upload is currently being processed. Try again later if the processing fails.'
    default_code = 'file_in_processing'


class FileAlreadyUploadedException(RadiologoException):
    status_code = 400
    default_detail = 'There is already a file for the requested date at the archive. Delete the file in the archive first before trying to upload a new one.'
    default_code = 'file_already_uploaded'


class FileNotDeletedException(RadiologoException):
    status_code = 400
    default_detail = 'The file could not be deleted in the archive due to an unknown problem. Contact us to request a manual file deletion.'
    default_code = 'file_not_deleted'


class FileDoesNotExistException(RadiologoException):
    status_code = 400
    default_detail = 'There was no uploaded file found for the requested date. Contact us if you believe this is an error.'
    default_code = 'file_does_not_exist'
