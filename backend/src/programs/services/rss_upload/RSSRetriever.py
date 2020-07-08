import feedparser
import requests
from django.conf import settings
import re #builtin
import os #builtin
from datetime import timedelta #builtin
from collections import namedtuple #builtin
from operator import attrgetter #builtin

class RSSRetriever:

	def __init__(self, url):
		self.feed_url = url
		self.name = ""
		self.episodeList = []

	def _uniformizeDuration (string):
		""" INTERNAL function: Parses duration information into
		timedelta object which can be stringified using str()
		or manipulated to other formats (show in seconds, etc.) """
	
		#Regex to interpret time durations in several formats
		durationDetector = re.compile("^([0-9]+):*([0-9]+)*:*([0-9]+)*")
	
		groupings = durationDetector.match(string).groups()
	
		if groupings[0] == None:
			raise SyntaxError('Episode duration format not recognized')
		elif groupings[1] == None:
			#duration was specified in seconds
			return timedelta(seconds=int(groupings[0]))
		elif groupings[2] == None:
			#duration was specified in minutes:seconds
			return timedelta(minutes=int(groupings[0]), seconds=int(groupings[1]))
		else:
			#duration was specified in hours:minutes:seconds
			return timedelta(hours=int(groupings[0]), minutes=int(groupings[1]), seconds=int(groupings[2]))


	def listEpisodesinPodcast (feedurl):
		""" Retrieve a list of episodes at the podcast feed
		located in _feedurl_.
		RETURNS [Episode] as list of Episode, podcastname as str
		Episode.title is str
		Episode.duration is datetime.timedelta
		Episode.date is time.struct_time
		Episode.link is Link
		(Episode.link.href is str, Episode.link.type is str)"""
	
		#Declare structures and tools
		Episode = namedtuple('Episode', 'title duration date link')
		Link = namedtuple('Link', 'href type')
	
		#Download and parse feed
		parsed = feedparser.parse(feedurl)
	
		self.name = parsed.feed.title

		#Extract episode list
		self.episodelist = [ Episode(title = episode.title, \
					duration = _uniformizeDuration(episode.itunes_duration), \
					date = episode.published_parsed, \
					link = Link(href=episode.enclosures[0].href, type=episode.enclosures[0].type)) \
	     	      for episode in parsed.entries]
		self.episodelist.sort(reverse=True, key=attrgetter('date'))
		return self.episodelist, self.name

	def downloadEpisode (destpath, episode):
		""" Downloads an episode _episode_ (Episode from episodelist)
		to the respective location specified in _destpath_
		which should not contain any extension, since it is
		added automatically depending on file type.
		RETURNS str location of file *including* file extension."""
	
		episodeurl = episode.link.href
		episodetype = episode.link.type
	
		if episodetype == 'audio/mpeg':
			destpath += '.mp3'
		elif episodetype == 'audio/mp4' or episodetype=='audio/x-m4a':
			destpath += '.m4a'
		elif episodetype == 'audio/ogg':
			destpath += '.ogg'
		else:
			destpath += '.mp3' #Just assume mp3...
	
		r = requests.get(episodeurl, stream=True) #Stream -> Do not download file yet
	
		with open(destpath, "wb") as episodefile: #Open destination path
			for chunk in r.iter_content(chunk_size=1024): #Download in chunks
				if chunk:
					episodefile.write(chunk)
					#print('.', end='', flush=True) #Debug only
	
		return destpath

	def downloadLastEpisode(normalized_name):
		"""Automatically download last episode"""
		episodes = listEpisodesinPodcast(self.feed_url)
		destpath = downloadEpisode(settings.FILE_UPLOAD_DIR + "uploaded_feed_" + normalized_name, episodes[0])
		#Introduce a function that hands over to processing here
		#e.g. ProcessFile(destpath_ext)
		#Introduce a function that notifies 
		#the Programming department by email of successful upload
		#with information of episode name and its date
		#e.g. SendEmail(episodes[0].title, episodes[0].date)
		#Cleanup the file
		os.remove(destpath)


#Tests

#Test urls (leave only one uncommented to use)

#feedurl = 'https://rss.art19.com/planetary-radio-space-exploration-astronomy-and-science' #Planetary Radio
#feedurl = 'http://benandmarty.libsyn.com/rss' #White Noise
#feedurl = 'http://www.outfarpress.com/podcast.xml' #Shortwave report
#feedurl = 'https://anchor.fm/s/79d3b20/podcast/rss' #Zero Preconceitos

#Feed retrieve test

#episodelist, podcastname = listEpisodesinPodcast(feedurl)

#Pretty-print last 5 episodes
#print(podcastname)
#pprint.pprint(episodelist[0:5])
#print( str(episodelist[0].duration) ) #output a duration in HH:MM:SS format

#Download episode to current directory with filename test(ensure you have permissions)

#downloadEpisode('test', episodelist[0])
