from __future__ import division
import math

def ngrams(words,n=2):
    grams = [" ".join(words[x:x+n]) for x in xrange(len(words)-n+1)]
    return grams

def tscore(words):
	grams = ngrams(words,n=2) #ngrams function from prev slide
	wordcount = {}
	gramcount = {}
	tsc = {}
	[ wordcount.__setitem__(word, 1 + \
	wordcount.get( word,0 )) for word in words ]
	[ gramcount.__setitem__(gram, 1 + \
	gramcount.get( gram,0 )) for gram in grams ]
	for gram in grams:
		tsc[gram] =  (gramcount[gram]  - (1/len(words)) * \
		wordcount[gram.split()[0]]  * wordcount[gram.split()[1]])\
		/ math.sqrt( gramcount[gram])
	return tsc



def mutual_info(words):
	grams = ngrams(words,n=2) #ngrams function from prev slide
	wordcount = {}
	gramcount = {}
	minfo = {}
	[ wordcount.__setitem__(word, 1 + \
	wordcount.get( word,0 )) for word in words ]
	[ gramcount.__setitem__(gram, 1 + \
	gramcount.get( gram,0 )) for gram in grams ]
	for gram in grams:
		minfo[gram] = (math.log( len(words) * gramcount[ gram ] \
		/ wordcount[gram.split()[0]] * wordcount[ gram.split()[1]])) \
		/ math.log( 2 )
	return minfo

#REF http://streamhacker.com/2010/page/2/


if __name__ == "__main__":
	words = "John likes to watch movies. Mary likes too."\
	.lower().split()

	a = mutual_info(words)
	print a
