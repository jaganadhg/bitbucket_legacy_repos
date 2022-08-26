#!/usr/bin/env python
"""
Simple demo of sklearn text classification with svm Linear kernal
@author Jaganadh G
@email jaganadhg [[@]] gmail [[.]] com
@home http://jaganadhg.in
"""
import os
import sys
import pickle

from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline



def train_classifier(data_dir):
	"""
	@param data_dir -- directory containing training data
	@return classifier lables
	"""
	categories = [name for name in os.listdir(data_dir) if \
	os.path.isdir(os.path.join(data_dir,name))]

	train_data = load_files(data_dir,categories = categories, shuffle = True,\
	random_state=42)
	
	"""
	Create category labels from training data directory structure
	Assumes that directory sturcture is like 
		A
		/\
		B C
	Loads training data
	"""
	vectorizer = CountVectorizer(analyzer = 'word',ngram_range=(1,3),\
	stop_words='english')

	transformer = TfidfTransformer(use_idf=True)


	classifier = Pipeline([('vect',vectorizer),('tfidf',TfidfTransformer()),\
	('clf',LinearSVC()),]) 	
	_ = classifier.fit(train_data.data, train_data.target)
	lables = train_data.target_names
	return classifier,lables


def classify(classifier, str_message):
	"""
	Classifier
	@param classifier -- object of classifier
	@param str_message - string- text documen
	"""
	clsf,lblels = classifier
	msg = str_message

	predicted = clsf.predict([msg])
	category = lblels[predicted[0]]
	return category

	

if __name__ == "__main__":
	train_d = sys.argv[1]
	classifier_o,labels = train_classifier(train_d)
	docs = ["That was a really bad and must worst filim. I hate it because of hero."\
	,"That was a really bad and must worst filim. I hate it because of hero."]
	for doc in docs:
		cat = classifier_o.predict(doc)
		print doc,"\t",labels[cat[0]]
