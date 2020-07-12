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

import collections


class RemoteService:
    def __init__(self):
        self.ssh_client = None
        self.ftp_client = None

    def check_track_exists(self, filename: str):  # emission_date is YYYYMMDD
        potential_file = "\"\'" + settings.PLAYLIST_SERVER_UPLOAD_DIRECTORY + filename + "\'\""

        self.open_ssh_playlist()
        ftp_client = self.ssh_client.open_sftp()
        try:
            file = ftp_client.stat(potential_file)
            if file is not None:
                raise FileAlreadyUploadedException
        except IOError:
            pass  # Success

        return ftp_client

    def upload_track_to_playlist(self, filename: str, initial_file_path: str):
        playlist_folder = "\"\'" + settings.PLAYLIST_SERVER_UPLOAD_DIRECTORY + "\'\""
        final_path = "\"\'" + settings.PLAYLIST_SERVER_UPLOAD_DIRECTORY + filename + "\'\""

        self.open_ssh_archive()
        ftp_client = self.ssh_client.open_sftp()
        ftp_client.chdir(archive_folder)

        ftp_client.put(initial_file_path, final_path)
        self.close_connections()
        return

    def download_playlist_file(self, filename: str):
        #Not implemented, previous implementation does not use SFTP
        return False

    def get_playlist_contents(self):
        destination = "\"\'" + settings.PLAYLIST_SERVER_UPLOAD_DIRECTORY + "\'\""
        file_list = []

        self.open_ssh_playlist()
        ftp_client = self.ssh_client.open_sftp()

        try:
            ftp_client.chdir(destination)
            for file_name in ftp_client.listdir():
                file_list.append(file_name)
        except IOError as e:
            pass
        finally:
            self.close_connections()
            return file_list

    def delete_playlist_file(self, filename: str): 
        file = "\"\'" + settings.PLAYLIST_SERVER_UPLOAD_DIRECTORY + filename + "\'\""

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
                self.ssh_client.connect(hostname=PLAYLIST_SERVER_IP, username=settings.PLAYLIST_SERVER_USERNAME,
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
