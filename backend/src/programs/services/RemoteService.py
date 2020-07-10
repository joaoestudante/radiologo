import os
import re
from datetime import datetime

import paramiko
import requests
from django.conf import settings
from django.http import StreamingHttpResponse

from exceptions.radiologoexception import FileAlreadyUploadedException, FileNotDeletedException, \
    FileDoesNotExistException


class RemoteService:
    def __init__(self):
        pass

    def check_file_for_date(self, program, emission_date):  # emission_date is YYYYMMDD
        potential_file = settings.ARCHIVE_SERVER_UPLOAD_DIRECTORY + program + "/" + emission_date + "*"

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=settings.ARCHIVE_SERVER_IP, username=settings.ARCHIVE_SERVER_USERNAME,
                           password=settings.ARCHIVE_SERVER_PASSWORD)

        ftp_client = ssh_client.open_sftp()
        try:
            ftp_client.stat(potential_file)
        except IOError:
            raise FileAlreadyUploadedException
        return ftp_client

    def upload_program_to_archive(self, normalized_program_name, file_path):
        archive_folder = settings.ARCHIVE_SERVER_UPLOAD_DIRECTORY + normalized_program_name + "/"

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=settings.ARCHIVE_SERVER_IP, username=settings.ARCHIVE_SERVER_USERNAME,
                           password=settings.ARCHIVE_SERVER_PASSWORD)

        ftp_client = ssh_client.open_sftp()
        try:
            ftp_client.chdir(archive_folder)
        except IOError:
            ftp_client.mkdir(archive_folder)

        ftp_client.put(file_path, archive_folder + os.path.basename(file_path))
        ftp_client.close()
        return

    def upload_program_to_emission(self, file_path):
        short_filename = os.path.basename(file_path).replace(datetime.now().strftime("%Y%m%d"),
                                                             "")  # Maintains weekday info, if it exists
        emission_file_path = settings.UPLOAD_SERVER_UPLOAD_DIRECTORY + short_filename

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=settings.UPLOAD_SERVER_IP, username=settings.UPLOAD_SERVER_USERNAME,
                           password=settings.UPLOAD_SERVER_PASSWORD)

        ftp_client = ssh_client.open_sftp()
        ftp_client.put(file_path, emission_file_path)
        ftp_client.close()
        return

    def download_archive_file(self, normalized_program_name, emission_date):
        filename = normalized_program_name + emission_date + ".mp3"
        archive_url = "http://{}".format(settings.ARCHIVE_SERVER_IP)
        session = requests.Session()
        session.auth = (settings.ARCHIVE_SERVER_USERNAME, settings.ARCHIVE_SERVER_PASSWORD)
        session.post(archive_url)

        r = session.get(archive_url + '/archive/' + normalized_program_name + "/" + filename, stream=True)

        resp = StreamingHttpResponse(r.iter_content(8096))
        resp['headers'] = "X-Accel-Redirect"
        resp['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        resp['Accept-Ranges'] = 'bytes'
        resp['Content-Type'] = 'audio/mpeg'

        return resp

    def get_archive_contents(self, normalized_program_name):
        destination = "/srv/arquivo_sonoro/radiologo/"
        file_list = {}

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=settings.ARCHIVE_SERVER_IP, username=settings.ARCHIVE_SERVER_USERNAME,
                           password=settings.ARCHIVE_SERVER_PASSWORD)

        ftp_client = ssh_client.open_sftp()

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
            return file_list

    def delete_archive_file(self, normalized_program_name, date):  # date is YYYYMMDDw (where w=weekday and is optional)
        file = settings.ARCHIVE_SERVER_UPLOAD_DIRECTORY + normalized_program_name + "/" + normalized_program_name + \
               date + ".mp3"

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=settings.ARCHIVE_SERVER_IP, username=settings.ARCHIVE_SERVER_USERNAME,
                           password=settings.ARCHIVE_SERVER_PASSWORD)

        ftp_client = ssh_client.open_sftp()

        try:
            ftp_client.remove(file)
        except IOError:
            raise FileDoesNotExistException

        try:
            ftp_client.stat(file)
            raise FileNotDeletedException
        except IOError:
            pass  # Success

        return
