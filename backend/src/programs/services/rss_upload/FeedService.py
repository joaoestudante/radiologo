from programs.models import Program
from programs.services.processing.ProcessingService import ProcessingService

from django.conf import settings

import feedparser
import requests
from django.conf import settings
import re  # builtin
import os  # builtin
from datetime import timedelta  # builtin
from collections import namedtuple  # builtin
from operator import attrgetter  # builtin
from time import struct_time

class FeedService:

    def __init__(self, program_pk):
        self.program_pk = program_pk
        self.program =  Program.objects.get(pk=self.program_pk)
        self.normalized_program_name = self.program.normalized_name()
        self.feed_url = self.program.rss_feed_url
        self.feed_status = self.program.rss_feed_status
        self.next_emission_date = self.program.next_emission_date()
        self.name = ""
        self.episodeList = []

    def _uniformize_duration(self, string):
        """ INTERNAL function: Parses duration information into
        timedelta object which can be stringified using str()
        or manipulated to other formats (show in seconds, etc.) """

        # Regex to interpret time durations in several formats
        durationDetector = re.compile("^([0-9]+):*([0-9]+)*:*([0-9]+)*")

        groupings = durationDetector.match(string).groups()

        if groupings[0] == None:
            raise SyntaxError('Episode duration format not recognized')
        elif groupings[1] == None:
            # duration was specified in seconds
            return timedelta(seconds=int(groupings[0]))
        elif groupings[2] == None:
            # duration was specified in minutes:seconds
            return timedelta(minutes=int(groupings[0]), seconds=int(groupings[1]))
        else:
            # duration was specified in hours:minutes:seconds
            return timedelta(hours=int(groupings[0]), minutes=int(groupings[1]), seconds=int(groupings[2]))

    def list_episodes_in_podcast(self) -> tuple:
        """ Retrieve a list of episodes at the podcast feed
        located in _feedurl_.
        RETURNS [Episode] as list of Episode, podcastname as str"""

        # Download and parse feed
        parsed = feedparser.parse(self.feed_url)

        self.name = parsed.feed.title

        # Extract episode list
        self.episodelist = [Episode(title=episode.title,
                                    duration=self._uniformize_duration(episode.itunes_duration),
                                    date=episode.published_parsed,
                                    link=Link(href=episode.enclosures[0].href, type=episode.enclosures[0].type))
                            for episode in parsed.entries]
        self.episodelist.sort(reverse=True, key=attrgetter('date'))
        return self.episodelist, self.name

    def download_episode(self, destpath, episode):
        """ Downloads an episode _episode_ (Episode from episodelist)
        to the respective location specified in _destpath_
        which should not contain any extension, since it is
        added automatically depending on file type.
        RETURNS str location of file *including* file extension."""

        episodeurl = episode.link.href
        episodetype = episode.link.type

        if episodetype == 'audio/mpeg':
            destpath += '.mp3'
        elif episodetype == 'audio/mp4' or episodetype == 'audio/x-m4a':
            destpath += '.m4a'
        elif episodetype == 'audio/ogg':
            destpath += '.ogg'
        else:
            destpath += '.mp3'  # Just assume mp3...

        r = requests.get(episodeurl, stream=True)  # Stream -> Do not download file yet

        with open(destpath, "wb") as episodefile:  # Open destination path
            for chunk in r.iter_content(chunk_size=1024):  # Download in chunks
                if chunk:
                    episodefile.write(chunk)
        # print('.', end='', flush=True) #Debug only

        return destpath

    def download_last_episode(self):
        """Automatically download last episode"""
        if self.feed_status == True:
            print("\t\t- Automatic RSS Feed Upload for "+ self.normalized_program_name)
            # Retrieve Episode List
            episodes, podcastname = self.list_episodes_in_podcast(self.feed_url)
            print("\t\t- Podcast name: "+ self.name)
            # Download last episode
            destpath = self.download_episode(settings.FILE_UPLOAD_DIR + "uploaded_feed_" + self.normalized_program_name, episodes[0])
            print("\t\t- Retrieved episode with title \""+ episodes[0].title + "\" dated from " + str(episodes[0].date))
            # Process the file
            service = ProcessingService(path=destpath, program_pk=self.program_pk, emission_date=self.next_emission_date,
                                author_name=self.name, email=settings.ADMIN_EMAIL)
            service.process()
        return True

# Tests

# Test urls (leave only one uncommented to use)

# feedurl = 'https://rss.art19.com/planetary-radio-space-exploration-astronomy-and-science' #Planetary Radio
# feedurl = 'http://benandmarty.libsyn.com/rss' #White Noise
# feedurl = 'http://www.outfarpress.com/podcast.xml' #Shortwave report
# feedurl = 'https://anchor.fm/s/79d3b20/podcast/rss' #Zero Preconceitos

# Feed retrieve test

# episodelist, podcastname = listEpisodesinPodcast(feedurl)

# Pretty-print last 5 episodes
# print(podcastname)
# pprint.pprint(episodelist[0:5])
# print( str(episodelist[0].duration) ) #output a duration in HH:MM:SS format

# Download episode to current directory with filename test(ensure you have permissions)

# downloadEpisode('test', episodelist[0])

class Link(namedtuple):
    href: str
    type: str

class Episode(namedtuple):
    title: str
    duration: timedelta
    date: struct_time
    link: Link

