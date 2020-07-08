from celery import shared_task

from programs.models import Program
from programs.services.processing.ProcessingService import ProcessingService


# TODO: Pass the PK and get the program, service gets simpler that way
@shared_task
def process_audio(uploaded_file_path, uploader, email, normalized_program_name, emission_date, weekday, already_normalized,
                  adjust_duration):
    service = ProcessingService(path=uploaded_file_path, emission_date=emission_date, normalized_program_name=normalized_program_name,
                                author_name=uploader, email=email, weekday=weekday, already_normalized=already_normalized,
                                adjust_duration=adjust_duration)
    service.process()
    return True
