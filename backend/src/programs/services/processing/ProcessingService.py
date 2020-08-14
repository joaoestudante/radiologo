import os
from datetime import datetime
from traceback import print_tb

from django.conf import settings
from pydub.utils import which, mediainfo

from exceptions.radiologoexception import FileBeingProcessedException
from pydub import AudioSegment

from programs.models import Program
from programs.services.RemoteService import RemoteService
from programs.services.processing.FileChecker import FileChecker, IrrecoverableProblemsException
from radiologo.emailservice import EmailService


class ProcessingService:
    def __init__(self, path: str, program_pk: int, emission_date: str, author_name: str, email: str):
        self.uploaded_file_path = path
        self.program = Program.objects.get(pk=program_pk)
        self.normalized_program_name = self.program.normalized_name()
        self.author_name = author_name
        self.email = email
        self.emission_date = emission_date
        self.already_normalized = self.program.comes_normalized
        self.adjust_duration = not self.program.ignore_duration_adjustment
        self.output_file_name = self.program.get_filename_for_date(emission_date)
        self.output_file_path = os.path.dirname(self.uploaded_file_path) + "/" + self.output_file_name

        self.collected_problems = []
        self.collected_warnings = []

        self.remote_service = RemoteService()

        display_emission_date = emission_date[:4] + "-" + emission_date[4:6] + "-" + emission_date[6:]
        self.email_service = EmailService(
            subject="Relatório de envio do programa {} para o dia {}".format(self.normalized_program_name,
                                                                             display_emission_date),
            to=email)

        # Settings
        self.min_sample_rate = '44100'  # Hz
        self.min_bitrate = '128'  # kbps
        self.recommended_bitrate = '192'  # kbps
        self.channels = '2'  # stereo
        self.maximum_level = -6  # DB (AudioSegment dBFS property)
        self.allowed_durations = [3, 10, 28, 57, 117]  # 3, 10 is for development testing
        self.tags = {"artist": "",
                     "album": "",
                     "title": "",
                     "date": ""}

    def process(self):
        print("Processing started for: " + self.normalized_program_name)
        try:
            AudioSegment.converter = which('ffmpeg')
            uploaded_file = AudioSegment.from_file(self.uploaded_file_path, self.uploaded_file_path[-3:])
            info = mediainfo(self.uploaded_file_path)

            checker = FileChecker(file_path=self.uploaded_file_path, durations=self.allowed_durations,
                                  min_sample_rate=self.min_sample_rate, min_bitrate=self.min_bitrate,
                                  recommended_bitrate=self.recommended_bitrate, info=info,
                                  do_normalization=not self.already_normalized, 
                                  do_check_duration=self.adjust_duration)
            print("\t* Checking file...")
            parameters = checker.run_checks()

            self.build_tags(info)

            print("\t* Exporting...")
            uploaded_file.export(self.output_file_path,
                                 bitrate=self.recommended_bitrate + "k",
                                 tags=self.tags,
                                 parameters=parameters)

            print("\t* Uploading...")
            self.remote_service.upload_program_to_archive(self.normalized_program_name, self.output_file_path)
            if self.emission_date == datetime.now().strftime("%Y%m%d"):
                self.remote_service.upload_program_to_emission(self.output_file_path)

            print("\t* Sending email...")
            self.email_service.send_upload_accepted(checker=checker, program_name=self.normalized_program_name,
                                                    emission_date=self.emission_date)

        except IrrecoverableProblemsException:
            print("\t\t- File has bad problems, sending email...")
            self.email_service.send_upload_rejected(checker=checker, program_name=self.normalized_program_name,
                                                    emission_date=self.emission_date)

        except Exception as e:
            print("- Something unexpected happened, sending email...")
            print(e)
            print_tb(e.__traceback__)
            self.email_service.send_upload_failed(program_name=self.normalized_program_name,
                                                  emission_date=self.emission_date)

        finally:
            print("\t* Cleaning up...")
            self.cleanup()

    def build_tags(self, info):
        for tag in info.get("TAG", []):
            if tag in self.tags:  # Only retrieve the tags we want
                self.tags[tag] = info.get("TAG", None)[tag]

        if not self.tags["artist"]:
            self.tags["artist"] = self.author_name

        if not self.tags["album"]:
            self.tags["album"] = self.normalized_program_name

        if not self.tags["title"]:
            self.tags["title"] = self.output_file_name

        if not self.tags["date"]:
            self.tags["date"] = datetime.now().strftime("%Y")

    @staticmethod
    def save_file(uploaded_file, emission_date: str, program: Program):
        uploaded_file.name = "uploaded_" + uploaded_file.name
        uploaded_file_path = settings.FILE_UPLOAD_DIR + uploaded_file.name
        output_file_path = settings.FILE_UPLOAD_DIR + program.get_filename_for_date(emission_date)

        if os.path.isfile(uploaded_file_path) or os.path.isfile(output_file_path):
            raise FileBeingProcessedException

        upload_service = RemoteService()
        upload_service.check_file_for_date(program.normalized_name(), emission_date)

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
