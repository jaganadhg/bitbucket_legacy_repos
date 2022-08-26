#!/usr/bin/env python
import sys
import urllib
import time
from urllib import urlencode
from xml.dom.minidom import parseString
from xml.dom import minidom

__version__ = '1.0'
__author__ = 'Jaganadh G'
__url__ = 'http://jaganadhg.freeflux.net/blog'
__email__ = 'jaganadhg@gmail.com'
__license__ = 'Apache Licence'


class YahooTermExtractor(object):
    """
	An unofficial API for Yahoo! Term Extracton Web Service
	For details on Yahoo! Term Extraction Web Services read:
	http://developer.yahoo.com/search/content/V1/termExtraction.html
    Note: The Term Extraction service is limited to 5,000 queries 
    per IP address per day and to noncommercial use.
    API Documentation:
    =================
    yte = YahooTermExtractor()
    text = open('sample.txt','r').read()
    terms = yte.getTerms(text) # reurns list of terms from the given document
    """
    def __init__(self):
        """
        Base URL
        """
        self.BASEURL = 'http://search.yahooapis.com/ContentAnalysisService/V1/termExtraction?'


    def getTerms(self,text,appid):
        urlparams = { 'appid':appid, 'context':text }
        encparam = urlencode(urlparams)
        appurl = self.BASEURL + encparam
        connect = urllib.urlopen(appurl)
        result = connect.read()
        time.sleep(3)
        xmldoc = minidom.parseString(result)
        allterms = [term.firstChild.wholeText for term in \
        xmldoc.getElementsByTagName("Result")]
        return allterms
	
if __name__ == "__main__":
    yte = YahooTermExtractor()
    sample = open('we8.txt','r').read()
    print yte.getTerms(sample,"APPKEY")
