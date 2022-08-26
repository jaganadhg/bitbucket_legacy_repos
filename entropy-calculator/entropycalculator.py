#!/usr/bin/env python
"""
Module to find keywords using the Montemurro and Zanette algorithm.
Created by Dr Peter J. Bleackley
Original code was forked from https://code.google.com/p/entropy-calculator/
Original Paper : http://arxiv.org/pdf/0907.1558.pdf
Hack by Jaganadh Gopinadhan a.k.a Jaggu
e-mail jaganadhg at gmail.com 
Code Licence - Apache 2.0
"""

from math import log, exp, lgamma
import re

class EntropyCalculator(object):
	"""
	Class that contains data and methods for calculating the entropy of
	words in a text
	"""
	strip_xml = re.compile(u'<[^>]*>')
	split_words = re.compile(u"[^A-Za-z0-9']+")
	split_sentences = re.compile(u'[.!?]')
	split_xml = re.compile(u'</p>')
	strip_times = re.compile(u'\d\d:\d\d:\d\d\.\d\d\d')
	
	def __init__(self, p):
		"""
		Creates an EntropyCalculator that uses P blocks to analyse the text
		"""
		self.parts = p
		self.nwords = 0
		self.text = []
		self.wordsperpart = 0
		self.unique = None
		self.rawtext = u''
		self.cleantext = u''
		self.totalentropy = 0.0
		self.rankedwords = []
		self.sentences = []
		self.rankedsentences = []
		self.xml = []
		self.search = []
	
	def log_combinations(self, x, y):
		"""
		Calculates the logarithm of a binomial coefficient.
		This avoids overflows. Implemented with gamma functions for efficiency
		"""
		result = lgamma(x + 1)
		result -= lgamma(y + 1)
		result -= lgamma(x - y + 1)
		return result
	
	def marginal_prob(self, m, n):
		"""
		Calculates the Marginal Probability in the Analytic Entropy calculation
		"""
		result = self.log_combinations(n, m)
		result += self.log_combinations(self.nwords - n, self.wordsperpart - m)
		result -= self.log_combinations(self.nwords, self.wordsperpart)
		prob = exp(result)
		return prob
	
	def analytic_entropy(self, n):
		"""
		Calculates the Analytic entropy of a word that occurs randomly n times
		in the text
		"""
		result = 0.0
		upperbound = min((n, self.wordsperpart))
		for m in range(1, upperbound + 1):
			x = float(m) / n
			result -= self.marginal_prob(m, n) * x * log(x, 2)
		result *= self.parts
		return result
	
	def entropy(self, word):
		"""
		Calculates the entropy of a word
		"""
		n = self.text.count(word)
		H = 0.0
		for i in range(self.parts):
			nj = float(self.text[i * self.wordsperpart:(i + 1) * \
			self.wordsperpart].count(word))
			x = nj / n
			if x > 0:
				H -= x * log(x, 2)
		result = self.analytic_entropy(n) - H
		return (result, n * result / self.nwords)
	
	def set_text(self, data):
		"""
		Loads the text to be analysed
		"""
		self.rawtext = u''
		if type(data).__name__ == 'str' or type(data).__name__ == 'unicode':
			self.rawtext = re.sub(u'\xa3', '&pound;', data.lower())
		else:
			for line in data:
				self.rawtext += re.sub(u'\xa3', '&pound;', line.lower())
		self.cleantext = EntropyCalculator.strip_times.sub('', \
		EntropyCalculator.strip_xml.sub(u'', self.rawtext))
		self.text = EntropyCalculator.split_words.split(self.cleantext)
		self.sentences = EntropyCalculator.split_sentences.split(\
		self.cleantext)
		for i in range(len(self.sentences)):
			if self.sentences[i] == ' ':
				self.sentences[i] += '.'
			else:
				place = self.cleantext.find(self.sentences[i]) + \
				len(self.sentences[i])
				if place < len(self.cleantext):
					self.sentences[i] += self.cleantext[place] + ' '
		self.xml = EntropyCalculator.split_xml.split(self.rawtext)
		for i in range(len(self.xml)):
			self.xml[i] += '</p>'
		self.search = [EntropyCalculator.strip_times.sub('', \
		EntropyCalculator.strip_xml.sub('', line)) for line in self.xml]
		while self.text[-1] == u'':
			self.text.pop()
		self.nwords = len(self.text)
		self.wordsperpart = self.nwords / self.parts
		if self.nwords % self.parts != 0:
			self.wordsperpart += 1
		self.unique = set(self.text)
		
	def set_words_per_part(self, block_size):
		"""
		Changes the block size
		"""
		self.wordsperpart = block_size
		self.parts = self.nwords / self.wordsperpart
		if self.nwords % self.wordsperpart > 0:
			self.parts += 1
	
	def set_parts(self, p):
		u"""Changes the number of blocks"""
		self.parts = p
		self.wordsperpart = self.nwords / self.parts
		if self.nwords % self.parts != 0:
			self.wordsperpart += 1
	
	def analyse_text(self):
		"""
		Calculates the entropy for each unique word in the text
		"""
		self.rankedwords = [(self.entropy(word), word) for word in self.unique]
		self.rankedwords.sort()
		self.rankedwords.reverse()
		self.totalentropy = sum([item[0][1] for item in self.rankedwords])
	
	def analyse_sentences(self):
		entropybyword = dict([(item[1], item[0][0]) for item in \
		self.rankedwords])
		self.rankedsentences = []
		for sentence in self.sentences:
			words = EntropyCalculator.split_words.split(sentence)
			nwords = len(words)
			total = 0.0
			for word in words:
				if word in entropybyword:
					total += entropybyword[word]
			self.rankedsentences.append((total, sentence))
		self.rankedsentences.sort()
		self.rankedsentences.reverse()
	
	def filter_words(self, filter_type=None, threshold=0.0):
		"""
		Selects a subset of the words according to a criterion
		"""
		result = []
		if filter_type == u'Entropy':
			result = [item for item in self.rankedwords if item[0][0]\
			>= threshold]
		elif filter_type == u'Number':
			result = self.rankedwords[:threshold]
		elif filter_type == u'Percentile':
			N = int((self.nwords * threshold / 100) + 0.5)
			result = self.rankedwords[:N]
		elif filter_type == u'Cumulative':
			runningtotal = 0.0
			i = 0
			while runningtotal < threshold:
				runningtotal += self.rankedwords[i][0][1]
				if runningtotal < threshold:
					result.append(self.rankedwords[i])
					i += 1
		elif filter_type == u'ProportionOfEntropy':
			x = threshold * self.totalentropy
			result = self.filter_words(u'Cumulative', x)
		else:
			result = self.rankedwords
		return result
	
	def output_words(self, ofile, filter_type=None, threshold=0.0):
		"""
		Outputs a set of selected keywords and their scores to a file
		"""
		keywords = self.filter_words(filter_type, threshold)
		ofile.write(u'Word,Entropy,Proportion of document entropy\n')
		for ((entropy, contrib), word) in keywords:
			ofile.write(word + u',' + unicode(entropy) + ',' + \
			unicode(contrib) + u'\n')

	def keyword_dictionary(self):
		"""
		Outputs a dictionary of keywords and their entropies
		"""
		self.analyse_text()
		return dict([(word, entropy[0]) for (entropy, word) in \
		self.rankedwords if entropy[0] > 0.0])
	
if __name__ == "__main__":
	import sys
	H = EntropyCalculator(10)
	data = open(sys.argv[1], 'r')
	H.set_text(data)
	H.set_words_per_part(1000)
	H.analyse_text()
	output = open(sys.argv[2], 'w')
	H.output_words(output)
	data.close()
	output.close()
	print sys.argv[1],"contains", H.nwords
	print "Analysed with", H.parts, "blocks"
	print "Total entropy", H.totalentropy, "bits"
	print "Words with entropy >", float(H.parts) / (H.parts + 1), "are likely to be particulary significant"
	print "Detailed analysis written to ",sys.argv[2] 
