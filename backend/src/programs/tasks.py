from celery import shared_task

from programs.models import Program
from programs.services.processing.ProcessingService import ProcessingService


# TODO: Pass the PK and get the program, service gets simpler that way
@shared_task
def process_audio(uploaded_file_path, program_pk, uploader, email, emission_date):
    service = ProcessingService(path=uploaded_file_path, program_pk=program_pk, emission_date=emission_date,
                                author_name=uploader, email=email)
    service.process()
    return True
