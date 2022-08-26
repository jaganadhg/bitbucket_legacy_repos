#!/usr/bin/env python
from __future__ import division
import os,sys
import re
from math import sqrt,log
from operator import itemgetter
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from pytagcloud import create_tag_image, make_tags
import networkx as nx
from happyfuntokenizing import Tokenizer


tokenozer = re.compile('\\W*')

def twokenize(tweet,pc=True):
	"""
	Tokenize tweets ysing happyfuntokenizing
	https://bitbucket.org/jaganadhg/twittertokenize
	The file happyfuntokenizing.py should be in the same dir
	@param pc = Preserve Case if set true case sensiteive
	"""
	twokenizer = Tokenizer(preserve_case=pc)

	return twokenizer.tokenize(tweet)


def tokenize(text):
	"""
	Tokenizing raw text to words
	"""
	words = tokenozer.split(text.strip().lower())
	return [word for word in words if word != '']

def ngrams(words,n=2):
	"""
	Populate N-Grams from words
	"""
	grams = [" ".join(words[x:x+n]) for x in xrange(len(words)-n+1)]
	return grams

def stop_filter(words):
	"""
	Remove stopwords from list of words
	Depends on english file 
	"""
	s = open('english','r').readlines()
	stops = [i.strip() for i in s]
	stopless = [word for word in words if word not in stops]
	stopless = [word for word in stopless if len(word) > 1]

	return stopless

def freq_count(seqeunces):
	"""
	Count frequency of each item in a list
	Generic freq counter for words and N-Grams
	"""
	frequency = dict([seq, seqeunces.count(seq)]\
	for seq in set(seqeunces))
	return frequency

def top_items(items,n=50):
	"""
	Finds top N items from a list
	To find ton N words or N-Grams
	"""
	wordfreq = freq_count(items)
	topwords = sorted(wordfreq.iteritems(), key = itemgetter(1),\
	reverse=True)[:n]
	return topwords

def word_propo(words):
	"""
	Find word propotion from a given set of words
	wp(word) = c(word) / c(words)
	"""
	wc = freq_count(words)
	propo = dict([(word, wc[word]/len(words)) for word\
	in set(words)])
	return propo

def word_type_ratio(words):
	"""
	Find word type ratio from a set of words
	wtr(words) = c(words)/c(uniq_words)
	"""
	return len(words) / len(set(words))


def tscore(words):
	grams = ngrams(words,n=2)
	wordcount = freq_count(words)
	gramcount = freq_count(grams)
	tsc = {}

	for gram in grams:
		print gram
		tsc[gram] =  (gramcount[gram]  - (1/len(words)) * \
		wordcount[gram.split()[0]]  * wordcount[gram.split()[1]])\
		/ sqrt( gramcount[gram])
	
	return tsc

def mutual_info(words):
	grams = ngrams(words,n=2)
	wordcount = freq_count(words)
	gramcount = freq_count(grams)
	minfo = {}
	
	for gram in grams:
		minfo[gram] = (log( len(words) * gramcount[ gram ] \
		/ wordcount[gram.split()[0]] * wordcount[ gram.split()[1]])) \
		/ log( 2 )
	
	return minfo

def plot_freq_words(words,n=50):
	"""
	Plot top frequent 50 or N words from a given word list
	"""
	top_freq_words = top_items(words,n=50)
	labels = [top_freq_words[i][0] for i in range(len(top_freq_words))]
	x = range(len(top_freq_words))
	np = len(top_freq_words)
	y = []

	for i in range(np):
		y = y + [top_freq_words[i][1]]
	
	plt.plot(x,y,'go',ls='dotted')
	#plt.xticks(range(0, len(top_freq_words) + 1, 1))
	plt.xlabel("Word Ranking")
	plt.ylabel("Word Frequency")
	plt.show()


