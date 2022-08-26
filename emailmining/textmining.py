#!/usr/bin/env python
import sys

from nltk.collocations import BigramCollocationFinder,\
TrigramCollocationFinder,TrigramAssocMeasures,\
BigramAssocMeasures
from nltk.corpus import stopwords

STOPWORDS = set(word for word stopwords.words('english'))

def extract_collocations(words,topn=50,ngrams=2):
	"""
	Extract bigram/trigram collocations from text using NLTK
	Collocation finder
	"""
	mesures = BigramAssocMeasures()
	colloc_finder = BigramCollocationFinder
	if ngrams == 3:
		mesures = TrigramAssocMeasures()
		colloc_finder = TrigramCollocationFinder()

	colloc_finder.from_words(words)
	colloc_finder.apply_freq_filter(3)
	frequent_colloc = colloc_finder.nbest(mesures.pmi,topn)

	return frequent_colloc


def mongodoc_to_words(mongodocs):
	"""
	MongoDB documents to words
	"""
	words = list()
	for document in mongodocs:
		tmp_doc = document.lower().replace("\n"," ")
		tmp_words = [wrd.strip() for wrd in tmp_doc.split(" ") \
		if wrd not in STOPWORDS and len(wrd.strip()) > 1]
		words.extend(tmp_words)
	return words



