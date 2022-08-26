#!/usr/bin/env python
from __future__ import division
import re
from math import sqrt
from operator import itemgetter
import numpy as np
import matplotlib.pyplot as plt

def tokenize(text):
	tokenozer = re.compile('\\W*')
	return tokenozer.split(text.strip().lower())

def freq_count(seqeunces):
	frequency = dict([seq, seqeunces.count(seq)]\
	for seq in set(seqeunces))
	return frequency


def word_count(text):
	words = tokenize(text)
	words = stop_filter(words)
	word_freq = dict([word, words.count(word)] for word \
	in set(words) if len(word) > 1)
	return word_freq

def top_words(text,n=50):
	wordfreq = word_count(text)
	topwords = sorted(wordfreq.iteritems(), key = itemgetter(1),\
	reverse=True)[:n]
	return topwords


def word_propo(text):
	words = tokenize(text)
	#TODO add stop filter here else this wont work
	wc = word_count(text)
	propo = dict([(word, wc[word]/len(words)) for word \
	in set(words)])
	return propo

def word_type_ratio(text):
	words = tokenize(text)
	ratio = len(words) / len(set(words))
	return ratio


def vec_length(vec):
	"""
	Eucledian length
	Length of vector
	"""
	mvec = [v * v for v in vec]
	length = sqrt(sum(mvec))
	return length

def vec_dot_prod(veca,vecb):
	"""
	Dot product
	Inner product
	"""
	if len(veca) == len(vecb):
		vecm = [veca[i] * vecb[i] for i in range(len(veca))]
		return sum(vecm)

def cosine_vec(veca,vecb):
	"""
	Angle of two vectors
	"""
	if len(veca) == len(vecb):
		len1 = vec_length(veca)
		len2 = vec_length(vecb)
		cosine = vec_dot_prod(veca,vecb) / (len1 * len2)
		return cosine

def plot_freq(text):
	tfw = top_words(text)
	words = [tfw[i][0] for i in range(len(tfw))]
	x = range(len(tfw))
	np = len(tfw)
	y = []
	for item in range(np):
		y = y + [tfw[item][1]]

	plt.plot(x,y,'go',ls='dotted')
	#plt.autoscale(enable=True, axis='both', tight=None)
	plt.xticks(range(0, len(words) + 1, 1))
	#plt.yticks(range(0, max(y) + 1, 10))
	plt.xlabel("Word Ranking")
	plt.ylabel("Word Frequency")
	plt.show()	

def plot_freq_tag(text):
	tfw = top_words(text)
	words = [tfw[i][0] for i in range(len(tfw))]
	x = range(len(tfw))
	np = len(tfw)
	y = []
	for item in range(np):
		y = y + [tfw[item][1]]
	
	fig = plt.figure()
	ax = fig.add_subplot(111,xlabel="Word Rank",\
	ylabel="Word Freqquncy")
	ax.set_title('Top 50 words')
	ax.plot(x, y, 'go-',ls='dotted')
	plt.xticks(range(0, len(words) + 1, 1))
	#plt.autoscale(enable=True, axis='both', tight=None)
	#plt.yticks(range(0, max(y) + 1, 10))
	for i, label in enumerate(words):
		plt.text (x[i], y[i], label ,rotation=45)
	plt.show()


def plot_hist(text):
	tw = top_words(text)
	words = [tw[i][0] for i in range(len(tw))]
	freq = [tw[j][1] for j in range(len(tw))]
	pos = np.arange(len(words))
	width = 1.0
	ax = plt.axes(frameon=True)
	ax.set_xticks(pos)
	ax.set_yticks(range(0,max(freq),10))
	ax.set_xticklabels(words,rotation='vertical',fontsize=9)
	plt.bar(pos,freq,width, color='b')
	#plt.autoscale(enable=True, axis='both', tight=None)
	plt.show()

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
	't', 'can', 'will', 'just', 'don', 'should', 'now']
	
	stopless = [word for word in words if word not in stops]

	return stopless


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
	#plt.xticks(range(0, len(wordst), 30))
	#plt.autoscale(enable=True, axis='both', tight=None)
	plt.ylim(-1,len(words))
	plt.title("Lexical Dispersion Plot")
	plt.xlabel("Word Offset")
	plt.show()
	

from pytagcloud import create_tag_image, make_tags

def create_tag_cloud(text):
	topw = top_words(text,n=100)
	tags = make_tags(topw, maxsize=80)
	create_tag_image(tags, 'cloud_large.png', size=(900, 600), \
	fontname='Philosopher')


text = "How can this be implemented? There are a lot of \
		subtleties, such as dot being used in abbreviations."


#plot_freq(text)

gpl = open('gpl-2.0.txt','r').read()
#wp = word_propo(text)

#for word, propo in wp.items():
#	print word, "\t\t", propo
text = "I shot an elephant in my pajamas. He saw the fine \
		fat trout in the brook."

lt = open('BoWAndOr.tex','r').read()

#gpl = open('gpl-2.0.txt','r').read()

#gita = open('gita_e.txt','r').read()

#plot_hist(gita)
#plot_freq_tag(gita)
#plot_freq(gita)
create_tag_cloud(gpl)
dispersion_plot(gpl,['software','license','copy','gnu','program','free'])
plot_hist(gpl)
plot_freq_tag(gpl)
plot_freq(gpl)
#words = tokenize(text)
#wc = word_count(text)
#print words, len(words)
#print wc.keys(), len(wc)

r = word_type_ratio(gpl)
print r

x = (19,9,7,13,22,0,1,2)
y = (33,0,17,3,32,0,1,0)

vdp = vec_dot_prod(x,y)

print vdp

cv = cosine_vec(x,y)

print cv

tv = top_words(gpl,n=20)
#print tv

for v,f in tv:
	print "%s %d" %(v,f)


from nltk import sent_tokenize, ne_chunk, pos_tag, word_tokenize
from collections import defaultdict
#d.setdefault(j, []).append(i)
def extract_entities(text):
	sents = sent_tokenize(text)
	chunks = [ ne_chunk(pos_tag(word_tokenize(sent))) for sent in sents]
	print chunks
	for chunk in chunks:
		#print help(chunk)
		if hasattr(chunk,'Tree'):
			print chunk.node, '\t', ' '.join(ne[0] for ne in chunk.leaves())
				

#http://timmcnamara.co.nz/post/2650550090/extracting-names-with-6-lines-of-python-code


if __name__ == "__main__":
	sent = "Barack Obama re-relected as American president. India is a growing country."
	extract_entities(sent)
