#!/usr/bin/env python
"""
This is a python libraray for corpus processing. The library is designed for to
find t-score, mutual info , log likely hood and ngram (unigram , bigram and
trigram ) from a given text.

Usage:

    >>> from corpus import *
    >>> corpus = Corpus()
    >>> inp = "mytext.txt"

    To find tscore
    >>> tscore = corpus.ttest(inp) # return a dict
    >>> for ts in tscore.keys():
    ....    print ts, "\t", tscore[ts]

    To find log likely hood
    >>> loglike = corpus.logLikelyHood(inp) # return a dict

    >>> for lo in loglike.keys():
    ....    print lo, "\t", loglike[lo]

    To find mutual info
    >>> mutualinfo = corpus.mutualInfo(inp) # return a dict

    >>> for min in mutualinfo.keys():
    ....    print min, "\t", mutualinfo[min]

 """
from __future__ import division
import math
import string
import sys
import re
import collections

__author__ = "Jaganadh G"
__copyright__ = "Copyright 2009, Jaganadh G"
__licence__ = "MIT Licence"
__version__ = "1.0.1"
__email__ = "jaganadhg@gmail.com"

class Corpus(object):
    """
    Yet another Python library for corpus processing
    """

    def __init__(self):
        """
        Init
        """

    def logLikelyHood(self, text):
        """
        Function to generate log likelyhood from a given text.
        Returns dict.
        """
        uni_freq,words = self.ngram(text)
        big_freq, bigrams = self.ngram(text,n=2)
        log_like_hood = {}

        for word in range(len(words)-1):
            p = uni_freq[words[word + 1]] / len(words)
            p1 = big_freq[bigrams[word]] / uni_freq[words[word]]
            p2 = ((uni_freq[words[word + 1]] - big_freq[bigrams[word]]) \
            / (len(words) - uni_freq[words[word]]))

            if p1 != 1 and p2 != 0:
                log_like_hood[bigrams[word]] = 2 * ((big_freq[bigrams[word]] * \
                math.log(p1) + (uni_freq[words[word]] - big_freq[bigrams[word]])) * \
                math.log(1- p1) + (uni_freq[words[word + 1]] - big_freq[bigrams[word]] * \
                math.log(p2) + (len(words)- uni_freq[words[word]] - uni_freq[words[word + 1]] + \
                big_freq[bigrams[word]]) * math.log(1-p2) - big_freq[bigrams[word]] * \
                math.log(p) + (uni_freq[words[word]] -big_freq[bigrams[word]]) * \
                math.log(1 - p) - (uni_freq[words[word + 1]] - big_freq[bigrams[word]]) * \
                math.log(p) + (len(words) - uni_freq[words[word]] - uni_freq[words[word + 1]]) + \
                big_freq[bigrams[word]]) * math.log(1-p))



        return log_like_hood

    def mutualInfo(self, text):
        """
        Function to generate mutual info from a text.
        Returnd dict.
        """
        uni_freq,words = self.ngram(text)
        words = uni_freq.keys()
        big_freq, bigrams = self.ngram(text,n=2)
        mutual_info = {}
        mutual_infoa = {}
        for bigram in bigrams:
            #print bigram.split(" ")[0]
            mutual_infoa[bigram] = math.log((len(words) + 1) * \
            big_freq[bigram] / (uni_freq[bigram.split(" ")[0]] * uni_freq[bigram.split(" ")[1]]))/ math.log(2)
        for bigram in bigrams:
            #print bigram.split(" ")[0]
            mutual_info[bigram] = (big_freq[bigram] + 1)  / (uni_freq[bigram.split(" ")[0]] + len(set(words))) 
        return mutual_info

    def ttest(self, text):
        """
        Function to find tscore form a text.
        Returns text
        """
        ugfreq,words = self.ngram(text)
        words = ugfreq.keys()
        bigfreq, bigrams = self.ngram(text,n=2)

        tsc = {}


        for wor in range(len(words) -1):
            tsc[bigrams[wor]] = (bigfreq[bigrams[wor]] - \
            ugfreq[words[wor]] * ugfreq[words[wor + 1]] / \
            (len(words) + 1)) / float(math.sqrt(bigfreq[bigrams[wor]]))


        return tsc

    def ngram(self, text,n=1):
		words = self.__cleanText(text)

		if n == 1:
			wordfreq = collections.Counter(words)
			return wordfreq,words
		elif n == 2:
			grams = [words[w] + " " + words[w +1] for w in range(len(words)-1)]
			gramfreq = collections.Counter(grams)
			return gramfreq, grams
		elif n == 3:
			grams = [words[w] + " " + words[w +1] + " " + words[w + 2] for w in range(len(words)-2)]
			gramfreq = collections.Counter(grams)
			return gramfreq, grams

    def __cleanText(self, text):
        """
        Private function to clean input text.
        """
        splitter = re.compile(r'\s+',re.UNICODE)
        textcont = open(text, 'r').read()
        words = [word.translate(None,string.punctuation).lower() for word in splitter.split(textcont) if len(word) > 1]
        return words

if __name__ == "__main__":
    corpus = Corpus()
    inp = sys.argv[1]
    tscore = corpus.ttest(inp)
    loglike = corpus.logLikelyHood(inp)
    mutualinfo = corpus.mutualInfo(inp)

    """print "**********************************************88"

    for ts in tscore.keys():
        print ts, "\t", tscore[ts]

    print "#################################################"

    for lo in loglike.keys():
        print lo, "\t", loglike[lo]

    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" """

    for min in mutualinfo.keys():
        print min, "\t", mutualinfo[min]
