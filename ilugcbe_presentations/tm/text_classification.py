#!/usr/bin/env python

from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB


dir_data = "/usr/share/nltk_data/corpora/movie_reviews/"

vectorizer = CountVectorizer(analyzer = 'word',ngram_range = (1,3),\
stop_words='english',lowercase=True)
transformer = TfidfTransformer(use_idf=True)
classifier = Pipeline([('vect',vectorizer),('tfidf',transformer),\
('clf',MultinomialNB()),]) 

categories = ['pos','neg']
training_data = load_files(dir_data,categories=categories,\
shuffle = True)

tr_d = training_data.data[:700]
tr_t = training_data.target[:700]

test_d = training_data.data[700:]
test_t = training_data.target[700:]

_ = classifier.fit(tr_d, tr_t)
#_ = classifier.fit(training_data.data, training_data.target)
#print training_data.target_names[classifier.predict(['This is a good one'])]

predicted = classifier.predict(test_d)
print predicted
import numpy as np
print np.mean(predicted == test_t)
from sklearn import metrics
print metrics.confusion_matrix(test_t,predicted)

print metrics.classification_report(test_t,predicted,target_names = \
		training_data.target_names)





import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews



def word_feats(words):
	return dict([(word, True) for word in words])
	 
negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')
	 
negfeats = [(word_feats(movie_reviews.words(fileids=[f])), \
		'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), \
		'pos') for f in posids]
	  
negcutoff = len(negfeats)*3/4
poscutoff = len(posfeats)*3/4
	   
trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

classifier = NaiveBayesClassifier.train(trainfeats)

sent = "This is really cool. I like it"
words = word_feats(sent.lower().split())

print classifier.classify(words)
