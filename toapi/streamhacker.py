#!/usr/bin/env python
#Un-Official python API for http://text-processing.com
#@author Jaganadh Gopinadhan <jaganadhg@gmail.com>
#@url jaganadhg.in
#@licence Apache Licence
"""
An unofficial Python API for http://text-processing.com 
"""
import pycurl
import StringIO


class TextProcessing(object):
	"""

	"""
	
	def __init__(self):
		self.BUFFER = StringIO.StringIO()
		self.BASEURL = 'http://text-processing.com/api/'
		self.CHARLIMIT = 10000
		self.STATUS = [400,503]
		self.PROXY = ''
		self.PROXYCRED = ''
		self.FETCHER = pycurl.Curl()
		self.FETCHER.setopt(self.FETCHER.PROXY,'')
		self.FETCHER.setopt(self.FETCHER.PROXYUSERPWD,'')
		self.FETCHER.setopt(self.FETCHER.WRITEFUNCTION,self.BUFFER.write)
	
	def sentiment(self,review):
		"""
		@args String text
		@return dict label
		"""
		API = 'sentiment/'
		URL = self.BASEURL + API
		self.FETCHER.setopt(self.FETCHER.URL,URL)

		if len(review) < self.CHARLIMIT and len(review) > 3:
			self.FETCHER.setopt(self.FETCHER.POSTFIELDS,"text"+ "=" + review)
			self.FETCHER.perform()
			status = self.FETCHER.getinfo(self.FETCHER.HTTP_CODE)
			if status in self.STATUS:
				print "You have reached maximum limit for the day"
				print "Signup for the Mashape Text-Processing API to get a \
				higher limit plan."
			else:
				result = self.BUFFER.getvalue()
				return result
		else:
			print "CharLimitExceed : \n Input exceeds max character limit\n \
					or text length tooooo short :-("
	

	def stem(self,textdata,language='english',stemmer='porter'):
		"""
		@args text , language, stemmer
		@reurn dict stems
		"""
		API = 'stem/'
		URL = self.BASEURL + API

		languages = ['arabic','english','danish','dutch','finnish',\
		'french','german','hungarian','italian','norwegian',\
		'portuguese','romanian','russian','spanish','swedish']
		stemmers = ['porter','lancaster','wordnet','rslp','isri'\
		'snowball']

		self.FETCHER.setopt(self.FETCHER.URL,URL)
		
		if len(textdata) < self.CHARLIMIT and len(textdata) > 3:
			if stemmer == "wordnet" and language != "english":
				print "WordNet Stemmer supports only English"
			elif stemmer == "rslp" and language != "portuguese":
				print "RSLP stemmer supports only Portuguese"
			elif stemmer == "isri" and language != "arabic":
				print "ISRI stemmer supports only Arabic"
			elif stemmer not in stemmers or language not in languages:
				print "Stemmer or language not covered"
		else:
			self.FETCHER.setopt(self.FETCHER.POSTFIELDS,'text=' + textdata)
			self.FETCHER.setopt(self.FETCHER.POSTFIELDS,'language=' + language)
			self.FETCHER.setopt(self.FETCHER.POSTFIELDS,'stemmer=' + stemmer)
			self.FETCHER.perform()
			status = self.FETCHER.getinfo(self.FETCHER.HTTP_CODE)
			if status in self.STATUS:
				print "You have reached maximum limit for the day"
				print "Signup for the Mashape Text-Processing API to get a \
				higher limit plan."
			else:
				result = self.BUFFER.getvalue()
				return result

if __name__ == "__main__":
	data = "processing"
	to = TextProcessing()
	res = to.stem(data)
	print res
