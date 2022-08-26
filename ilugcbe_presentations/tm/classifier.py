#!/usr/bin/env python
from __future__ import division
import re
import math


TOKENIZER = re.compile('\\W*')

def stop_filter(words):
    stops = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', \
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', \
    'she','her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', \
    'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', \
    'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were','be', 'been', \
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', \
    'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because','as', 'until', \
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',\
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',\
    'from', 'up', 'down', 'in', 'out','on', 'off', 'over', 'under', 'again',\
    'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',\
    'all', 'any', 'both', 'each', 'few','more', 'most', 'other', 'some', 'such',\
    'no', 'nor','not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', \
    't', 'can', 'will', 'just', 'don', 'should', 'now','']

    stopless = [word for word in words if word not in stops]

    return stopless

def feature_extractor(text):
	words = TOKENIZER.split(text.lower())
	content_words = stop_filter(words)

	return dict([(word,1) for w in content_words if len(w) >2])

class Classifier(object):

	def __init__(self,feat_extractor,filename=None):
		self.feature_count = {}
		self.category_count = {}
		self.feat_ext = feat_extractor
	
	def increase_feature(self,feature,category):
		self.feature_count.setdefault(feature,{})
		self.feature_count[feature].setdefault(category,0)
		self.feature_count[feature].[category] += 1
	
	def increase_category(self,category):
		self.category_count.setdefault(cat,0)
		self.category_count[category] += 1