def plot_freq_words_tagged(words,n=50):
	"""
	Plot top frequent 50 or N words from a given word list
	"""
	top_freq_words = top_items(words,n=50)
	labels = [top_freq_words[i][0] for i in range(len(top_freq_words))]
	x = range(len(top_freq_words))
	np = len(top_freq_words)
	y = []

	for i in range(np):
		y = y + [top_freq_words[i][1]]
	
	plt.plot(x,y,'go',ls='dotted')
	#plt.xticks(range(0, len(top_freq_words) + 1, 1))
	plt.xlabel("Word Ranking")
	plt.ylabel("Word Frequency")

	for num,label in enumerate(labels):
		plt.text(x[num],y[num], label, rotation=45)
	
	plt.show()




def plot_hist(words,n=50):
	"""
	Pot histogram of top N words
	"""
	tw = top_items(words,n=50)
	wordst = [tw[i][0] for i in range(len(tw))]
	freq = [tw[j][1] for j in range(len(tw))]
	pos = np.arange(len(wordst))
	width = 1.0
	ax = plt.axes(frameon=True)
	ax.set_xticks(pos)
	#ax.set_yticks(range(0,max(freq),10))
	ax.set_xticklabels(wordst,rotation='vertical',fontsize=9)
	plt.bar(pos,freq,width, color='g')
	plt.show()


def dispersion_plot(text,words):
	"""
	Code adopted from http://nltk.googlecode.com/svn/trunk/doc/api/nltk.draw.dispersion-pysrc.html
	"""
	wordst = tokenize(text)
	points = [(x,y) for x in range(len(wordst))\
	for y in range(len(words)) if wordst[x] == words[y]]
	if points:
		x,y = zip(*points)
	else:
		x = y = ()
	
	plt.plot(x,y,"go",scalex=.2)
	plt.yticks(range(len(words)),words,color="b")
	plt.ylim(-1,len(words))
	plt.title("Lexical Dispersion Plot")
	plt.xlabel("Word Offset")
	plt.show()


def tag_cloud(words,image="tc_t.png"):
	"""
	create tag cloud of top 100 words form a wordlist
	depends on pytagcloud
	"""
	top_words = top_items(words,n=100)
	tags = make_tags(top_words, maxsize=100)
	create_tag_image(tags, image, size=(900, 600), \
	fontname='Philosopher')


def cooccurrence_matrix(words):
	"""
	Find co-occourance matrix from words
	"""
	matrix = defaultdict(lambda : defaultdict(int))
	for i in xrange(len(words)-1):
		for j in xrange(i+1, len(words)):
			word1, word2 = [words[i], words[j]]
			matrix[word1][word2] += 1
			matrix[word2][word1] += 1
	return matrix


def cooccurrence_matrix_corpus(corpus):
	"""
	Create co-occurance matrix from corpus
	Takes list of list as input
	Each list will be words from the corpus
	"""
	matrix = defaultdict(lambda : defaultdict(int))

	for corpora in corpus:
		for i in xrange(len(corpora)-1):
			for j in xrange(i+1, len(corpora)):
				word1, word2 = [corpora[i],corpora[j]]
				matrix[word1][word2] += 1
				matrix[word2][word1] += 1

	return matrix

def create_graph(matrix,word,n=5):
	"""
	Create graph of top N co-occourance
	TODO - auto select 5 + 3 node graph 
	"""
	w = sort_dict(matrix[word])[:n+1]
	g1 = [i[0] for i in w if i[0] != word]
	graph = {}
	graph[word] = g1[:n]
	all = []

	for term in g1[:n]:
		tmpl = sort_dict(matrix[term])
		tmplist = [j[0] for j in tmpl if j[0] != term] 
		all.extend(tmplist)
		graph[term] = tmplist
	
	ngw = {}
	k = graph.keys()

	alling = []
	alling.extend(k)
	for g in k:
		if g != word:
			tmp = list(set([o for o in graph[g]]))
			ngw[g] = [o for o in graph[g] if o not in alling][:3]
			alling.extend(tmp)

	for k,v in ngw.items():
		if len(v) == 0:
			del ngw[k]
			graph[word].remove(k)	
	ngw[word] = graph[word] 
	return ngw


