import os
import re
import subprocess
from datetime import datetime, timedelta
from stat import S_ISREG

import paramiko
import requests
from django.conf import settings
from django.http import StreamingHttpResponse

from exceptions.radiologoexception import FileAlreadyUploadedException, FileNotDeletedException, \
    FileDoesNotExistException, CouldNotConnectToServerException

import collections


class RemoteService:
    def __init__(self):
        self.ssh_client = None
        self.ftp_client = None

    def check_track_exists(self, filename: str):  # emission_date is YYYYMMDD
        potential_file = settings.PLAYLIST_SERVER_UPLOAD_DIRECTORY + filename

        self.open_ssh_playlist()
        ftp_client = self.ssh_client.open_sftp()
        try:
            file = ftp_client.stat(potential_file)
            if file is not None:
                raise FileAlreadyUploadedException
        except IOError:
            pass  # Success

        return ftp_client

    def upload_track_to_playlist(self, filename: str, local_path: str):
        final_path = settings.PLAYLIST_SERVER_UPLOAD_DIRECTORY + filename

        self.open_ssh_playlist()
        ftp_client = self.ssh_client.open_sftp()
        ftp_client.put(local_path, final_path)
        self.close_connections()
        return

    def download_playlist_file(self, filename: str):
        #Not implemented, previous implementation does not use SFTP
        return False

    def get_playlist_contents(self):
        destination = settings.PLAYLIST_SERVER_UPLOAD_DIRECTORY[:-1]
        file_list = []

        self.open_ssh_playlist()
        ftp_client = self.ssh_client.open_sftp()

        try:
            for entry in ftp_client.listdir_attr(destination):
                mode = entry.st_mode
                if S_ISREG(mode):
                    file_list.append(entry.filename)
        except IOError as e:
            pass
        finally:
            self.close_connections()
            return { i : file_list[i] for i in range(0, len(file_list) ) }

    def delete_playlist_file(self, filename: str): 
        file = settings.PLAYLIST_SERVER_UPLOAD_DIRECTORY + filename

        self.open_ssh_playlist()
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

    def open_ssh_playlist(self):
        tries = 1
        while tries <= 5:
            try:
                self.ssh_client = paramiko.SSHClient()
                self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh_client.connect(hostname=settings.PLAYLIST_SERVER_IP, username=settings.PLAYLIST_SERVER_USERNAME,
                                        password=settings.PLAYLIST_SERVER_PASSWORD)
                print("SSH connection to playlist server established.")
                return
            except Exception:
                print("Could not connect to playlist server. Trying again. [Attempt {}/5]".format(tries))
                tries += 1
        raise CouldNotConnectToServerException

    def close_connections(self):
        if self.ssh_client is not None:
            self.ssh_client.close()
        if self.ftp_client is not None:
            self.ftp_client.close()
