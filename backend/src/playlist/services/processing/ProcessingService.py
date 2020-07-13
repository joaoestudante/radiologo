import os
from datetime import datetime
from traceback import print_tb

from django.conf import settings
from pydub.utils import which, mediainfo

from exceptions.radiologoexception import FileBeingProcessedException
from pydub import AudioSegment

from playlist.services.RemoteService import RemoteService
from programs.services.processing.FileChecker import FileChecker, IrrecoverableProblemsException
#uses the FileChecker from programs, consider putting in more general Radiologo 

class ProcessingService:
    def __init__(self, path: str, artist: str, title: str):
        self.title = title
        self.artist = artist

        self.output_file_name = artist + " - " + title + ".mp3"

        self.uploaded_file_path = path

        self.output_file_path = os.path.dirname(self.uploaded_file_path) + "/" + self.output_file_name

        self.collected_problems = []
        self.collected_warnings = []

        self.remote_service = RemoteService()

        # Settings
        self.min_sample_rate = '44100'  # Hz
        # Bitrate requirements higher for music
        self.min_bitrate = '256'  # kbps
        self.recommended_bitrate = '312'  # kbps
        self.channels = '2'  # stereo
        self.maximum_level = -6  # DB (AudioSegment dBFS property)
        self.tags = {"artist": "",
                     "title": ""}

    def process(self):
        print("[Playlist] Processing started for: " + self.output_file_name)
        try:
            AudioSegment.converter = which('ffmpeg')
            uploaded_file = AudioSegment.from_file(self.uploaded_file_path, self.uploaded_file_path[-3:])
            info = mediainfo(self.uploaded_file_path)
            
            self.allowed_durations = float(info['duration']) / 60 #Music of all durations is permitted

            checker = FileChecker(file_path=self.uploaded_file_path, durations=self.allowed_durations,
                                  min_sample_rate=self.min_sample_rate, min_bitrate=self.min_bitrate,
                                  recommended_bitrate=self.recommended_bitrate, info=info,
                                  do_normalization=True)
            print("\t* Checking file...")
            parameters = checker.run_checks()

            self.build_tags(info)

            print("\t* Exporting...")
            uploaded_file.export(self.output_file_path,
                                 bitrate=self.recommended_bitrate + "k",
                                 tags=self.tags,
                                 parameters=parameters)

            print("\t* Uploading...")
            self.remote_service.upload_track_to_playlist(self.output_file_name, self.output_file_path)

        finally:
            print("\t* Cleaning up...")
            self.cleanup()

    def build_tags(self, info):
        for tag in info.get("TAG", []):
            self.tags[tag] = info.get("TAG", None)[tag]

        self.tags["artist"] = self.artist
        self.tags["title"] = self.title

    @staticmethod
    def save_file(uploaded_file, title: str, artist: str):
        uploaded_file.name = "uploaded_" + uploaded_file.name
        uploaded_file_path = settings.FILE_UPLOAD_DIR + uploaded_file.name
        output_file_name = artist + " - " + title + ".mp3"
        output_file_path = settings.FILE_UPLOAD_DIR + output_file_name

        if os.path.isfile(uploaded_file_path) or os.path.isfile(output_file_path):
            raise FileBeingProcessedException

        upload_service = RemoteService()
        upload_service.check_track_exists(output_file_name)

        with open(uploaded_file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

    def cleanup(self):
        try:
            os.remove(self.output_file_path)
        except Exception as e:
            print("Error deleting generated file. Exception was:")
            print(e)

        try:
            os.remove(self.uploaded_file_path)
        except Exception as e:
            print("Error deleting uploaded file. Exception was:")
            print(e)
