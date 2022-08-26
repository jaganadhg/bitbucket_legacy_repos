import re

def bag_of_words(docs):
	stops = ['to','too','also']
	splitter = re.compile('\W*')
	token_list = [splitter.split(doc.lower()) for doc in docs]
	vocab = list(set(token_list[0]).union(*token_list))
	vocab =[v for v in vocab if v not in stops and len(v) > 1]
	vocab_idex = dict( [ ( word, vocab.index(word) ) for word \
	in vocab] )
	bow = [[tokens.count(word) for word in vocab_idex.keys()] \
	for tokens in token_list]
	print vocab_idex
	for bag in bow:
		print bag

d = ("John likes to watch movies. Mary likes too.",\
"John also likes to watch football games.")

bag_of_words(d)
