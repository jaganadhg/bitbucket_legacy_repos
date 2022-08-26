#!/usr/bin/env python

from nltk.corpus import movie_reviews
from nltk.probability import ConditionalFreqDist
from nltk.cluster import KMeansClusterer,euclidean_distance
from numpy import numarray

def create_doc(labels,n_class):
	doc_set = []

	for label in labels:
		for file in movie_reviews.fileids(categories=label):
			doc = movie_reviews.raw(file)
			doc['FILE'] = file
			doc['LABEL'] = label
			doc_set.append(doc)
	
	return doc_set


def vectorize_docs(docs):
	words = set()
	cfd = ConditionalFreqDist()

	for doc in docs:
		for word in doc['WORDS']:
			text = word['TEXT']
			words.add(text)
			cfd[doc['FILE']].inc(text)
	

	for doc in docs:
		vector = [ cfd[doc['FILE']].count(word) for word in words ]
		doc['FEATURES'] = numarray.array(vector)
	
	return words

if __name__ == "__main__":
	labels = ['pos','neg']
	docs = create_doc(labels,2)
	vector = vectorize_docs(docs)
	clusterer = KMeansClusterer(2,euclidean_distance)
	clusterer.cluster(docs,True)
	means = clusterer.means()
