from celery import shared_task

from programs.services.ProcessingService import ProcessingService


@shared_task
def process_audio():
    service = ProcessingService()
    service.process()
    return True
