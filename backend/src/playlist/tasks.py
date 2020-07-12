from datetime import date, timedelta

from celery import shared_task

@shared_task
def process_audio(uploaded_file_path, artist: str, title: str):
    from playlist.services.processing.ProcessingService import ProcessingService

    service = ProcessingService(path=uploaded_file_path, artist=artist, title=title)
    service.process()
    return True