def sort_dict(dicti):
	"""
	Sort dictionary
	"""
	sdict = sorted(dicti.iteritems(), key=itemgetter(1),\
	reverse=True)
	return sdict


def traverse(graph,start,nodes):
	"""
	Create a graph for plotting
	#TODO explain proper
	"""
	for t in nodes:
		graph.add_edge(start,t)

def grap_plotter(worddict,cw):
	"""
	Plot network graph
	TODO explain
	"""
	wgraph = nx.MultiGraph()
	k = worddict.keys()
	initgrap = list(worddict[cw])
	for g in initgrap:
		wgraph.add_edge(cw,g)
		traverse(wgraph,g,list(worddict[g]))
	
	pos=nx.graphviz_layout(wgraph,prog='twopi')
	#pos=nx.graphviz_layout(wgraph,prog='twopi',splines="polyline")
	plt.figure(figsize=(8,8))
	plt.axis('equal')
	nx.draw(wgraph,pos,style='solid',alpha=1.0,font_size=16,font_color='black',\
	edge_color='black',node_size=4500,node_color='#B66E01',node_shape='o',font_family='calibri',\
	cmap=plt.cm.Blues,arrows=False,arrowhead="forward")
	plt.show()


def list_files(directory):
	"""
	Lists .txt files in a directory
	"""
	files = [os.path.join(directory,f) for f in \
	os.listdir(directory) if f.endswith(".txt")]
	return files

def corpus(directory):
	"""
	Create corpus from a directory
	"""
	corpusc = []
	files = list_files(directory)
	for f in files[:100]:
		text = open(f,'r').read()
		words = tokenize(text)
		swords = stop_filter(words)
		corpusc.append(swords)

	return corpusc

def join_list(lists):
	"""
	Convert a list of list to list
	to get all the words from corpus output
	"""
	new_list = []
	for l in lists:
		new_list.extend(l)
	return new_list

if __name__ == "__main__":
	#text = open('/usr/share/nltk_data/corpora/gutenberg/shakespeare-caesar.txt','r').read()
	text = open('gpl-2.0.txt','r').read()
	words = tokenize(text)
	#print words
	swords = stop_filter(words)
	"""print swords
	word_freq = freq_count(swords)
	print word_freq
	top_words = top_items(swords)
	print top_words
	wp = word_propo(swords)
	print wp
	wtr = word_type_ratio(words)
	print wtr
	plot_freq_words(swords)
	plot_freq_words_tagged(swords)
	plot_hist(swords)
	bigrams = ngrams(words,n=2)
	print bigrams
	trigrams = ngrams(words,n=3)
	print trigrams
	plot_hist(bigrams)
	plot_hist(trigrams)
	plot_freq_words_tagged(bigrams)
	plot_freq_words_tagged(trigrams)
	dispersion_plot(text,['software','license','copy','gnu','program','free'])
	#tag_cloud(swords)"""
	#t = tscore(words)
	#m = mutual_info(words)
	#print m
	"""top5 = top_items(swords,n=5)
	t1= top5[0][0]
	ccm = cooccurrence_matrix(swords)
	#create_graph(ccm,"software")
	g = create_graph(ccm,t1,n=5)
	print t1, "T",g
	grap_plotter(g,t1) """
	
	d = "/usr/share/nltk_data/corpora/movie_reviews/pos"
	fl = list_files(d)
	corpora = corpus(d)
	#corpora = corpus(d[:100])
	top5 = top_items(join_list(corpora),n=7)
	t1 = top5[0][0]
	ccm = cooccurrence_matrix_corpus(corpora)
	g = create_graph(ccm,t1)
	print g
	grap_plotter(g,t1)
	
