from celery import shared_task

from programs.models import Program
from programs.services.processing.ProcessingService import ProcessingService
from programs.services.rss_upload.FeedService import FeedService

# TODO: Pass the PK and get the program, service gets simpler that way
@shared_task
def process_audio(uploaded_file_path, program_pk, uploader, email, emission_date):
    service = ProcessingService(path=uploaded_file_path, program_pk=program_pk, emission_date=emission_date,
                                author_name=uploader, email=email)
    service.process()
    return True

# TODO: Schedule this task as recurring automatically for every program
@shared_task
def upload_from_feed(program_pk):
    service = FeedService(program_pk)
    service.download_last_episode() # Only runs if program.rss_feed_status = True
    return True
