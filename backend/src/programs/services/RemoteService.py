import os
import re
import subprocess
from datetime import datetime, timedelta

import paramiko
import requests
from django.conf import settings
from django.http import StreamingHttpResponse

from exceptions.radiologoexception import FileAlreadyUploadedException, FileNotDeletedException, \
    FileDoesNotExistException, CouldNotConnectToServerException
from programs.models import Program

import collections


class RemoteService:
    def __init__(self):
        self.ssh_client = None
        self.ftp_client = None

    def check_file_for_date(self, program, emission_date):  # emission_date is YYYYMMDD
        potential_file = settings.ARCHIVE_SERVER_UPLOAD_DIRECTORY + program + "/" + program + emission_date + "*"

        self.open_ssh_archive()
        ftp_client = self.ssh_client.open_sftp()
        try:
            file = ftp_client.stat(potential_file)
            if file is not None:
                raise FileAlreadyUploadedException
        except IOError:
            pass  # Success

        return ftp_client

    def upload_program_to_archive(self, normalized_program_name, file_path):
        archive_folder = settings.ARCHIVE_SERVER_UPLOAD_DIRECTORY + normalized_program_name + "/"

        self.open_ssh_archive()
        ftp_client = self.ssh_client.open_sftp()
        try:
            ftp_client.chdir(archive_folder)
        except IOError:
            ftp_client.mkdir(archive_folder)

        ftp_client.put(file_path, archive_folder + os.path.basename(file_path))
        self.close_connections()
        return

    def upload_program_to_emission(self, file_path):
        short_filename = os.path.basename(file_path).replace(datetime.now().strftime("%Y%m%d"),
                                                             "")  # Maintains weekday info, if it exists
        emission_file_path = settings.UPLOAD_SERVER_UPLOAD_DIRECTORY + short_filename

        self.open_ssh_emission()
        ftp_client = self.ssh_client.open_sftp()
        ftp_client.put(file_path, emission_file_path)
        self.close_connections()
        return

    def download_archive_file(self, program: Program, emission_date: str):
        filename = program.get_filename_for_date(emission_date)
        archive_url = "http://{}".format(settings.ARCHIVE_SERVER_IP)
        session = requests.Session()
        session.auth = (settings.ARCHIVE_SERVER_USERNAME, settings.ARCHIVE_SERVER_PASSWORD)
        session.post(archive_url)

        r = session.get(archive_url + '/archive/' + program.normalized_name() + "/" + filename, stream=True)

        resp = StreamingHttpResponse(r.iter_content(8096))
        resp['headers'] = "X-Accel-Redirect"
        resp['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        resp['Accept-Ranges'] = 'bytes'
        resp['Content-Type'] = 'audio/mpeg'

        return resp

    def get_archive_contents(self, normalized_program_name):
        destination = "/srv/arquivo_sonoro/radiologo/"
        file_list = {}

        self.open_ssh_archive()
        ftp_client = self.ssh_client.open_sftp()

        try:
            ftp_client.chdir(destination + normalized_program_name)
            for file_name in ftp_client.listdir():
                compact_date = re.findall('\d{8,9}', file_name)[0]
                display_date = datetime.strptime(compact_date[:8], "%Y%m%d").strftime("%d/%m/%Y")
                file_list[display_date] = {
                    "file_date": compact_date,
                    "file_name": file_name}
            file_list = sorted(file_list.items(), key=lambda k: k[1]['file_date'], reverse=True)

        except IOError as e:
            pass
        finally:
            self.close_connections()
            return file_list

    def delete_archive_file(self, program, date):  # date is YYYYMMDDw (where w=weekday and is optional)
        file = settings.ARCHIVE_SERVER_UPLOAD_DIRECTORY + program.normalized_name() + "/" + program.get_filename_for_date(
            date)

        self.open_ssh_archive()
        ftp_client = self.ssh_client.open_sftp()

        try:
            ftp_client.remove(file)
        except IOError:
            raise FileDoesNotExistException

        try:
            ftp_client.stat(file)
            raise FileNotDeletedException
        except IOError:
            pass  # Success
        self.close_connections()
        return

    def get_archive_stats(self):
        # Uploaded/not uploaded in the latest 7 days
        self.open_ssh_archive()
        ftp_client = self.ssh_client.open_sftp()
        ftp_client.chdir(settings.ARCHIVE_SERVER_UPLOAD_DIRECTORY)

        stats = collections.defaultdict(self._default_stat_dict)

        active_programs = Program.objects.filter(state='A')
        for program in active_programs:
            for i in range(8):
                iteration_date = datetime.now() - timedelta(days=i)
                if iteration_date.isoweekday() in program.enabled_days:  # check if there is an upload for this day
                    try:
                        ftp_client.chdir(program.normalized_name())
                    except IOError:  # never uploaded
                        pass  # we can ignore... stats are properly updated anyway
                    self._update_stats_dict(stats, program, iteration_date, ftp_client)
                    ftp_client.chdir("..")
        self.close_connections()
        return stats

    @staticmethod
    def _default_stat_dict():
        return {"uploaded": [], "not_uploaded": []}

    def _update_stats_dict(self, stats, current_program, iteration_date, ftp_client):
        if current_program.get_filename_for_date(iteration_date.strftime("%Y%m%d")) in ftp_client.listdir():
            stats[iteration_date.strftime("%Y-%m-%d")]["uploaded"].append(
                (current_program.pk, current_program.normalized_name()))
        else:
            stats[iteration_date.strftime("%Y-%m-%d")]["not_uploaded"].append(
                (current_program.pk, current_program.normalized_name()))

    def get_uploaded_dates(self, program: Program):
        self.open_ssh_archive()
        ftp_client = self.ssh_client.open_sftp()
        try:
            ftp_client.chdir(settings.ARCHIVE_SERVER_UPLOAD_DIRECTORY + program.normalized_name())
        except IOError:
            return []

        files = ftp_client.listdir()
        self.close_connections()

        dates = []
        for file in files:
            date_weekday = file[:-4].replace(program.normalized_name(), "")
            if len(date_weekday) == 9:  # has weekday
                without_weekday = date_weekday[:-1]
                dates.append(without_weekday[:4] + "-" + without_weekday[4:6] + "-" + without_weekday[6:])
            else:
                dates.append(date_weekday[:4] + "-" + date_weekday[4:6] + "-" + date_weekday[6:])
        return dates

    def move_from_archive_to_emission(self, program, date: datetime.date):
        source = settings.ARCHIVE_SERVER_UPLOAD_DIRECTORY + program.normalized_name() + "/" + program.get_filename_for_date(
            date.strftime("%Y%m%d"))

        # Replacement is for scp
        destination = "\"\'" + settings.UPLOAD_SERVER_UPLOAD_DIRECTORY + program.get_filename_for_date(
            date.strftime("%Y%m%d")).replace(date.strftime("%Y%m%d"), "") + "\'\""

        # command may error if there is no upload, but we don't care
        command = "scp,{}@{}:{},{}@{}:{}".format(settings.ARCHIVE_SERVER_USERNAME, settings.ARCHIVE_SERVER_IP, source,
                                                 settings.UPLOAD_SERVER_USERNAME, settings.UPLOAD_SERVER_IP,
                                                 destination)
        print("Running:" + command)
        subprocess.run(command.split(","))

    def open_ssh_archive(self):
        tries = 1
        while tries <= 5:
            try:
                self.ssh_client = paramiko.SSHClient()
                self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh_client.connect(hostname=settings.ARCHIVE_SERVER_IP, username=settings.ARCHIVE_SERVER_USERNAME,
                                        password=settings.ARCHIVE_SERVER_PASSWORD)
                print("SSH connection to archive server established.")
                return
            except Exception:
                print("Could not connect to archive server. Trying again. [Attempt {}/5]".format(tries))
                tries += 1
        raise CouldNotConnectToServerException

    def open_ssh_emission(self):
        tries = 1
        while tries <= 5:
            try:
                self.ssh_client = paramiko.SSHClient()
                self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh_client.connect(hostname=settings.UPLOAD_SERVER_IP, username=settings.UPLOAD_SERVER_USERNAME,
                                   password=settings.UPLOAD_SERVER_PASSWORD)
                print("SSH connection to upload/emission server established.")
                return
            except Exception:
                print("Could not connect to upload/emission server. Trying again. [Attempt {}/5]".format(tries))
                tries += 1
        raise CouldNotConnectToServerException

    def close_connections(self):
        if self.ssh_client is not None:
            self.ssh_client.close()
        if self.ftp_client is not None:
            self.ftp_client.close()
