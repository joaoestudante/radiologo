from datetime import date, timedelta

from celery import shared_task

from programs.models import Program
from programs.services.RemoteService import RemoteService
from programs.services.IcecastService import IcecastService

@shared_task
def process_audio(uploaded_file_path, program_pk, uploader, email, emission_date):
    from programs.services.processing.ProcessingService import ProcessingService

    service = ProcessingService(path=uploaded_file_path, program_pk=program_pk, emission_date=emission_date,
                                author_name=uploader, email=email)
    service.process()
    return True


# TODO: Schedule this task as recurring automatically for every program
@shared_task
def upload_from_feed():
    from programs.services.rss_upload.FeedService import FeedService
    active_rss = Program.objects.filter(state='A', rss_feed_status=True)
    for program in active_rss:
        service = FeedService(program.pk)
        service.download_last_episode()
    return True


@shared_task
def do_alignment():
    active_programs = Program.objects.filter(state='A')
    tomorrow = date.today() + timedelta(days=1)
    remote_service = RemoteService()
    for program in active_programs:
        if tomorrow.isoweekday() in program.enabled_days:
            remote_service.move_from_archive_to_emission(program, tomorrow)
    return True

@shared_task
def update_listener_stats():
    return IcecastService.report_listener_count()

